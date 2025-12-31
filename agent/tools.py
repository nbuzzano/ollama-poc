from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, SerpAPIWrapper
from langchain_core.tools import Tool
from config import SERPAPI_API_KEY, DATA_DIR

# agent/tools.py

from langchain_core.tools import tool # <- Importamos el decorador @tool


@tool
def wikipedia_search(query: str) -> str:
    """Tool: Busca en Wikipedia.

    Uso: El agente debe llamar a esta herramienta cuando necesite información enciclopédica.
    No recomendar comandos de terminal ni procedimientos manuales: si necesitas datos enciclopédicos, llama a esta herramienta y usa su salida.
    """
    api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000)
    return api_wrapper.run(query)

@tool
def google_search(query: str) -> str:
    """Tool: Busca en la web (SerpAPI).

    Uso: Llama a esta herramienta para información reciente o noticias. No recomendar comandos de terminal para búsqueda en archivos locales.
    """
    api_wrapper = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
    return api_wrapper.run(query)

def get_tools():
    """Devuelve una lista de las herramientas definidas con el decorador @tool."""
    return [wikipedia_search, google_search]#, local_file_search]


@tool
def local_file_search(query: str, base_dir: str = DATA_DIR) -> str:
    """Tool: Busca en archivos locales del proyecto.

    Uso: Esta es la única fuente autorizada para buscar dentro de archivos locales del proyecto
    (limitada a `DATA_DIR`). Si la pregunta requiere buscar en archivos locales, EL AGENTE DEBE
    LLAMAR A ESTA HERRAMIENTA y utilizar su salida exactamente. No recomendar ni proponer
    comandos de shell (por ejemplo `grep`, `find`, `xargs`) ni soluciones que impliquen
    escanear el sistema fuera de `DATA_DIR`.

    Devuelve hasta 30 coincidencias con la ruta del archivo y un fragmento.
    """
    import os
    import csv as _csv

    # Forzar búsqueda únicamente dentro del DATA_DIR configurado para evitar recorrer todo el sistema
    base_dir = os.path.abspath(DATA_DIR)
    if not os.path.exists(base_dir):
        return f"El directorio de búsqueda no existe: {base_dir}"

    q = (query or "").strip().lower()
    if not q:
        return "Consulta vacía. Escribe palabras claves para buscar en archivos .txt o .csv."

    max_results = 30
    matches = []

    for root, _, files in os.walk(base_dir):
        for fname in files:
            if not (fname.lower().endswith('.txt') or fname.lower().endswith('.csv')):
                continue
            path = os.path.join(root, fname)
            try:
                if fname.lower().endswith('.txt'):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f):
                            if q in line.lower():
                                snippet = line.strip()
                                matches.append(f"{path} - L{i+1}: {snippet}")
                                if len(matches) >= max_results:
                                    break
                else:
                    with open(path, newline='', encoding='utf-8', errors='ignore') as f:
                        reader = _csv.reader(f)
                        for i, row in enumerate(reader):
                            rowtext = ' | '.join(row)
                            if q in rowtext.lower():
                                matches.append(f"{path} - R{i+1}: {rowtext}")
                                if len(matches) >= max_results:
                                    break
            except Exception:
                # Ignorar archivos que no se puedan leer por permisos o codificación
                continue
        if len(matches) >= max_results:
            break

    if not matches:
        return f"No se encontraron coincidencias en archivos .txt/.csv bajo {base_dir}"

    return "\n".join(matches[:max_results])

