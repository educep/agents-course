# Standard imports
import asyncio

# Third party imports
import chromadb
import nest_asyncio
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
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

# Usaremos as_query_engine por ahora.

nest_asyncio.apply()  # Esto es necesario para ejecutar el query engine
llm = HuggingFaceInferenceAPI(model_name="Qwen/Qwen2.5-Coder-32B-Instruct")
query_engine = index.as_query_engine(
    llm=llm,
    response_mode="tree_summarize",
)
response = query_engine.query(
    "Respond using a persona that describes author and travel experiences?"
)


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
response_open_ai = query_engine.query(
    "Respond using a persona that describes author and travel experiences?"
)

response  # Qwen, via HuggingFaceInferenceAPI
"""
Response(response='An anthropologist or cultural expert with a deep dive into
Cypriot culture, history, and society, having spent significant time researching
and living in Cyprus to understand its people, customs, and way of life.',
source_nodes=[NodeWithScore(node=TextNode(id_='8dbe5dfe-c57e-489f-91b1-9542824cebb3', embedding=None,
metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1.txt',
'file_name': 'persona_1.txt', 'file_type': 'text/plain', 'file_size': 266, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'},
excluded_embed_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'],
excluded_llm_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'],
relationships={<NodeRelationship.SOURCE: '1'>: RelatedNodeInfo(node_id='7ee41083-0061-4749-94e9-e9a28662576d', node_type='4',
metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1.txt',
'file_name': 'persona_1.txt', 'file_type': 'text/plain', 'file_size': 266, 'creation_date': '2025-06-05', 'last_modified_date':
'2025-06-05'}, hash='8f3342504dc60aee6af0aa576451ee2b33cfd9cde97ccca25884afec41d77d05')}, metadata_template='{key}: {value}',
metadata_separator='\n', text='An anthropologist or a cultural expert interested in the intricacies of Cypriot culture, history,
and society, particularly someone who has spent considerable time researching and living in Cyprus to gain a deep understanding
of its people, customs, and way of life.', mimetype='text/plain', start_char_idx=0, end_char_idx=266, metadata_seperator='\n',
text_template='{metadata_str}\n\n{content}'), score=0.5065240613865369),
NodeWithScore(node=TextNode(id_='35d2e2e7-58ac-436a-9873-9828cfc2ebaf', embedding=None,
metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1004.txt',
'file_name': 'persona_1004.txt', 'file_type': 'text/plain', 'file_size': 160, 'creation_datn_date', 'last_modified_date',
'last_accessed_date'], excluded_llm_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date',
'last_accessed_date'], relationships={<NodeRelationship.SOURCE: '1'>:
RelatedNodeInfo(node_id='0b085808-dbed-4a59-80af-5d2c61c194d3', node_type='4',
metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1004.txt',
'file_name': 'persona_1004.txt', 'file_type': 'text/plain', 'file_size': 160, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'}, hash='6ceba78ab268f6e0ce6995eded7fb2d16e6084530eebf9357d61f0604e5afe0a')},
metadata_template='{key}: {value}', metadata_separator='\n', text='An environmental historian or urban planner
focused on ecological conservation and sustainability, likely working in local government or a related organization.',
mimetype='text/plain', start_char_idx=0, end_char_idx=160, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'),
score=0.48230491686949534)], metadata={'8dbe5dfe-c57e-489f-91b1-9542824cebb3':
{'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1.txt',
'file_name': 'persona_1.txt', 'file_type': 'text/plain', 'file_size': 266, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'}, '35d2e2e7-58ac-436a-9873-9828cfc2ebaf':
{'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1004.txt',
'file_name': 'persona_1004.txt', 'file_type': 'text/plain', 'file_size': 160, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'}})
"""

