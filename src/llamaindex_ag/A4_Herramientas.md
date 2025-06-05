# Usando Herramientas en LlamaIndex

Definir un conjunto claro de Herramientas es crucial para el rendimiento. Como discutimos en la first_agent y smolagent_ag, las interfaces de herramientas claras son más fáciles de usar para los LLMs. Al igual que una interfaz de API de software para ingenieros humanos, pueden sacar más provecho de la herramienta si es fácil entender cómo funciona.

Hay cuatro tipos principales de herramientas en LlamaIndex:

## Herramientas

- **FunctionTool**: Convierte cualquier función de Python en una herramienta que un agente puede usar. Automáticamente descifra cómo funciona la función.
- **QueryEngineTool**: Una herramienta que permite a los agentes usar motores de consulta. Dado que los agentes están construidos sobre motores de consulta, también pueden usar otros agentes como herramientas.
- **Toolspecs**: Conjuntos de herramientas creadas por la comunidad, que a menudo incluyen herramientas para servicios específicos como Gmail.
- **Utility Tools**: Herramientas especiales que ayudan a manejar grandes cantidades de datos de otras herramientas.

Revisaremos cada una de ellas en más detalle a continuación.

## Creando un FunctionTool

Puedes seguir el código en este notebook que puedes ejecutar usando Google Colab.

Un FunctionTool proporciona una forma simple de envolver cualquier función de Python y hacerla disponible para un agente. Puedes pasar una función síncrona o asíncrona a la herramienta, junto con parámetros opcionales de nombre y descripción. El nombre y la descripción son particularmente importantes ya que ayudan al agente a entender cuándo y cómo usar la herramienta de manera efectiva. Veamos cómo crear un FunctionTool a continuación y luego llamarlo.

```python
from llama_index.core.tools import FunctionTool

def get_weather(location: str) -> str:
    """Útil para obtener el clima de una ubicación dada."""
    print(f"Obteniendo clima para {location}")
    return f"El clima en {location} es soleado"

tool = FunctionTool.from_defaults(
    get_weather,
    name="my_weather_tool",
    description="Útil para obtener el clima de una ubicación dada.",
)
tool.call("New York")
```

> **Nota**: Al usar un agente o LLM con llamadas de función, la herramienta seleccionada (y los argumentos escritos para esa herramienta) dependen fuertemente del nombre de la herramienta y la descripción del propósito y argumentos de la herramienta. Aprende más sobre llamadas de función en la [Guía de Llamadas de Función](https://docs.llamaindex.ai/en/stable/examples/workflow/function_calling_agent/).

## Creando un QueryEngineTool

El QueryEngine que definimos en la unidad anterior puede ser fácilmente transformado en una herramienta usando la clase QueryEngineTool. Veamos cómo crear un QueryEngineTool a partir de un QueryEngine en el ejemplo a continuación.

```python
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

embed_model = HuggingFaceEmbedding("BAAI/bge-small-en-v1.5")

db = chromadb.PersistentClient(path="./alfred_chroma_db")
chroma_collection = db.get_or_create_collection("alfred")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

llm = HuggingFaceInferenceAPI(model_name="Qwen/Qwen2.5-Coder-32B-Instruct")
query_engine = index.as_query_engine(llm=llm)
tool = QueryEngineTool.from_defaults(query_engine, name="algún nombre útil", description="alguna descripción útil")
```

## Creando Toolspecs

Piensa en los `ToolSpecs` como colecciones de herramientas que trabajan juntas armoniosamente - como un kit de herramientas profesional bien organizado. Así como el kit de herramientas de un mecánico contiene herramientas complementarias que trabajan juntas para reparaciones de vehículos, un `ToolSpec` combina herramientas relacionadas para propósitos específicos. Por ejemplo, el ToolSpec de un agente contable podría integrar elegantemente capacidades de hojas de cálculo, funcionalidad de correo electrónico y herramientas de cálculo para manejar tareas financieras con precisión y eficiencia.

### Instalar el Toolspec de Google

Y ahora podemos cargar el toolspec y convertirlo en una lista de herramientas.

```python
from llama_index.tools.google import GmailToolSpec

tool_spec = GmailToolSpec()
tool_spec_list = tool_spec.to_tool_list()
```

Para obtener una vista más detallada de las herramientas, podemos echar un vistazo a los metadatos de cada herramienta.

```python
[(tool.metadata.name, tool.metadata.description) for tool in tool_spec_list]
```

## Protocolo de Contexto de Modelo (MCP) en LlamaIndex

LlamaIndex también permite usar herramientas MCP a través de un ToolSpec en el [LlamaHub](https://llamahub.ai/l/tools/llama-index-tools-mcp). Simplemente puedes ejecutar un servidor MCP y comenzar a usarlo a través de la siguiente implementación.


### Instalar el Toolspec MCP

Como se introdujo en la sección sobre LlamaHub, podemos instalar el toolspec MCP con el siguiente comando:

```bash
pip install llama-index-tools-mcp
```

```python
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

# Consideramos que hay un servidor mcp ejecutándose en 127.0.0.1:8000, o puedes usar el cliente mcp para conectarte a tu propio servidor mcp.
mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
mcp_tool = McpToolSpec(client=mcp_client)

# obtener el agente
agent = await get_agent(mcp_tool)

# crear el contexto del agente
agent_context = Context(agent)
```

## Herramientas de Utilidad

A menudo, consultar directamente una API puede devolver una cantidad excesiva de datos, algunos de los cuales pueden ser irrelevantes, desbordar la ventana de contexto del LLM, o aumentar innecesariamente el número de tokens que estás usando. Veamos nuestras dos principales herramientas de utilidad a continuación.

- **OnDemandToolLoader**: Esta herramienta convierte cualquier cargador de datos existente de LlamaIndex (clase `BaseReader`) en una herramienta que un agente puede usar. La herramienta puede ser llamada con todos los parámetros necesarios para activar load_data del cargador de datos, junto con una cadena de consulta en lenguaje natural. Durante la ejecución, primero cargamos datos del cargador de datos, los indexamos (por ejemplo, con un almacén vectorial), y luego los consultamos 'bajo demanda'. Los tres pasos ocurren en una sola llamada de herramienta.

- **LoadAndSearchToolSpec**: El `LoadAndSearchToolSpec` toma cualquier Herramienta existente como entrada. Como un tool spec, implementa `to_tool_list`, y cuando esa función es llamada, se devuelven dos herramientas: una herramienta de carga y luego una herramienta de búsqueda. La ejecución de la herramienta de carga llamaría a la Herramienta subyacente, y luego indexaría la salida (por defecto con un índice vectorial). La ejecución de la herramienta de búsqueda tomaría una cadena de consulta como entrada y llamaría al índice subyacente.

## Recursos

Puedes encontrar toolspecs y herramientas de utilidad en el [LlamaHub](https://llamahub.ai/).

¡Ahora que entendemos los conceptos básicos de agentes y herramientas en LlamaIndex, veamos cómo podemos usar LlamaIndex para crear flujos de trabajo configurables y manejables!
