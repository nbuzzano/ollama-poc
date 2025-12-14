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

def get_tools_old():
    """Crea y devuelve una lista de herramientas para el agente."""

    # Herramienta 1: Wikipedia
    wikipedia_api = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000)
    wikipedia_tool = Tool(
        name="WikipediaSearch",
        func=WikipediaQueryRun(api_wrapper=wikipedia_api).run,
        description="Útil para cuando necesitas responder preguntas sobre temas enciclopédicos, personas, lugares o conceptos históricos.",
    )

    # Herramienta 2: Google Search (SerpAPI)
    search_api = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
    serpapi_tool = Tool(
        name="GoogleSearch",
        func=search_api.run,
        description="Útil para cuando necesitas responder preguntas sobre eventos actuales, el clima, o temas muy recientes. Siempre usa esta si la información cambia con el tiempo.",
    )

    return [wikipedia_tool, serpapi_tool]
