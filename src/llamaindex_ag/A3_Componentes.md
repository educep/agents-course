# Componentes en LlamaIndex

## ¿Qué son los componentes en LlamaIndex?

¿Recuerdas nuestro primer agente, nuestro útil agente mayordomo Alfred de `agent_2_toolcalling.py`? Para ayudarnos de manera efectiva, Alfred necesita entender nuestras solicitudes y preparar, encontrar y usar información relevante para ayudar a completar tareas. Aquí es donde entran los componentes de LlamaIndex.

Aunque LlamaIndex tiene muchos componentes, nos enfocaremos específicamente en el componente **QueryEngine**. ¿Por qué? Porque puede usarse como una herramienta de Generación Aumentada por Recuperación (RAG) para un agente.

Entonces, ¿qué es RAG? Los LLMs están entrenados en enormes cantidades de datos para aprender conocimiento general. Sin embargo, es posible que no estén entrenados en datos relevantes y actualizados. RAG resuelve este problema encontrando y recuperando información relevante de tus datos y dándosela al LLM.

Ahora, piensa en cómo funciona Alfred:

1. Le pides a Alfred que ayude a planear una cena
2. Alfred necesita revisar tu calendario, preferencias dietéticas y menús exitosos del pasado
3. El QueryEngine ayuda a Alfred a encontrar esta información y usarla para planear la cena

Esto hace que el QueryEngine sea un componente clave para construir flujos de trabajo RAG agénticos en LlamaIndex. Así como Alfred necesita buscar a través de la información de tu hogar para ser útil, cualquier agente necesita una forma de encontrar y entender datos relevantes. El QueryEngine proporciona exactamente esta capacidad.

## Creando un pipeline RAG usando componentes

Hay cinco etapas clave dentro de RAG, que a su vez serán parte de la mayoría de aplicaciones más grandes que construyas. Estas son:

