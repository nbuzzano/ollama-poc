# Mi Agente de IA Robusto con LangChain y Ollama

Este proyecto es una implementación robusta de un agente de IA conversacional utilizando una pila de código abierto:
- **LLM Local:** Ollama (ej. con Llama 3)
- **Framework de Agente:** LangChain
- **Herramientas:** Búsqueda en Wikipedia y Google (SerpAPI)
- **Seguridad:** Capa de Guardrails para validación de entrada y salida.

## Arquitectura

El proyecto sigue una arquitectura modular donde la configuración, las herramientas, la lógica del agente y los guardrails están separados para facilitar el mantenimiento y la escalabilidad.

## Configuración

descargar ollama server https://ollama.com/download/windows

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

3.  **Configura tus claves de API:**
    Crea un archivo llamado `.env` en la raíz del proyecto copiando el contenido de `.env.example` y añade tu clave de SerpAPI:
    ```
    SERPAPI_API_KEY="tu_clave_de_serpapi"
    ```

4.  **Asegúrate de que Ollama esté corriendo:**
    Debes tener Ollama instalado y un modelo descargado.
    ```bash
    ollama pull llama3

    >> se puede usar gpt-oss:120b-cloud, que ya esta disponible.
    ```


## Ejecución

Para iniciar el agente en modo de chat interactivo, ejecuta:
```bash
python main.py