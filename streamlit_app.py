import streamlit as st
from app import run_agent

st.title("Asistente de respuesta a reseñas de hoteles ⭐")

review = st.text_area("Introduce la reseña del cliente")

if st.button("Generar respuesta"):
    if review.strip():
        reply = run_agent(review)
        st.subheader("Respuesta generada")
        st.success(reply)
