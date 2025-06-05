# Standard library imports

import chromadb

# Third party imports
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.tools.google import GmailToolSpec
from llama_index.vector_stores.chroma import ChromaVectorStore

# Internal imports
from config.settings import settings
from src.llamaindex_ag.b1_load_local_sets import load_local_sets, this_path

# ---------  Cargamos los documentos de las personas ---------
load_local_sets()


# ---------  Creamos una FunctionTool  ---------
# Vamos a crear una FunctionTool y la llamamos.
def get_weather(location: str) -> str:
    """Useful for getting the weather for a given location."""
    print(f"Getting weather for {location}")
    return f"The weather in {location} is sunny"


tool = FunctionTool.from_defaults(
    get_weather,
    name="my_weather_tool",
    description="Useful for getting the weather for a given location.",
)
tool.call("New York")


# ---------  Creamos un QueryEngineTool  ---------
# Vamos a reutilizar el QueryEngine que definimos en la unidad anterior
# sobre herramientas y lo convertimos en un QueryEngineTool
chroma_path = this_path / "alfred_chroma_db"
chroma_path.mkdir(parents=True, exist_ok=True)
db = chromadb.PersistentClient(path=str(chroma_path))
chroma_collection = db.get_or_create_collection(name="alfred")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)
llm = OpenAI(
    model="gpt-4o-mini",  # o "gpt-4o", "gpt-3.5-turbo"
    api_key=settings.open_api_key,  # Usa tu clave desde settings
    temperature=0.7,
    max_tokens=1500,
)
query_engine = index.as_query_engine(llm=llm)
tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="persona_finder",
    description="Useful for finding a persona that describes author and experiences",
)


response = tool.call(
    "Responds about research on the impact of AI on the future of work and society?"
)

print(response)
# Ver la respuesta recibida en este caso al final del archivo

# ---------  Creamos un ToolSpec  ---------
# Vamos a crear un ToolSpec desde el GmailToolSpec del LlamaHub y lo convertimos en una
# lista de herramientas.


tool_spec = GmailToolSpec()
tool_spec_list = tool_spec.to_tool_list()
[print(tool.metadata.name, tool.metadata.description) for tool in tool_spec_list]


# Model Context Protocol (MCP) en LlamaIndex
# LlamaIndex también permite usar herramientas MCP a través de un ToolSpec en el LlamaHub.
# Simplemente puedes ejecutar un servidor MCP y comenzar a usarlo a través de la siguiente implementación.


# from llama_index.tools.mcp import BasicMCPClient, McpToolSpec


# Consideramos que hay un servidor MCP corriendo en 127.0.0.1:8000,
# o puedes usar el cliente MCP para conectarte a tu propio servidor MCP.
# mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
# mcp_tool = McpToolSpec(client=mcp_client)

# Estos componetes serán vistos en b6_agentes.py
# obtenemos el agente
# agent = await get_agent(mcp_tool)

# creamos el contexto del agente
# agent_context = Context(agent)

# Utility Tools
# Ver la documentation A4_Herramientas.md


"""
QueryEngineTool:
>>> response
ToolOutput(content='The impact of AI on the future of work and society is multifaceted,
influencing various sectors by automating tasks, enhancing productivity, and reshaping
job roles. It raises important considerations regarding equity and inclusivity, as
certain groups may face disproportionate challenges or benefits from these advancements.
Addressing these inequalities is crucial to ensure that the integration of AI fosters a
diverse and equitable workforce, promoting understanding and empathy among all stakeholders involved.',
tool_name='persona_finder', raw_input={'input': 'Responds about research on the impact of AI on the
future of work and society?'}, raw_output=Response(response='The impact of AI on the future of
 work and society is multifaceted, influencing various sectors by automating tasks, enhancing
 productivity, and reshaping job roles. It raises important considerations regarding equity and
 inclusivity, as certain groups may face disproportionate challenges or benefits from these advancements.
 Addressing these inequalities is crucial to ensure that the integration of AI fosters a diverse and
 equitable workforce, promoting understanding and empathy among all stakeholders involved.',
 source_nodes=[NodeWithScore(node=TextNode(id_='89ba8c58-3900-441a-bb3b-0794d416a5f2', embedding=None,
 metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_10.txt',
 'file_name': 'persona_10.txt', 'file_type': 'text/plain', 'file_size': 207, 'creation_date': '2025-06-05',
 'last_modified_date': '2025-06-05'}, excluded_embed_metadata_keys=['file_name', 'file_type', 'file_size',
 'creation_date', 'last_modified_date', 'last_accessed_date'], excluded_llm_metadata_keys=['file_name',
 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'],
 relationships={<NodeRelationship.SOURCE: '1'>: RelatedNodeInfo(node_id='f230324b-541b-46d6-a3ed-9ffc6b77f224',
 node_type='4', metadata={'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaie':
 '2025-06-05', 'last_modified_date': '2025-06-05'}, hash='9496bc039fa731c2d4e6603fa734ed4fd79861f5138970cf9537a7bb71d96516')},
 metadata_template='{key}: {value}', metadata_separator='\n', text='A social justice educator or activist focused on
 diversity, equity, and inclusion, likely working with families and communities to promote empathy and understanding
 of intersectional identity and oppression.', mimetype='text/plain', start_char_idx=0, end_char_idx=207,
 metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), score=0.39394692855109686)],
 metadata={'89ba8c58-3900-441a-bb3b-0794d416a5f2':
 {'file_path': 'C:\\Users\\ecepeda\\PycharmProjects\\agents-course\\src\\llamaindex_ag\\data\\persona_10.txt',
 'file_name': 'persona_10.txt', 'file_type': 'text/plain', 'file_size': 207, 'creation_date': '2025-06-05',
 'last_modified_date': '2025-06-05'}}), is_error=False)
"""
