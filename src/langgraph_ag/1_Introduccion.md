# LangGraph - Módulo de Agentes

## Resumen del Módulo

En esta unidad, descubrirás:

1. **¿Qué es LangGraph y cuándo usarlo?**
2. **Bloques de construcción de LangGraph**
3. **Alfred, el mayordomo clasificador de correos**
4. **Alfred, el agente analista de documentos**
5. **Quiz**

> **⚠️ Nota Importante:** Los ejemplos en esta sección requieren acceso a un modelo LLM/VLM potente. Los ejecutamos usando la API de GPT-4o porque tiene la mejor compatibilidad con LangGraph.

## ¿Qué es LangGraph?

**LangGraph** es un framework desarrollado por LangChain para gestionar el flujo de control de aplicaciones que integran un LLM (Large Language Model).

### Diferencias con LangChain

Aunque ambos forman parte del ecosistema LangChain, son paquetes diferentes:

- **LangChain**: Proporciona una interfaz estándar para interactuar con modelos y otros componentes, útil para recuperación de información, llamadas a LLM y herramientas.
- **LangGraph**: Se enfoca en el control del flujo de ejecución y puede usarse de forma independiente, aunque comúnmente se usan en conjunto.

### ¿Cuándo usar LangGraph?

LangGraph es ideal cuando necesitas **control** sobre la ejecución de tu aplicación, especialmente en:

- **Procesos de razonamiento multi-paso** que requieren control explícito del flujo
- **Aplicaciones que necesitan persistencia** de estado entre pasos
- **Sistemas que combinan lógica determinística** con capacidades de IA
- **Flujos de trabajo con intervención humana** (human-in-the-loop)
- **Arquitecturas de agentes complejas** con múltiples componentes

### ¿Cómo funciona?

LangGraph utiliza una **estructura de grafo dirigido**:

- **Nodos**: Representan pasos de procesamiento individuales (llamadas a LLM, uso de herramientas, decisiones)
- **Aristas**: Definen las transiciones posibles entre pasos
- **Estado**: Definido por el usuario, se mantiene y pasa entre nodos durante la ejecución

### Ventajas sobre Python vanilla

Aunque podrías implementar flujos similares con Python tradicional, LangGraph ofrece:

- ✅ **Estados integrados** y gestión automática
- ✅ **Visualización** del flujo de trabajo
- ✅ **Logging y trazas** incorporados
- ✅ **Human-in-the-loop** nativo
- ✅ **Abstracciones** especializadas para agentes IA

## Documentación Oficial

Para más información, referirse a la documentación oficial de LangGraph:
- [Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph)
- [Ejemplos de agentes](https://langchain-ai.github.io/langgraph/)
