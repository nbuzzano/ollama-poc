import os
from dotenv import load_dotenv
from pathlib import Path

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Configuración del LLM
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral") # >> gpt-oss:120b-cloud

# Configuración de memoria (opcional)
# MEMORY_TYPE puede ser: 'buffer' | 'window' | 'summary' | 'combined' | 'vector'
MEMORY_TYPE = os.getenv("MEMORY_TYPE", "buffer")
# Para 'window' puedes controlar cuántas interacciones mantener con MEMORY_K
MEMORY_K = int(os.getenv("MEMORY_K", "5"))
# Para memoria vectorial (si la usas) puedes definir un directorio de persistencia
MEMORY_PERSIST_DIR = os.getenv("MEMORY_PERSIST_DIR", "")

# Configuración de APIs
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise ValueError("La clave de API de SerpAPI no se ha configurado. Por favor, añádela a tu archivo .env")

# Rutas del proyecto
PROMPT_TEMPLATE_PATH = os.path.join("prompts", "agent_prompt.v2.txt")

# Directorio por defecto para archivos locales buscables por el agente
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = os.path.join(str(PROJECT_ROOT), "data", "local_files")

