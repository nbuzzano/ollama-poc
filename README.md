# Mi Agente de IA Robusto con LangChain y Ollama

**Proyecto educativo** para aprender a construir agentes conversacionales locales y seguros. El objetivo principal es la experimentación y el aprendizaje —este repositorio muestra patrones prácticos y configurables, no políticas de producción ni despliegue seguro por defecto.

Este proyecto implementa un agente de IA conversacional modular usando una pila de código abierta:
- **LLM Local:** Ollama (ej. con Llama 3 o modelos comunitarios)
- **Framework de Agente:** LangChain (LCEL, tools y agents)
- **Herramientas:** Búsqueda en Wikipedia y Google (SerpAPI) como ejemplos de 'external tools'
- **Memoria:** Soporte para buffer, ventana, resumen y memoria vectorial (Chroma)
- **Seguridad:** Capas de Guardrails para validación de entrada y salida (ej. evitar PII y respuestas no útiles)

> En el README encontrarás: ejecución rápida, configuración de memoria, cómo agregar herramientas, y referencias para seguir aprendiendo; para un tutorial paso a paso consulta `docs/learning.md`.

## Arquitectura

El proyecto sigue una arquitectura modular donde la configuración, las herramientas, la lógica del agente y los guardrails están separados para facilitar el mantenimiento y la escalabilidad.

## Configuración

Sigue estos pasos antes de ejecutar el agente.

1.  **Clona el repositorio:**
    ```bash
    git clone <tu-repositorio>
    cd mi_agente_ia
    ```

2.  **Crea un entorno virtual e instala las dependencias:**
    ```bash
    python -m venv venv
    # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process # en windows
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configura tus claves y opciones (archivo `.env`):**
    Copia `.env.example` a `.env` y añade tu clave de SerpAPI y otras variables opcionales:
    ```bash
    cp .env.example .env
    # luego edita .env y rellena las claves
    ```

    Variables relevantes:
    - `SERPAPI_API_KEY` (obligatoria para las búsquedas de Google/SerpAPI)
    - `OLLAMA_BASE_URL` (por defecto `http://localhost:11434`)
    - `LLM_MODEL` (modelo por defecto, e.g. `mistral` o `llama3`)
    - `MEMORY_TYPE` (opcional: `buffer|window|summary|combined|vector`)
    - `MEMORY_K` (opcional: tamaño de la ventana para `window`)
    - `MEMORY_PERSIST_DIR` (opcional: carpeta para Chroma si usas memoria vectorial)

    Para opciones de memoria avanzada (memoria vectorial), consulta `docs/memory_vector.md`.

4.  **Instala y arranca Ollama / descarga un modelo:**
    Debes tener Ollama instalado y el servicio disponible localmente.
    ```bash
    # Ejemplo: descarga un modelo
    ollama pull llama3

    # Opcional: usa gpt-oss:120b-cloud si lo prefieres
    ```

5.  **Ejecuta el agente:**
    - Modo guardrails (por defecto):
    ```bash
    python main.py
    ```

    - Modo 'functions' / experimental (usa `main_()`):
    ```bash
    python -c "from main import main_; main_()"
    ```

    Al arrancar se imprimirá el tipo de memoria elegido (p. ej. `🔧 Memoria configurada: buffer (k=5)`).



## Ejecución

Para iniciar el agente en modo de chat interactivo, ejecuta:
```bash
python main.py