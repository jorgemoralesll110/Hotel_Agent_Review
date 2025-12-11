import streamlit as st
from app import run_agent

st.title("Chatbot para responder reseñas de hoteles")

review = st.text_area("Escribe una reseña del cliente:")

if st.button("Generar respuesta"):
    if review.strip() != "":
        output = run_agent(review)
        st.write("### Respuesta generada:")
        st.success(output)