from __future__ import annotations

from typing import Dict, List

GUIDELINES = {
    "cleanliness": [
        "Priorizar inspección inmediata de la habitación.",
        "Ofrecer cambio de habitación o limpieza urgente.",
        "Registrar incidente y revisar checklist de housekeeping.",
    ],
    "noise": [
        "Revisar fuente de ruido (habitaciones vecinas, calle, eventos).",
        "Ofrecer habitación alternativa o soluciones (tapones, horarios).",
        "Ajustar políticas de silencio y recordatorios a huéspedes.",
    ],
    "staff": [
        "Revisar el caso con el equipo implicado (sin culpar al cliente).",
        "Ofrecer disculpa formal y plan de mejora de atención.",
        "Reforzar formación en trato y protocolos de recepción.",
    ],
    "room": [
        "Verificar mantenimiento (AC, baño, cama) y actuar con urgencia.",
        "Ofrecer cambio de habitación o compensación proporcional.",
        "Abrir ticket de mantenimiento con prioridad.",
    ],
    "food": [
        "Revisar calidad/variedad del servicio.",
        "Ofrecer alternativa (early breakfast, opciones sin alérgenos, etc.).",
        "Registrar feedback y ajustar proveedores/menú si procede.",
    ],
    "location": [
        "Aclarar información de distancias y transporte.",
        "Ofrecer recomendaciones personalizadas (rutas, transporte).",
        "Mejorar descripciones en web/booking para evitar expectativas erróneas.",
    ],
    "price": [
        "Explicar valor aportado (servicios incluidos) sin confrontar.",
        "Revisar política de precios en fechas pico.",
        "Ofrecer gesto comercial si procede (upgrade, late checkout).",
    ],
}


def get_service_guidelines(issues: List[str]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for issue in issues:
        key = str(issue).strip().lower()
        if key in GUIDELINES:
            out[key] = GUIDELINES[key]
        else:
            out[key] = [
                "Agradecer el feedback y pedir disculpas si procede.",
                "Investigar internamente el incidente.",
                "Proponer una solución y explicar medidas preventivas.",
            ]
    return out