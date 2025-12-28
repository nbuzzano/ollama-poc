from typing import Any

from langchain_classic.memory.buffer import ConversationBufferMemory

# Import optional memory classes lazily when required
try:
    from langchain_classic.memory.buffer import ConversationBufferWindowMemory
except Exception:  # pragma: no cover - optional dependency
    ConversationBufferWindowMemory = None

try:
    from langchain_classic.memory.summary import ConversationSummaryMemory
except Exception:  # pragma: no cover - optional dependency
    ConversationSummaryMemory = None

try:
    from langchain_classic.memory.combine import CombinedMemory
except Exception:  # pragma: no cover - optional dependency
    CombinedMemory = None


def get_memory(kind: str = "buffer", **kwargs: Any):
    """Factory para crear diferentes tipos de memoria.

    kind: 'buffer' | 'window' | 'summary' | 'combined' | 'vector'

    kwargs soportados (ejemplos):
      - memory_key, return_messages (buffer/window)
      - k (window)
      - llm (summary) -> obligatorio si kind == 'summary'
      - memories (combined) -> lista de objetos de memoria
      - vectorstore / embedding / persist_dir (vector) -> ver nota

    Nota: Las implementaciones vectoriales (Chroma/FAISS) requieren dependencias
    externas y configuración de embeddings; aquí se proporciona un _helper_ que
    intenta dar errores útiles si faltan piezas.
    """
    kind = (kind or "buffer").lower()

    if kind == "buffer":
        return ConversationBufferMemory(
            memory_key=kwargs.get("memory_key", "chat_history"),
            return_messages=kwargs.get("return_messages", True),
        )

    if kind == "window":
        if ConversationBufferWindowMemory is None:
            raise ImportError(
                "ConversationBufferWindowMemory no está disponible. Asegúrate de tener la versión apropiada de langchain_classic."
            )
        return ConversationBufferWindowMemory(
            k=kwargs.get("k", 5),
            memory_key=kwargs.get("memory_key", "chat_history"),
            return_messages=kwargs.get("return_messages", True),
        )

    if kind == "summary":
        if ConversationSummaryMemory is None:
            raise ImportError(
                "ConversationSummaryMemory no está disponible. Asegúrate de tener la versión apropiada de langchain_classic."
            )
        llm = kwargs.get("llm")
        if llm is None:
            raise ValueError("Para 'summary' debes pasar un llm via llm=...")
        return ConversationSummaryMemory(
            llm=llm, memory_key=kwargs.get("memory_key", "chat_history")
        )

    if kind == "combined":
        if CombinedMemory is None:
            raise ImportError(
                "CombinedMemory no está disponible. Asegúrate de tener la versión apropiada de langchain_classic."
            )
        memories = kwargs.get("memories")
        if not memories:
            raise ValueError("Para 'combined' debes pasar una lista 'memories=[...]'")
        return CombinedMemory(memories=memories)

    if kind == "vector":
        # Soporte básico para ayudar al usuario a configurar memoria basada en vectorstore.
        try:
            from langchain.vectorstores import Chroma  # type: ignore
        except Exception as e:  # pragma: no cover - dependencia optional
            raise ImportError(
                "Para usar 'vector' instala chromadb/langchain o configura tu vectorstore."
            ) from e

        vectorstore = kwargs.get("vectorstore")
        if vectorstore is None:
            embedding = kwargs.get("embedding")
            persist_dir = kwargs.get("persist_dir")
            if embedding is None or persist_dir is None:
                raise ValueError(
                    "Para crear memoria 'vector' sin vectorstore, pasa embedding=... y persist_dir=..."
                )
            vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embedding)

        # Intentar localizar una clase VectorStoreRetrieverMemory compatible
        VectorMemClass = None
        for mod in ("langchain_classic.memory.vector", "langchain.memory.vector"):
            try:
                m = __import__(mod, fromlist=["VectorStoreRetrieverMemory"])
                VectorMemClass = getattr(m, "VectorStoreRetrieverMemory")
                break
            except Exception:
                continue
        if VectorMemClass is None:
            raise ImportError(
                "No se encontró VectorStoreRetrieverMemory en langchain. Actualiza/langchain o implementa un wrapper."
            )

        retriever = vectorstore.as_retriever(search_kwargs=kwargs.get("search_kwargs", {}))
        return VectorMemClass(retriever=retriever, memory_key=kwargs.get("memory_key", "chat_history"))

    raise ValueError(f"Tipo de memoria no soportado: {kind}")
