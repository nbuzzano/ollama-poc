import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Configuración del LLM
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral") # >> gpt-oss:120b-cloud

# Configuración de APIs
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise ValueError("La clave de API de SerpAPI no se ha configurado. Por favor, añádela a tu archivo .env")

# Rutas del proyecto
PROMPT_TEMPLATE_PATH = os.path.join("prompts", "agent_prompt.v2.txt")
