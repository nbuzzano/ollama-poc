from langchain_community.llms import Ollama
from langchain_classic.agents.agent import AgentExecutor 
from langchain_classic.agents.react.agent import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_classic.agents.format_scratchpad import format_to_openai_function_messages
from langchain_classic.agents.output_parsers.openai_functions import OpenAIFunctionsAgentOutputParser

from agent.tools import get_tools
from agent.memory import get_memory
from config import LLM_MODEL, OLLAMA_BASE_URL, PROMPT_TEMPLATE_PATH



def create_agent_executor():
    """
    Crea el ejecutor del agente principal usando el método robusto y moderno de ChatOllama.
    """
    # 1. Obtener herramientas
    tools = get_tools()

    # 2. Inicializar el LLM
    # Pedimos texto plano (vacío) en vez de JSON para evitar respuestas serializadas vacías.
    llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, format="")

    # --- LÍNEA CLAVE AÑADIDA ---
    # Vinculamos explícitamente el token de parada de Llama 3 para mejorar la fiabilidad.
    llm_with_stop = llm.bind(stop=["<|eot_id|>"])

    # 3. Crear el prompt
    # Forzar texto plano en la respuesta: evitar JSON o marcas especiales.
    # Si necesitas JSON estructurado en el futuro, vuelve a cambiar `format='json'`
    # y proporciona un esquema explícito en este system message.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente de IA muy útil. Responde las preguntas del usuario en TEXTO PLANO solamente. No devuelvas JSON, diccionarios, ni marcas de código. Ofrece una respuesta concisa y legible."),
        ("user", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ])

    # 4. Vincular las herramientas al LLM que ya tiene el token de parada configurado.
    llm_with_tools = llm_with_stop.bind_tools(tools)

    # 5. Construir la cadena principal del agente usando LCEL.
    # Runnable para loguear la salida del LLM antes del parser
    def log_llm_output(data):
        print("LLM_RAW_OUTPUT:", data)
        return data

    log_llm_runnable = RunnableLambda(log_llm_output)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(x.get("intermediate_steps", [])),
        }
        | prompt
        | llm_with_tools
        | log_llm_runnable
        | OpenAIFunctionsAgentOutputParser()
    )

    # 6. Crear el ejecutor del agente.
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor

def create_agent_executor_old_x_3():
    """
    Crea el ejecutor del agente principal usando el método robusto y moderno de ChatOllama.
    """
    # 1. Obtener herramientas
    tools = get_tools()

    # 2. Inicializar el LLM, usando la clase moderna ChatOllama.
    # Versión alternativa: texto plano (vacío) para mayor fiabilidad
    llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, format="")

    # 3. Crear el prompt (sigue siendo el mismo, simple y efectivo).
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente de IA muy útil. Responde las preguntas del usuario lo mejor que puedas usando las herramientas disponibles."),
        ("user", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ])

    # 4. Vincular las herramientas al LLM.
    llm_with_tools = llm.bind_tools(tools)

    # 5. Construir la cadena principal del agente usando LCEL.
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(x.get("intermediate_steps", [])),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    # 6. Crear el ejecutor del agente.
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor

def create_agent_executor_old_old():
    """
    Crea el ejecutor del agente principal usando el método robusto de Ollama Functions.
    """
    # 1. Obtener herramientas
    tools = get_tools()

    # 2. Inicializar el LLM, usando la clase OllamaFunctions.
    # Esta clase está diseñada para el "tool calling". Le decimos que espere un formato JSON.
    llm = OllamaFunctions(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, format="json")

    # 3. Crear el prompt. Es mucho más simple para este tipo de agente.
    # No necesitamos darle ejemplos complicados de "Pensamiento/Acción".
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente de IA muy útil. Responde las preguntas del usuario lo mejor que puedas usando las herramientas disponibles."),
        ("user", "{input}"),
        # La variable "agent_scratchpad" es crucial.
        # Contiene los pasos intermedios de pensamiento y llamadas a herramientas.
        ("ai", "{agent_scratchpad}"),
    ])

    # 4. Vincular las herramientas al LLM.
    # Esto le permite al LLM saber qué "funciones" puede llamar.
    llm_with_tools = llm.bind_tools(tools)

    # 5. Construir la cadena principal del agente usando LCEL (LangChain Expression Language)
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(x.get("intermediate_steps", [])),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    # 6. Crear el ejecutor del agente.
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor

def create_agent_executor_():
    """
    Crea el ejecutor del agente principal, combinando el LLM, las herramientas y el prompt.
    """
    # 1. Cargar el prompt desde el archivo
    with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        prompt_template_str = f.read()
    prompt = PromptTemplate.from_template(prompt_template_str)

    # 2. Inicializar el LLM
    llm = Ollama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)

    # 3. Obtener herramientas y memoria
    tools = get_tools()
    memory = get_memory()

    # 4. Crear el agente usando la función de LangChain
    agent = create_react_agent(llm, tools, prompt)

    # 5. Crear el ejecutor del agente
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors="Por favor, reformula tu respuesta para seguir el formato requerido.",
        max_iterations=5
    )

    return agent_executor