**Carga (Loading)**: se refiere a obtener tus datos de donde viven — ya sean archivos de texto, PDFs, otro sitio web, una base de datos o una API — en tu flujo de trabajo. [LlamaHub](https://docs.llamaindex.ai/en/stable/module_guides/loading/connector/) proporciona cientos de integraciones para elegir.

**Indexación (Indexing)**: significa crear una estructura de datos que permita consultar los datos. Para LLMs, esto casi siempre significa crear embeddings vectoriales, que son representaciones numéricas del significado de los datos. La indexación también puede referirse a numerosas otras estrategias de metadatos para facilitar el encontrar datos contextualmente relevantes basados en propiedades.

**Almacenamiento (Storing)**: una vez que tus datos están indexados, querrás almacenar tu índice, así como otros metadatos, para evitar tener que reindexar.

**Consulta (Querying)**: para cualquier estrategia de indexación dada, hay muchas formas en que puedes utilizar LLMs y estructuras de datos de LlamaIndex para consultar, incluyendo subconsultas, consultas de múltiples pasos y estrategias híbridas.

**Evaluación (Evaluation)**: un paso crítico en cualquier flujo es verificar qué tan efectivo es en relación a otras estrategias, o cuando haces cambios. La evaluación proporciona medidas objetivas de qué tan precisas, fieles y rápidas son tus respuestas a las consultas.

A continuación, veamos cómo podemos reproducir estas etapas usando componentes.

## Cargando y embebiendo documentos

Como se mencionó antes, LlamaIndex puede trabajar sobre tus propios datos, sin embargo, antes de acceder a los datos, necesitamos cargarlos. Hay tres formas principales de cargar datos en LlamaIndex:

**SimpleDirectoryReader**: Un cargador incorporado para varios tipos de archivos desde un directorio local.

**LlamaParse**: [LlamaParse](https://github.com/run-llama/llama_cloud_services/blob/main/parse.md), la herramienta oficial de LlamaIndex para análisis de PDF, disponible como una API administrada.

**LlamaHub**: Un registro de cientos de bibliotecas de carga de datos para ingerir datos desde cualquier fuente.

```python
# [ver código en .py]
```

Después de cargar nuestros documentos, necesitamos dividirlos en piezas más pequeñas llamadas objetos Node. Un Node es simplemente un fragmento de texto del documento original que es más fácil de manejar para la IA, mientras aún mantiene referencias al objeto Document original.

El **IngestionPipeline** nos ayuda a crear estos nodos a través de dos transformaciones clave:

**SentenceSplitter** divide los documentos en fragmentos manejables dividiéndolos en límites naturales de oraciones.

**HuggingFaceEmbedding** convierte cada fragmento en embeddings numéricos - representaciones vectoriales que capturan el significado semántico de una manera que la IA puede procesar eficientemente.

Este proceso nos ayuda a organizar nuestros documentos de una manera que es más útil para búsquedas y análisis.

## Almacenando e indexando documentos

Después de crear nuestros objetos Node necesitamos indexarlos para hacerlos búsquedas, pero antes de que podamos hacer eso, necesitamos un lugar para almacenar nuestros datos.

Como estamos usando un pipeline de ingesta, podemos adjuntar directamente un vector store al pipeline para poblarlo. En este caso, usaremos Chroma para almacenar nuestros documentos.

Una descripción general de los diferentes vector stores se puede encontrar en la [documentación de LlamaIndex](https://docs.llamaindex.ai/en/stable/module_guides/storing/vector_stores/).

Aquí es donde entran los embeddings vectoriales - al embeber tanto la consulta como los nodos en el mismo espacio vectorial, podemos encontrar coincidencias relevantes. El **VectorStoreIndex** maneja esto por nosotros, usando el mismo modelo de embedding que usamos durante la ingesta para asegurar consistencia.

Toda la información se persiste automáticamente dentro del objeto ChromaVectorStore y la ruta del directorio pasada.

¡Excelente! Ahora que podemos guardar y cargar nuestro índice fácilmente, exploremos cómo consultarlo de diferentes maneras.

## Consultando un VectorStoreIndex con prompts y LLMs

Antes de que podamos consultar nuestro índice, necesitamos convertirlo a una interfaz de consulta. Las opciones de conversión más comunes son:

**as_retriever**: Para recuperación básica de documentos, devolviendo una lista de objetos NodeWithScore con puntuaciones de similitud

**as_query_engine**: Para interacciones de pregunta-respuesta única, devolviendo una respuesta escrita

**as_chat_engine**: Para interacciones conversacionales que mantienen memoria a través de múltiples mensajes, devolviendo una respuesta escrita usando historial de chat y contexto indexado

## Procesamiento de Respuestas

Bajo el capó, el query engine no solo usa el LLM para responder la pregunta sino que también usa un **ResponseSynthesizer** como estrategia para procesar la respuesta. Una vez más, esto es completamente personalizable pero hay tres estrategias principales que funcionan bien desde el inicio:

**refine**: crear y refinar una respuesta yendo secuencialmente a través de cada fragmento de texto recuperado. Esto hace una llamada LLM separada por Node/fragmento recuperado.

**compact** (predeterminado): similar a refinar pero concatenando los fragmentos de antemano, resultando en menos llamadas LLM.

**tree_summarize**: crear una respuesta detallada yendo a través de cada fragmento de texto recuperado y creando una estructura de árbol de la respuesta.

Toma control de grano fino de tus flujos de trabajo de consulta con la [API de composición de bajo nivel](https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/usage_pattern/#low-level-composition-api). Esta API te permite personalizar y ajustar finamente cada paso del proceso de consulta para que coincida con tus necesidades exactas, lo que también se combina genial con [Workflows](https://docs.llamaindex.ai/en/stable/module_guides/workflow/).

El modelo de lenguaje no siempre funcionará de maneras predecibles, así que no podemos estar seguros de que la respuesta que obtenemos siempre sea correcta. Podemos lidiar con esto evaluando la calidad de la respuesta.

## Evaluación y observabilidad

LlamaIndex proporciona herramientas de evaluación incorporadas para evaluar la calidad de las respuestas. Estos evaluadores aprovechan LLMs para analizar respuestas a través de diferentes dimensiones. Veamos los tres evaluadores principales disponibles:

**FaithfulnessEvaluator**: Evalúa la fidelidad de la respuesta verificando si la respuesta está respaldada por el contexto.

**AnswerRelevancyEvaluator**: Evalúa la relevancia de la respuesta verificando si la respuesta es relevante a la pregunta.

**CorrectnessEvaluator**: Evalúa la corrección de la respuesta verificando si la respuesta es correcta.

### Implementando Evaluación de Fidelidad

Ahora podemos verificar si la consulta es fiel a la persona original usando el `FaithfulnessEvaluator`:

```python
from llama_index.core.evaluation import FaithfulnessEvaluator

# consultar el índice
evaluator = FaithfulnessEvaluator(llm=llm)
eval_result = evaluator.evaluate_response(response=response)
print(f"Resultado de evaluación de fidelidad: {eval_result.passing}")
# True
```

### Observabilidad Avanzada con Arize Phoenix

Si uno de estos evaluadores basados en LLM no proporciona suficiente contexto, podemos verificar la respuesta usando la herramienta **Arize Phoenix**, después de crear una cuenta en [LlamaTrace](https://llamatrace.com) y generar una clave API.

```python
import llama_index
import os

# Configuración de Phoenix (requiere clave API)
PHOENIX_API_KEY = "<TU_PHOENIX_API_KEY>"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
llama_index.core.set_global_handler(
    "arize_phoenix", endpoint="https://llamatrace.com/v1/traces"
)

# Ahora podemos consultar el índice y ver la respuesta en la herramienta Arize Phoenix
response = query_engine.query(
    "What is the name of the someone that is interested in AI and technology?"
)
print(response)
```

### Beneficios de la Observabilidad

**Trazabilidad completa**: Phoenix te permite rastrear cada consulta, desde la entrada hasta la respuesta final, incluyendo:
- Los documentos recuperados
- Las puntuaciones de similitud
- Los prompts utilizados
- Las respuestas del LLM

**Debugging visual**: Interfaz gráfica para entender el flujo de datos y identificar cuellos de botella o problemas en el pipeline RAG.

**Métricas en tiempo real**: Monitoreo continuo del rendimiento de tu sistema de consultas.

Incluso sin evaluación directa, podemos obtener perspectivas sobre cómo está funcionando nuestro sistema a través de la observabilidad. Esto es especialmente útil cuando estamos construyendo flujos de trabajo más complejos y queremos entender cómo está funcionando cada componente.

¿Quieres aprender más sobre componentes y cómo usarlos? Continúa tu viaje con las [Guías de Componentes](https://docs.llamaindex.ai/en/stable/module_guides/) o la [Guía sobre RAG](https://docs.llamaindex.ai/en/stable/understanding/rag/).

Hemos visto cómo usar componentes para crear un QueryEngine. ¡Ahora, veamos cómo podemos usar el QueryEngine como una herramienta para un agente!
