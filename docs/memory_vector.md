# Memoria vectorial (Chroma) — Ejemplo

Esta página muestra cómo configurar memoria vectorial usando Chroma y embeddings.

Requisitos:
- Instalar `chromadb` y un paquete de embeddings (por ejemplo `sentence-transformers` o usar OpenAI).

Instalación (opciones):

```bash
pip install chromadb sentence-transformers
# o si usas OpenAI embeddings:
# pip install openai
```

Ejemplo local con HuggingFace (sin depender de API externa):

```python
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import Chroma
from agent.memory import get_memory

# Crea el embedding local (puede requerir GPU/CPU y dependencias pesadas)
emb = HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-large')

# Crea/abre la base de vectores en persistencia local
vectorstore = Chroma(persist_directory='./chroma_db', embedding_function=emb)

# Crea la memoria basada en vectorstore
memory = get_memory('vector', vectorstore=vectorstore)
```

Ejemplo usando OpenAIEmbeddings (requiere `OPENAI_API_KEY`):

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from agent.memory import get_memory

emb = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory='./chroma_db', embedding_function=emb)
memory = get_memory('vector', vectorstore=vectorstore)
```

Integración con el agente:

```python
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)
```

Notas:
- La factory `get_memory('vector', ...)` acepta un `vectorstore` ya inicializado o creará un `Chroma` a partir de `embedding` + `persist_dir` si los pasas.
- Si usas `MEMORY_TYPE='vector'` en variables de entorno, asegúrate de inicializar embeddings/vectorstore antes (o modificar `agent_builder.py` para que lo haga automáticamente).