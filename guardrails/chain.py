from langchain_core.runnables import RunnableLambda
from agent.agent_builder import create_agent_executor
from guardrails.validators import validate_input, validate_output

def build_guarded_chain():
    """
    Construye la cadena final de ejecución, envolviendo el agente
    con los guardrails de entrada y salida.
    """
    # 1. Obtener el agente principal
    core_agent = create_agent_executor()

    # 2. Crear los Runnables para los guardrails
    input_guardrail = RunnableLambda(validate_input)
    output_guardrail = RunnableLambda(validate_output)

    # 2.b Añadir un Runnable de logging para inspeccionar la salida cruda
    def log_raw_output(data):
        # Imprime la estructura tal cual la devuelve el agente para diagnóstico
        print("RAW_AGENT_OUTPUT:", data)
        return data

    logging_guardrail = RunnableLambda(log_raw_output)

    # 3. Encadenar todo usando el LangChain Expression Language (LCEL)
    # El flujo es: Guardrail de Entrada -> Agente Principal -> Guardrail de Salida
    # El flujo es: Guardrail de Entrada -> Agente Principal -> Logging -> Guardrail de Salida
    guarded_chain = input_guardrail | core_agent | logging_guardrail | output_guardrail
    
    return guarded_chain
