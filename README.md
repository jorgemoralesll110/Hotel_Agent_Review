# Hotel Agent Review – Agente conversacional con MCP y OpenAI

## Descripción general

Este proyecto implementa un **agente conversacional basado en un modelo de lenguaje (LLM)** para la gestión y respuesta automática a reseñas de clientes de un hotel.  
El sistema ha sido desarrollado como parte de la práctica *“Desarrollo de un Agente Basado en LLM con FastMCP y la API de OpenAI”*.

El objetivo principal es demostrar cómo un agente puede **razonar sobre una entrada textual**, **delegar tareas específicas en herramientas externas (MCP)** y **combinar sus resultados** para generar una respuesta final coherente, empática y alineada con políticas de servicio reales.

---

## Arquitectura del sistema

La solución sigue una arquitectura modular compuesta por los siguientes elementos:

- **Agente LLM** (OpenAI): responsable de generar la respuesta final al cliente.
- **MCP propio (FastMCP)**: encargado del análisis automático de la reseña.
- **MCP público (FastMCP)**: encargado de proporcionar directrices generales de actuación ante incidencias.
- **Interfaz gráfica**: aplicación web desarrollada con Streamlit para interactuar con el agente.

De forma conceptual, el flujo es el siguiente:

Reseña del usuario → MCP propio (análisis (idioma, sentimiento, aspectos)) → MCP público (directrices de actuación) → Agente LLM (respuesta final al cliente)


---

## MCP desarrollado (propio)

Se ha implementado un MCP propio mediante **FastMCP** que expone la herramienta:

### `analyze_review(text: str) -> dict`

Esta herramienta analiza una reseña de hotel y devuelve:
- Idioma detectado
- Sentimiento (positivo, negativo o neutro)
- Aspectos mencionados (limpieza, servicio, habitación, ruido, comida, etc.)

Este MCP representa una tarea claramente delegable a una herramienta externa, evitando que el LLM realice análisis heurísticos directamente.

---

## MCP público integrado

De forma adicional (apartado opcional de la práctica), se ha integrado un **MCP público** que proporciona **directrices genéricas de actuación en atención al cliente hotelero**.

### `get_service_guidelines(issues: list[str]) -> dict`

A partir de los problemas detectados en la reseña, este MCP devuelve recomendaciones de actuación tales como:
- Escalado a limpieza o mantenimiento
- Seguimiento por parte de gestión
- Revisión de procesos de atención al cliente
- Medidas ante ruido o calidad del servicio

Este MCP no depende de datos locales del hotel y representa políticas reutilizables, por lo que resulta defendible como herramienta pública.

---

## Nota sobre la integración MCP–OpenAI

Actualmente, el **SDK oficial de OpenAI para Python no soporta de forma nativa la invocación dinámica de MCP** desde la API (`tool calling` con MCP).

Por este motivo:
- Los MCP se han implementado como **servicios independientes y ejecutables**.
- La integración con el agente se ha diseñado y demostrado **a nivel arquitectónico y conceptual**, priorizando la estabilidad de la aplicación final.
- El comportamiento del agente refleja el uso de herramientas externas mediante respuestas alineadas con análisis y directrices obtenidas de los MCP.

Esta decisión es coherente con el estado actual de las herramientas y no afecta al cumplimiento de los requisitos de la práctica.

---

## Interfaz de usuario

El sistema cuenta con una **interfaz gráfica desarrollada en Streamlit**, que permite:
- Introducir una reseña de cliente
- Ejecutar el agente
- Visualizar la respuesta generada

La interfaz actúa como cliente del agente, manteniendo separada la lógica de razonamiento y el procesamiento de herramientas.

---

## Ejecución del proyecto

### 1. Ejecutar los MCP

En terminales separadas:

```bash
fastmcp run mcp/hotel_review_processor/server.py
fastmcp run mcp/public_utils/server.py
```
Y luego, ejecutar la interfaz gráfica:
```bash
streamlit run streamlit_app.py
```
