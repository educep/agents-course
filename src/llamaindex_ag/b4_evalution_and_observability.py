# Evaluación y observabilidad
# LlamaIndex proporciona herramientas de evaluación integradas para evaluar la calidad de las respuestas.
# Estos evaluadores utilizan LLMs para analizar las respuestas en diferentes dimensiones.
# Ahora podemos verificar si la consulta es fiel a la persona original.

# Standard imports
import asyncio

# Third party imports
import chromadb
import nest_asyncio
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.evaluation import FaithfulnessEvaluator
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore

# Internal imports
from config.settings import settings
from src.llamaindex_ag.b1_load_local_sets import load_local_sets, this_path

# ---------  Cargamos los documentos de las personas ---------
load_local_sets()
reader = SimpleDirectoryReader(input_dir=this_path)
documents = reader.load_data()
len(documents)

# Después de crear nuestros objetos Node, necesitamos indexarlos para que sean buscables,
# pero antes de poder hacer eso, necesitamos un lugar para almacenar nuestros datos.
# Podemos conectar directamente un vector store al pipeline para poblarlo. En este caso,
# usaremos Chroma para almacenar nuestros documentos. Ejecutemos el pipeline nuevamente
# con el vector store conectado.
chroma_path = this_path / "alfred_chroma_db"
chroma_path.mkdir(parents=True, exist_ok=True)
db = chromadb.PersistentClient(path=str(chroma_path))
chroma_collection = db.get_or_create_collection(name="alfred")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

pipeline = IngestionPipeline(
    transformations=[SentenceSplitter(), embed_model],
    vector_store=vector_store,
)


async def process_documents():
    """Process documents asynchronously."""
    # run the pipeline async
    nodes = await pipeline.arun(documents=documents[:10])
    return nodes


nodes = asyncio.run(process_documents())
len(nodes)
# > 10

# Ahora podemos crear un VectorStoreIndex a partir del vector store y usarlo para
# consultar los documentos pasando el vector store y el modelo de embedding a la
# función from_vector_store().

index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)

# Consulta al index : Ahora que tenemos nuestro index, podemos usarlo para consultar
# los documentos. Vamos a crear un QueryEngine a partir del index y usarlo para
# consultar los documentos usando un modo de respuesta específico.

# Recuerda que: antes de poder consultar nuestro index, necesitamos convertirlo en una interfaz de consulta.
# Las opciones más comunes de conversión son:
# as_retriever:    Para búsqueda de documentos básica, devolviendo una lista de objetos NodeWithScore
#                  con puntuaciones de similitud
# as_query_engine: Para interacciones de pregunta-respuesta individuales, devolviendo una respuesta escrita
# as_chat_engine:  Para interacciones conversacionales que mantienen memoria entre múltiples mensajes,
#                  devolviendo una respuesta escrita usando el historial de chat y el contexto indexado

# Usaremos as_chat_engine por ahora.

nest_asyncio.apply()  # Esto es necesario para ejecutar el query engine
llm = OpenAI(
    model="gpt-4o-mini",  # o "gpt-4o", "gpt-3.5-turbo"
    api_key=settings.open_api_key,  # Usa tu clave desde settings
    temperature=0.7,
    max_tokens=1500,
)
query_engine = index.as_query_engine(
    llm=llm,
    response_mode="tree_summarize",
)
response = query_engine.query(
    "Respond using a persona that describes author and travel experiences?"
)

# Consultar el index
evaluator = FaithfulnessEvaluator(llm=llm)
eval_result = evaluator.evaluate_response(response=response)
eval_result.passing

# ----------- COMPARACIÓN: Query Engine vs Chat Engine -----------

print("=== TESTING QUERY ENGINE ===")
query_engine = index.as_query_engine(
    llm=llm,
    response_mode="tree_summarize",
)
query_response = query_engine.query(
    "Respond using a persona that describes author and travel experiences?"
)

print(f"Query Engine Response:\n{query_response.response}\n")
print(f"Source Nodes: {len(query_response.source_nodes)}")

# Evaluar query engine
query_eval_result = evaluator.evaluate_response(response=query_response)
print(f"Query Engine - Faithfulness Passing: {query_eval_result.passing}")
print(f"Query Engine - Faithfulness Score: {query_eval_result.score}")
print(f"Query Engine - Feedback: {query_eval_result.feedback}\n")

print("=== TESTING CHAT ENGINE ===")
chat_engine = index.as_chat_engine(
    llm=llm,
    chat_mode="condense_question",  # Explicitly set chat mode
)
chat_response = chat_engine.chat(
    "Respond using a persona that describes author and travel experiences?"
)

print(f"Chat Engine Response:\n{chat_response.response}\n")
print(f"Source Nodes: {len(chat_response.source_nodes)}")

# Evaluar chat engine
chat_eval_result = evaluator.evaluate_response(response=chat_response)
print(f"Chat Engine - Fidelidad Aprobada: {chat_eval_result.passing}")
print(f"Chat Engine - Puntuación Fidelidad: {chat_eval_result.score}")
print(f"Chat Engine - Retroalimentación: {chat_eval_result.feedback}\n")

# Comparar respuestas
print("=== COMPARACIÓN DE RESPUESTAS ===")
print(f"Longitud respuesta query: {len(query_response.response)}")
print(f"Longitud respuesta chat: {len(chat_response.response)}")
print(
    f"Las respuestas son similares: {query_response.response[:100] == chat_response.response[:100]}"
)

# Analizar las diferencias en detalle
print("=== ANÁLISIS DETALLADO ===")
print("Estructura de Respuesta Query Engine:")
print(f"- Tipo: {type(query_response)}")
print(
    f"- Atributos disponibles: {[attr for attr in dir(query_response) if not attr.startswith('_')]}"
)

print("\nEstructura de Respuesta Chat Engine:")
print(f"- Tipo: {type(chat_response)}")
print(
    f"- Atributos disponibles: {[attr for attr in dir(chat_response) if not attr.startswith('_')]}"
)

# Verificar si hay diferencias en los nodos fuente
print("\nComparación de nodos fuente:")
if hasattr(query_response, "source_nodes") and hasattr(chat_response, "source_nodes"):
    query_sources = [node.node.text[:100] for node in query_response.source_nodes]
    chat_sources = [node.node.text[:100] for node in chat_response.source_nodes]
    print(f"Los nodos fuente de query coinciden con los de chat: {query_sources == chat_sources}")

# ----------- EVALUACIÓN Y OBSERVABILIDAD ADICIONAL -----------

# Si uno de estos evaluadores basados en LLM no proporciona suficiente contexto,
# podemos verificar la respuesta usando la herramienta Arize Phoenix,
# después de crear una cuenta en LlamaTrace y generar una clave API.

# import llama_index
# import os

# Nota: Descomenta las siguientes líneas si tienes una clave API de Phoenix
# PHOENIX_API_KEY = "<PHOENIX_API_KEY>"
# os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
# llama_index.core.set_global_handler(
#     "arize_phoenix", endpoint="https://llamatrace.com/v1/traces"
# )

# Ahora podemos consultar el índice y ver la respuesta en la herramienta Arize Phoenix.

# response = query_engine.query(
#     "What is the name of the someone that is interested in AI and techhnology?"
# )
# response

print(
    "Configuración de observabilidad completada. Para usar Phoenix, descomenta las líneas anteriores con tu clave API."
)
