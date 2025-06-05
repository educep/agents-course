# Introducción a LlamaHub

LlamaHub es un registro de cientos de integraciones, agentes y herramientas que puedes usar dentro de LlamaIndex.

**LlamaHub**

Estaremos usando varias integraciones en este curso, así que primero veamos [LlamaHub](https://llamahub.ai/) y cómo nos puede ayudar.

Veamos cómo encontrar e instalar las dependencias para los componentes que necesitamos.

## Instalación

Las instrucciones de instalación de LlamaIndex están disponibles como una descripción bien estructurada en [LlamaHub](https://llamahub.ai/). Esto puede ser un poco abrumador al principio, pero la mayoría de los comandos de instalación generalmente siguen un formato fácil de recordar:

```bash
pip install llama-index-{tipo-de-componente}-{nombre-del-framework}
```

Intentemos instalar las dependencias para un componente LLM y de embedding usando la integración de la [API de inferencia de Hugging Face](https://llamahub.ai/l/llms/llama-index-llms-huggingface-api?from=llms ).

```bash
pip install llama-index-llms-huggingface-api llama-index-embeddings-huggingface
```

## Uso

Una vez instalado, podemos ver los patrones de uso. ¡Notarás que las rutas de importación siguen el comando de instalación! A continuación, podemos ver un ejemplo del uso de la API de inferencia de Hugging Face para un componente LLM.

```python
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# Obtener HF_TOKEN de las variables de entorno
hf_token = os.getenv("HF_TOKEN")

llm = HuggingFaceInferenceAPI(
    model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
    temperature=0.7,
    max_tokens=100,
    token=hf_token,
)

response = llm.complete("Hola, ¿cómo estás?")
print(response)
# Estoy bien, ¿cómo puedo ayudarte hoy?
```

¡Excelente! Ahora sabemos cómo encontrar, instalar y usar las integraciones para los componentes que necesitamos. Profundicemos más en los componentes y veamos cómo podemos usarlos para construir nuestros propios agentes.
