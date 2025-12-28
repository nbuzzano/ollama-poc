from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, SerpAPIWrapper
from langchain_core.tools import Tool
from config import SERPAPI_API_KEY

# agent/tools.py

from langchain_core.tools import tool # <- Importamos el decorador @tool


@tool
def wikipedia_search(query: str) -> str:
    """Busca en Wikipedia. Útil para cuando necesitas responder preguntas sobre temas enciclopedicos, personas, lugares o conceptos históricos."""
    api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000)
    return api_wrapper.run(query)

@tool
def google_search(query: str) -> str:
    """Busca en Google. Útil para cuando necesitas responder preguntas sobre eventos actuales, el clima, o temas muy recientes. Siempre usa esta si la información cambia con el tiempo."""
    api_wrapper = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
    return api_wrapper.run(query)

def get_tools():
    """Devuelve una lista de las herramientas definidas con el decorador @tool."""
    return [wikipedia_search, google_search]

