def generate_reply(review: str, sentiment: str):

    if sentiment == "positive":
        reply = (
            "¡Muchas gracias por su comentario! "
            "Nos alegra saber que ha disfrutado de su estancia. "
            "Esperamos volver a verle pronto."
        )

    elif sentiment == "negative":
        reply = (
            "Lamentamos sinceramente que su experiencia no haya sido satisfactoria. "
            "Estamos revisando lo ocurrido para mejorar nuestro servicio."
        )

    else:
        reply = (
            "Gracias por compartir su opinión. "
            "Seguiremos trabajando para ofrecer la mejor experiencia posible."
        )

    return {"reply": reply}
