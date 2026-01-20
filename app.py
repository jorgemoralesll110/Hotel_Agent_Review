from __future__ import annotations
import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI
from fastmcp import Client

load_dotenv()

def _run_coro_sync(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    import threading

    box: Dict[str, Any] = {"value": None, "error": None}

    def _runner():
        try:
            box["value"] = asyncio.run(coro)
        except Exception as e:
            box["error"] = e

    t = threading.Thread(target=_runner, daemon=True)
    t.start()
    t.join()

    if box["error"] is not None:
        raise box["error"]
    return box["value"]



def _project_root() -> Path:
    return Path(__file__).resolve().parent


def _make_mcp_config() -> Dict[str, Any]:

    transport = os.getenv("MCP_TRANSPORT", "stdio").strip().lower()

    if transport == "http":
        review_url = os.getenv("MCP_REVIEW_URL", "http://localhost:8001/mcp").strip()
        policies_url = os.getenv("MCP_POLICIES_URL", "http://localhost:8002/mcp").strip()
        return {
            "mcpServers": {
                "review": {"transport": "http", "url": review_url},
                "policies": {"transport": "http", "url": policies_url},
            }
        }

    root = _project_root()
    review_server = str(root / "mcp" / "hotel_review_processor" / "server.py")
    policies_server = str(root / "mcp" / "public_utils" / "server.py")

    return {
        "mcpServers": {
            "review": {
                "transport": "stdio",
                "command": "python",
                "args": [review_server],
                "cwd": str(root),
            },
            "policies": {
                "transport": "stdio",
                "command": "python",
                "args": [policies_server],
                "cwd": str(root),
            },
        }
    }

def _get_attr(obj: Any, *names: str) -> Any:
    for n in names:
        if isinstance(obj, dict) and n in obj:
            return obj[n]
        if hasattr(obj, n):
            return getattr(obj, n)
    return None

def _tool_to_openai(tool_obj: Any) -> Dict[str, Any]:
    name = _get_attr(tool_obj, "name")
    desc = _get_attr(tool_obj, "description") or ""
    schema = _get_attr(tool_obj, "inputSchema", "input_schema", "input_schema_")

    if not isinstance(schema, dict):
        schema = {"type": "object", "properties": {}}

    return {
        "type": "function",
        "function": {
            "name": str(name),
            "description": str(desc),
            "parameters": schema,
        },
    }

def _normalize_tool_result(result: Any) -> Any:

    def to_jsonable(x: Any) -> Any:
        if x is None:
            return None
        if isinstance(x, (str, int, float, bool)):
            return x
        if isinstance(x, dict):
            return {str(k): to_jsonable(v) for k, v in x.items()}
        if isinstance(x, list):
            return [to_jsonable(i) for i in x]

        if hasattr(x, "model_dump"):
            try:
                return to_jsonable(x.model_dump())
            except Exception:
                pass

        if hasattr(x, "text"):
            try:
                return str(getattr(x, "text"))
            except Exception:
                pass

        return str(x)

    return to_jsonable(result)

@dataclass
class AgentResult:
    final_answer: str
    tool_trace: List[Dict[str, Any]]
    messages_sent: List[Dict[str, Any]]
    discovered_tools: List[Dict[str, Any]]

SYSTEM_PROMPT = """Eres un agente de atención al cliente de un hotel.
Objetivo: ayudar a un supervisor a entender una reseña y proponer acciones.

Reglas:
- Usa las herramientas MCP cuando sea útil.
- Responde en el idioma de la reseña si es posible.
- Da una salida final clara con: Resumen, Problemas detectados, Recomendaciones accionables, y Tono sugerido de respuesta al cliente.
- Si faltan datos, haz suposiciones prudentes y menciónalas.
"""

async def _run_agent_async(
    user_text: str,
    *,
    chat_history: Optional[List[Dict[str, Any]]] = None,
    model: str = "gpt-4.1-mini",
    max_tool_rounds: int = 6,
) -> AgentResult:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY en el entorno (.env).")

    oai = OpenAI(api_key=api_key)

    mcp_config = _make_mcp_config()
    mcp_client = Client(mcp_config)

    tool_trace: List[Dict[str, Any]] = []
    messages_sent: List[Dict[str, Any]] = []

    messages: List[Dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    if chat_history:
        messages.extend(chat_history)
    messages.append({"role": "user", "content": user_text})

    async with mcp_client:
        mcp_tools = await mcp_client.list_tools()
        openai_tools = [_tool_to_openai(t) for t in mcp_tools]

        for _round in range(max_tool_rounds):
            messages_sent.append({"messages": messages, "tools": openai_tools})

            resp = oai.chat.completions.create(
                model=model,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto",
            )
            msg = resp.choices[0].message

            if not getattr(msg, "tool_calls", None):
                return AgentResult(
                    final_answer=msg.content or "",
                    tool_trace=tool_trace,
                    messages_sent=messages_sent,
                    discovered_tools=openai_tools,
                )

            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
                }
            )

            for tc in msg.tool_calls:
                tool_name = tc.function.name
                raw_args = tc.function.arguments or "{}"
                try:
                    args = json.loads(raw_args)
                    if not isinstance(args, dict):
                        args = {}
                except json.JSONDecodeError:
                    args = {}

                try:
                    res = await mcp_client.call_tool(tool_name, args)
                    norm = _normalize_tool_result(res)
                    ok = True
                    err = None
                except Exception as e:
                    norm = {"error": str(e)}
                    ok = False
                    err = str(e)

                tool_trace.append(
                    {
                        "tool": tool_name,
                        "arguments": args,
                        "raw_arguments": raw_args,
                        "ok": ok,
                        "error": err,
                        "result": norm,
                    }
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(norm, ensure_ascii=False),
                    }
                )

        return AgentResult(
            final_answer=(
                "No pude completar el flujo dentro del máximo de rondas de herramientas. "
                "Revisa las trazas para ver qué tool call falló."
            ),
            tool_trace=tool_trace,
            messages_sent=messages_sent,
            discovered_tools=openai_tools,
        )

def run_agent(
    user_text: str,
    *,
    chat_history: Optional[List[Dict[str, Any]]] = None,
    model: str = "gpt-4.1-mini",
    max_tool_rounds: int = 6,
) -> AgentResult:
    return _run_coro_sync(
        _run_agent_async(
            user_text, chat_history=chat_history, model=model, max_tool_rounds=max_tool_rounds
        )
    )

def build_next_history(
    previous_history: List[Dict[str, Any]],
    user_text: str,
    assistant_text: str,
) -> List[Dict[str, Any]]:
    history = list(previous_history or [])
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": assistant_text})
    return history
