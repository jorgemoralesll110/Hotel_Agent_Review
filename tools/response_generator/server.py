from fastmcp import MCPTool

class ResponseGenerator(MCPTool):

    def generate_reply(self, review: str, sentiment: str):

        if sentiment == "positive":
            reply = (
                "¡Muchas gracias por compartir su experiencia positiva! "
                "Nos alegra saber que ha disfrutado de su estancia. "
                "Será un placer volver a recibirle pronto."
            )

        elif sentiment == "negative":
            reply = (
                "Lamentamos sinceramente que su experiencia no haya sido satisfactoria. "
                "Agradecemos que nos lo haya comunicado y revisaremos lo sucedido para mejorar. "
                "Si desea ampliar la información, estaremos encantados de atenderle."
            )

        else:
            reply = (
                "Gracias por compartir su opinión. "
                "Seguiremos trabajando para ofrecer siempre la mejor experiencia posible."
            )

        return {"reply": reply}

tool = ResponseGenerator()