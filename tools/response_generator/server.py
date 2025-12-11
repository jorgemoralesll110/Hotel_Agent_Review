from fastmcp import MCPTool

class ResponseGenerator(MCPTool):

    def generate_reply(self, review: str, sentiment: str):

        if sentiment == "positive":
            return {
                "reply": f"¡Muchas gracias por su comentario! Nos alegra saber que ha disfrutado de su estancia. Esperamos volver a verle pronto."
            }

        if sentiment == "negative":
            return {
                "reply": "Lamentamos sinceramente que su experiencia no haya sido satisfactoria. Estamos revisando lo ocurrido para mejorar nuestro servicio."
            }

        return {
            "reply": "Gracias por compartir su opinión. Seguiremos trabajando para ofrecer la mejor experiencia posible."
        }

tool = ResponseGenerator()