# Guía de aprendizaje — Cómo avanzar con este proyecto

Este documento sirve como roadmap de aprendizaje para ayudarte a entender y extender el proyecto.

1) Ejecuta el agente y experiméntalo
   - Asegúrate de tener Ollama corriendo y un modelo descargado (`ollama pull llama3`).
   - Ejecuta `python main.py` y prueba preguntas que requieran buscar en la web (usa `google_search`) y preguntas enciclopédicas (Wikipedia).

2) Prueba distintos tipos de memoria
   - `MEMORY_TYPE=buffer` — historial completo (por defecto).
   - `MEMORY_TYPE=window` — solo últimas `k` interacciones.
   - `MEMORY_TYPE=summary` — genera resúmenes del historial (necesita `llm=` en la factory).
   - `MEMORY_TYPE=vector` — usa Chroma + embeddings para memoria a largo plazo (consulta `docs/memory_vector.md`).

3) Añade y prueba herramientas
   - Crea funciones con `@tool` en `agent/tools.py`.
   - Añade tests o invoca la función directamente desde un REPL antes de integrarla.

4) Experimenta con guardrails
   - Modifica `guardrails/validators.py` para adaptar validaciones de entrada/salida.
   - Añade reglas adicionales (p. ej. listas de términos sensibles, límites de contenido, etc.).

5) Debug y observabilidad
   - Usa el modo `verbose=True` del `AgentExecutor` para ver pasos intermedios.
   - Añade logs en los puntos críticos (entrada, llamadas a tools, resultados).

6) Extensiones posibles (proyectos finales)
   - Persistencia de preferencias de usuarios (memoria vectorial + metadata).
   - Interfaz web simple (FastAPI + WebSocket) para chat persistente.
   - Integración con un sistema de control de acceso / límites por usuario.

7) Lecturas recomendadas
   - LangChain docs: https://docs.langchain.com/
   - Ollama docs: https://ollama.com/docs
   - Artículos sobre memory architectures y herramientas de agentes.