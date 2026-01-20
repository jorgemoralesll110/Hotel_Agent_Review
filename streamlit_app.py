import json
import streamlit as st

from app import run_agent, build_next_history

st.set_page_config(page_title="Hotel Review Agent", layout="wide")

st.title("Hotel Review Agent (Streamlit + OpenAI + MCP Tool Calling)")
st.caption("Agente conversacional con llamadas reales a herramientas MCP y trazas visibles.")

if "history" not in st.session_state:
    st.session_state.history = []

if "last_trace" not in st.session_state:
    st.session_state.last_trace = []

if "last_messages_sent" not in st.session_state:
    st.session_state.last_messages_sent = []

if "last_tools" not in st.session_state:
    st.session_state.last_tools = []

with st.sidebar:
    st.subheader("Opciones")
    model = st.text_input("Modelo", value="gpt-4.1-mini")
    max_rounds = st.slider("Máx. rondas de herramientas", 1, 10, 6)
    show_debug = st.checkbox("Mostrar trazas", value=True)

    if st.button("🧹 Reiniciar conversación"):
        st.session_state.history = []
        st.session_state.last_trace = []
        st.session_state.last_messages_sent = []
        st.session_state.last_tools = []
        st.rerun()


st.markdown("### Conversación")

for m in st.session_state.history:
    if m["role"] == "user":
        st.chat_message("user").write(m["content"])
    elif m["role"] == "assistant":
        st.chat_message("assistant").write(m["content"])

user_text = st.chat_input("Escribe/pega una reseña del hotel…")

if user_text:
    st.chat_message("user").write(user_text)

    try:
        result = run_agent(
            user_text,
            chat_history=st.session_state.history,
            model=model,
            max_tool_rounds=max_rounds,
        )
    except Exception as e:
        st.error(str(e))
        st.stop()

    st.chat_message("assistant").write(result.final_answer)

    st.session_state.history = build_next_history(
        st.session_state.history, user_text, result.final_answer
    )

    st.session_state.last_trace = result.tool_trace
    st.session_state.last_messages_sent = result.messages_sent
    st.session_state.last_tools = result.discovered_tools


if show_debug:
    st.markdown("---")
    st.markdown("## Trazas (observabilidad)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tool calls ejecutadas")
        if not st.session_state.last_trace:
            st.info("Aún no hay tool calls (o el modelo respondió sin herramientas).")
        else:
            for i, t in enumerate(st.session_state.last_trace, start=1):
                with st.expander(f"{i}. {t['tool']} (ok={t['ok']})"):
                    st.write("**Arguments:**")
                    st.code(
                        json.dumps(t["arguments"], ensure_ascii=False, indent=2),
                        language="json",
                    )
                    st.write("**Result:**")
                    st.code(
                        json.dumps(t["result"], ensure_ascii=False, indent=2),
                        language="json",
                    )
                    if t["error"]:
                        st.error(t["error"])

    with col2:
        st.subheader("Mensajes enviados al modelo")
        if not st.session_state.last_messages_sent:
            st.info("Sin registros aún.")
        else:
            for j, payload in enumerate(st.session_state.last_messages_sent, start=1):
                with st.expander(f"Round {j}"):
                    st.write("**Messages:**")
                    st.code(
                        json.dumps(payload["messages"], ensure_ascii=False, indent=2),
                        language="json",
                    )
                    st.write("**Tools (OpenAI schema):**")
                    st.code(
                        json.dumps(payload["tools"], ensure_ascii=False, indent=2),
                        language="json",
                    )

    st.subheader("Tools descubiertas desde MCP")
    if not st.session_state.last_tools:
        st.info("Aún no se han descubierto tools (haz una consulta primero).")
    else:
        st.code(
            json.dumps(st.session_state.last_tools, ensure_ascii=False, indent=2),
            language="json",
        )
