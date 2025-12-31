
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from agent.tools import local_file_search


if __name__ == '__main__':
    # `local_file_search` está registrado como StructuredTool (decorador @tool)
    # por lo que hay que llamar a su método `run`.
    try:
        res = local_file_search.run('agent', base_dir='data/local_files/')
    except AttributeError:
        # En ambientes donde @tool no envuelve el callable, intentar llamar directamente
        res = local_file_search('agent', base_dir='data/local_files/')

    print('--- RESULTADOS ---')
    print(res)
