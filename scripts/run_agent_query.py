from guardrails.chain import build_guarded_chain
from agent.tools import local_file_search
from config import DATA_DIR


def run_query(question: str):
    # Si la pregunta menciona "archivos locales" hacemos la búsqueda local antes
    preface = ""
    if 'local' in question.lower() or 'locales' in question.lower() or 'archivos' in question.lower():
        print('Detección: la pregunta menciona archivos locales — ejecutando local_file_search...')
        try:
            # local_file_search es una StructuredTool; llamar a .run
            results = local_file_search.run(question, base_dir=DATA_DIR)
        except AttributeError:
            results = local_file_search(question, base_dir=DATA_DIR)
        preface = f"Resultados de la búsqueda local:\n{results}\n\n"

    chain = build_guarded_chain()
    print('Enviando pregunta al agente:')
    print(question)

    # Incluir resultados locales en el input para que el agente pueda usarlos
    input_payload = preface + question
    result = chain.invoke({"input": input_payload})
    print('\n=== RAW CHAIN RESULT ===')
    print(result)
    print('\n=== AGENT OUTPUT ===')
    print(result.get('output'))


if __name__ == '__main__':
    q = "Por favor busca la palabra 'agent' en mis archivos locales y devuelve las rutas y fragmentos donde aparece. Resume brevemente lo encontrado."
    run_query(q)