response_open_ai
"""
Response(response='The author is an anthropologist with extensive travel experiences in Cyprus.
They have immersed themselves in the local culture, history, and society, allowing for a profound understanding
of the Cypriot way of life. This journey has not only enriched their knowledge but also deepened their
appreciation for the customs and traditions of the island. Their insights are informed by both academic
research and personal interactions with the local community, making their narrative both informative and relatable.',
source_nodes=[NodeWithScore(node=TextNode(id_='8dbe5dfe-c57e-489f-91b1-9542824cebb3', embedding=None,
metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1.txt',
'file_name': 'persona_1.txt', 'file_type': 'text/plain', 'file_size': 266, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'}, excluded_embed_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date',
'last_modified_date', 'last_accessed_date'], excluded_llm_metadata_keys=['file_name', 'file_type', 'file_size',
'creation_date', 'last_modified_date', 'last_accessed_date'],
relationships={<NodeRelationship.SOURCE: '1'>: RelatedNodeInfo(node_id='7ee41083-0061-4749-94e9-e9a28662576d',
node_type='4', metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1.txt',
'file_name': 'persona_1.txt', 'file_type': 'text/plain', 'file_size': 266, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'}, hash='8f3342504dc60aee6af0aa576451ee2b33cfd9cde97ccca25884afec41d77d05')},
metadata_template='{key}: {value}', metadata_separator='\n', text='An anthropologist or a cultural expert interested
in the intricacies of Cypriot culture, history, and society, particularly someone who has spent considerable time
researching and living in Cyprus to gain a deep understanding of its people, customs, and way of life.',
mimetype='text/plain', start_char_idx=0, end_char_idx=266, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'),
score=0.5065240613865369), NodeWithScore(node=TextNode(id_='35d2e2e7-58ac-436a-9873-9828cfc2ebaf', embedding=None,
metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1004.txt',
'file_name': 'persona_1004.txt', 'file_type': 'text/plain', 'file_size': 160, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'}, excluded_embed_metadata_keys=['file_name', 'file_type', 'file_size',
'creation_date', 'last_modified_date', 'last_accessed_date'], excluded_llm_metadata_keys=['file_name', 'file_type',
'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'],
relationships={<NodeRelationship.SOURCE: '1'>: RelatedNodeInfo(node_id='0b085808-dbed-4a59-80af-5d2c61c194d3', node_type='4',
metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1004.txt',
'file_name': 'persona_1004.txt', 'file_type': 'text/plain', 'file_size': 160, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'}, hash='6ceba78ab268f6e0ce6995eded7fb2d16e6084530eebf9357d61f0604e5afe0a')},
metadata_template='{key}: {value}', metadata_separator='\n', text='An environmental historian or urban planner focused on
ecological conservation and sustainability, likely working in local government or a related organization.',
mimetype='text/plain', start_char_idx=0, end_char_idx=160, me686949534)],
metadata={'8dbe5dfe-c57e-489f-91b1-9542824cebb3': {'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1.txt',
'file_name': 'persona_1.txt', 'file_type': 'text/plain', 'file_size': 266, 'creation_date': '2025-06-05',
'last_modified_date': '2025-06-05'}, '35d2e2e7-58ac-436a-9873-9828cfc2ebaf':
{'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_1004.txt',
'file_name': 'persona_1004.txt', 'file_type': 'text/plain', 'file_size': 160, 'creation_date': '2025-06-05', 'last_modified_date': '2025-06-05'}})
"""

"""
response = query_engine.query(
    "Respond using a persona that describes author and travel experiences?"
)
Esto se obtiene si usamos el query_engine.query() con open_ai
Response(response="As an author with a deep passion for travel, I have always believed that the world
is an open book, waiting to be explored, filled with stories just waiting to be told. My journey began
in the quaint streets of Paris, where I first discovered the magic of writing in a bustling café,
sipping espresso while the world rushed by. The vibrant culture and rich history inspired me to weave
tales that reflect the beauty of human experiences.\n\nTravel has taken me to the sun-kissed beaches of
Bali, where I found tranquility and inspiration among the lush landscapes. Each destination has gifted
me with unique characters and narratives, from the bustling markets of Marrakech to the serene temples of
Kyoto. I often immerse myself in local traditions, capturing the essence of each place through my writing.
\n\nNavigating through foreign citth locals or wandering through ancient ruins, every experience becomes a
thread in the tapestry of my stories.\n\nThrough my writing, I aim to transport readers to the far corners
of the earth, allowing them to experience the sights, sounds, and emotions that I have felt. Each book is
not just a collection of words, but a passport to adventure, encouraging others to embark on their own
journeys and discover the stories that await them.", source_nodes=[], metadata=None)
"""
