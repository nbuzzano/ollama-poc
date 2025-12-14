from langchain_classic.memory.buffer import ConversationBufferMemory

def get_memory():
    """Crea y devuelve un objeto de memoria para el agente."""
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)
