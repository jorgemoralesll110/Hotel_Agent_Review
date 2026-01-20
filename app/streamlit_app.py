
import json
import datetime as dt
import streamlit as st

from app import run_agent, build_next_history
from storage import (
    init_db,
    create_conversation,
    update_conversation_title,
    add_message,
    list_conversations,
    load_conversation,
    delete_conversation,
)

st.set_page_config(page_title="Hotel Review Agent", layout="wide")
st.title("Agente de Análisis de Reseñas de Hoteles")
st.caption("Agente Inteligente para el Análisis Automático de Reseñas Hoteleras usando OpenAI y MCP.")

init_db()

st.session_state.setdefault("history", [])
st.session_state.setdefault("last_trace", [])
st.session_state.setdefault("last_messages_sent", [])
st.session_state.setdefault("last_tools", [])
st.session_state.setdefault("mode", "Análisis interno")

def new_conversation():
    st.session_state.history = []
    st.session_state.last_trace = []
    st.session_state.last_messages_sent = []
    st.session_state.last_tools = []

    st.session_state.conversation_id = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    title = "Conversación " + dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    create_conversation(st.session_state.conversation_id, title=title)

if "conversation_id" not in st.session_state:
    new_conversation()

with st.sidebar:
    st.subheader("Opciones")
    model = st.text_input("Modelo", value="gpt-4.1-mini")
    max_rounds = st.slider("Máx. rondas de herramientas", 1, 10, 6)
    show_debug = st.checkbox("Mostrar trazas", value=True)

    st.markdown("---")
    st.subheader("Modo")
    st.session_state.mode = st.radio("Salida", ["Análisis interno", "Respuesta al cliente"])

    st.markdown("---")
    st.subheader("Conversación actual")
    st.code(st.session_state.conversation_id)

    colA, colB = st.columns(2)
    with colA:
        if st.button("Nueva"):
            new_conversation()
            st.rerun()
    with colB:
        if st.button("Borrar actual"):
            # borra la actual y crea otra
            delete_conversation(st.session_state.conversation_id)
            new_conversation()
            st.rerun()

    st.markdown("---")
    st.subheader("Historial (cargar)")
    convs = list_conversations(200)
    conv_map = {f"{cid} — {title}": cid for (cid, _, title) in convs}
    load_choice = st.selectbox("Selecciona una conversación", ["(no cargar)"] + list(conv_map.keys()))

    if load_choice != "(no cargar)":
        cid = conv_map[load_choice]
        msgs = load_conversation(cid)
        st.session_state.conversation_id = cid
        st.session_state.history = [{"role": m["role"], "content": m["content"]} for m in msgs]
        st.success("Conversación cargada.")
        st.rerun()

    st.markdown("---")
    st.subheader("Borrar una conversación guardada")
    deletable = [(cid, title) for (cid, _, title) in convs if cid != st.session_state.conversation_id]

    if not deletable:
        st.info("No hay otras conversaciones para borrar (solo existe la actual).")
    else:
        del_labels = [f"{cid} — {title}" for (cid, title) in deletable]
        del_choice = st.selectbox("Elegir para borrar", ["(no borrar)"] + del_labels)
        confirm = st.checkbox("Confirmo borrado irreversible")

        if st.button("Borrar seleccionada", disabled=(del_choice == "(no borrar)" or not confirm)):
            idx = del_labels.index(del_choice)
            cid, _title = deletable[idx]
            delete_conversation(cid)
            st.success("Conversación borrada.")
            st.rerun()

st.markdown("### Conversación")

for m in st.session_state.history:
    st.chat_message("user" if m["role"] == "user" else "assistant").write(m["content"])

user_text = st.chat_input("Escribe/pega una reseña del hotel…")

if user_text:
    st.chat_message("user").write(user_text)
    add_message(st.session_state.conversation_id, "user", user_text, meta={"mode": st.session_state.mode})

    # si es primer mensaje, mejorar título
    if len(st.session_state.history) == 0:
        short = (user_text.strip().replace("\n", " "))[:48]
        if short:
            update_conversation_title(st.session_state.conversation_id, short)

    try:
        result = run_agent(
            user_text,
            chat_history=st.session_state.history,
            model=model,
            max_tool_rounds=max_rounds,
            mode=st.session_state.mode,
        )
    except Exception as e:
        st.error(str(e))
        st.stop()

    st.chat_message("assistant").write(result.final_answer)
    add_message(st.session_state.conversation_id, "assistant", result.final_answer, meta={"mode": st.session_state.mode})

    st.session_state.history = build_next_history(st.session_state.history, user_text, result.final_answer)

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
                    st.code(json.dumps(t["arguments"], ensure_ascii=False, indent=2), language="json")
                    st.write("**Result:**")
                    st.code(json.dumps(t["result"], ensure_ascii=False, indent=2), language="json")
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
                    st.code(json.dumps(payload["messages"], ensure_ascii=False, indent=2), language="json")
                    st.write("**Tools (OpenAI schema):**")
                    st.code(json.dumps(payload["tools"], ensure_ascii=False, indent=2), language="json")

    st.subheader("Tools descubiertas desde MCP")
    if not st.session_state.last_tools:
        st.info("Aún no se han descubierto tools (haz una consulta primero).")
    else:
        st.code(json.dumps(st.session_state.last_tools, ensure_ascii=False, indent=2), language="json")
