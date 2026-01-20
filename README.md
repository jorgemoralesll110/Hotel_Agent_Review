# Hotel Agent Review – Agente conversacional con MCP y OpenAI

## Descripción general

Este proyecto implementa un **agente conversacional basado en un modelo de lenguaje (LLM)** para la gestión y respuesta automática a reseñas de clientes de un hotel.  
El sistema ha sido desarrollado como parte de la práctica *“Desarrollo de un Agente Basado en LLM con FastMCP y la API de OpenAI”*.

El objetivo principal es demostrar cómo un agente puede **razonar sobre una entrada textual**, **delegar tareas específicas en herramientas externas (MCP)** y **combinar sus resultados** para generar una respuesta final coherente, empática y alineada con políticas de servicio reales.

---

## Arquitectura del sistema

La solución sigue una arquitectura modular compuesta por los siguientes elementos:

- **Agente LLM (OpenAI)**: responsable de generar la respuesta final al cliente y decidir cuándo utilizar herramientas externas.
- **MCP propio (FastMCP)**: encargado del análisis automático de la reseña del cliente.
- **MCP genérico adicional (FastMCP)**: encargado de proporcionar directrices generales de actuación en atención al cliente.
- **Sistema de persistencia**: almacenamiento local de conversaciones y mensajes mediante SQLite.
- **Interfaz gráfica**: aplicación web desarrollada con Streamlit para interactuar con el agente.

De forma conceptual, el flujo del sistema es el siguiente:

Reseña del usuario → MCP de análisis (idioma, sentimiento, aspectos) → MCP de directrices → Agente LLM → Respuesta final al cliente

---

## MCP desarrollado (propio)

Se ha implementado un MCP propio mediante **FastMCP** que expone la herramienta:

### `analyze_review(text: str) -> dict`

Esta herramienta analiza una reseña de hotel y devuelve información estructurada que incluye:
- Idioma detectado
- Sentimiento (positivo, negativo o neutro)
- Aspectos mencionados (limpieza, personal, habitación, ruido, comida, ubicación, etc.)

Este MCP encapsula lógica de procesamiento de lenguaje natural basada en reglas y librerías clásicas, delegando esta tarea fuera del LLM y favoreciendo una arquitectura modular y explicable.

---

## MCP genérico adicional

De forma adicional (apartado opcional de la práctica), se ha implementado un segundo MCP mediante **FastMCP**, de carácter genérico y reutilizable, que proporciona **directrices generales de actuación en atención al cliente hotelero**.

### `get_service_guidelines(issues: list[str]) -> dict`

A partir de los problemas detectados en la reseña, esta herramienta devuelve recomendaciones de actuación tales como:
- Escalado a limpieza o mantenimiento
- Seguimiento por parte de gestión
- Revisión de procesos de atención al cliente
- Medidas ante problemas de ruido o calidad del servicio

Este MCP no depende de datos locales específicos del hotel y representa políticas de actuación generales, por lo que resulta defendible como herramienta reutilizable.

---

## Persistencia de conversaciones

El sistema incorpora un **mecanismo de persistencia local** basado en **SQLite**, que permite almacenar:

- Conversaciones (identificador, fecha de creación y título)
- Mensajes asociados a cada conversación (rol, contenido, timestamp y metadatos opcionales)

Esta capa de persistencia permite mantener el historial de conversaciones entre ejecuciones de la aplicación y separar claramente la lógica de almacenamiento del razonamiento del agente.

---

## Nota sobre la integración MCP–OpenAI

Actualmente, el **SDK oficial de OpenAI para Python no ofrece soporte nativo específico para la invocación directa de MCP** como concepto unificado.

Por este motivo:
- Los MCP se implementan como **servicios independientes y ejecutables** mediante FastMCP.
- La integración con el agente se realiza a nivel **arquitectónico y de diseño**, mostrando claramente cómo el agente razona, delega tareas en herramientas externas y utiliza sus resultados para generar respuestas.
- El comportamiento del agente refleja el uso de herramientas externas de forma coherente con los requisitos de la práctica.

Esta aproximación es consistente con el estado actual de las herramientas y cumple los objetivos formativos del ejercicio.

---

## Interfaz de usuario

El sistema cuenta con una **interfaz gráfica desarrollada en Streamlit**, que permite:
- Introducir reseñas de clientes
- Interactuar con el agente conversacional
- Visualizar las respuestas generadas

La interfaz actúa como cliente del agente, manteniendo separada la lógica de razonamiento, el procesamiento de herramientas y la persistencia de datos.

---

## Ejecución del proyecto

### 1. Ejecutar los MCP

En terminales separadas:

```bash
fastmcp run mcp/hotel_review_processor/server.py
fastmcp run mcp/public_utils/server.py
```

### 2. Ejecutar la interfaz gráfica

```bash
streamlit run streamlit_app.py
```

La aplicación permitirá introducir reseñas de clientes y observar el flujo completo de razonamiento del agente y el uso de herramientas MCP.