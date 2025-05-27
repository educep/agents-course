# Third party imports
import os
from typing import Any, TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

# Internal imports
from config.settings import settings

# Configurar la variable de entorno (si no está configurada)
# os.environ["OPENAI_API_KEY"] = settings.open_api_key
model = ChatOpenAI(model="gpt-4o", temperature=0, api_key=settings.open_api_key)


# Paso 1: Definiendo nuestra estructura de estado
# Definir la estructura del estado
class EmailState(TypedDict):
    """
    En LangGraph, State es el concepto central. Representa toda la información que fluye a través de nuestro flujo de trabajo.

    Necesitamos rastrear:
    - El correo electrónico que se está procesando
    - Si es spam o no
    - La respuesta preliminar (para correos legítimos)
    - El historial de conversación con el LLM
    """

    # El correo electrónico que se está procesando
    email: dict[str, Any]  # Contiene asunto, remitente, cuerpo, etc.
    # Categoría del correo electrónico (consulta, queja, etc.)
    email_category: str | None
    # Razón por la que el correo fue marcado como spam
    spam_reason: str | None
    # Análisis y decisiones
    is_spam: bool | None
    # Generación de respuesta
    email_draft: str | None
    # Metadatos de procesamiento
    messages: list[dict[str, Any]]  # Rastrear conversación con LLM para análisis


# Paso 2: Definiendo nuestros nodos
def read_email(state: EmailState):
    """Alfred lee y registra el correo electrónico entrante"""
    email = state["email"]
    # Aquí podríamos hacer algún preprocesamiento inicial
    print(f"Alfred está procesando un correo de {email['sender']} con asunto: {email['subject']}")
    # No se necesitan cambios de estado aquí
    return {}


def classify_email(state: EmailState):
    """Alfred usa un LLM para determinar si el correo es spam o legítimo"""
    email = state["email"]
    # Preparar nuestro prompt para el LLM
    prompt = f"""
    Como Alfred el mayordomo, analiza este correo electrónico y determina si es spam o legítimo.
    Correo:
    De: {email['sender']}
    Asunto: {email['subject']}
    Cuerpo: {email['body']}
    Primero, determina si este correo es spam. Explica la razón de por qué lo clasificas como spam o no.
    Responde con SPAM o HAM si es legítimo.
    Si es legítima categorízala en una de las siguientes categorías: consulta, queja, agradecimiento, solicitud, información.
    """
    # Llamar al LLM
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)
    # Lógica simple para analizar la respuesta (en una app real, querrías un análisis más robusto)
    response_text = response.content.lower()
    is_spam = "spam" in response_text and "ham" not in response_text
    # Extraer una razón si es spam
    spam_reason = None
    if is_spam and "razón:" in response_text:
        spam_reason = response_text.split("razón:")[1].strip()
    # Determinar categoría si es legítimo
    email_category = None
    if not is_spam:
        categories = ["consulta", "queja", "agradecimiento", "solicitud", "información"]
        for category in categories:
            if category in response_text:
                email_category = category
                break
    # Actualizar mensajes para seguimiento
    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content},
    ]
    # Devolver actualizaciones de estado
    return {
        "is_spam": is_spam,
        "spam_reason": spam_reason,
        "email_category": email_category,
        "messages": new_messages,
    }


def handle_spam(state: EmailState):
    """Alfred descarta el correo spam con una nota"""
    print(f"Alfred ha marcado el correo como spam. Razón: {state['spam_reason']}")
    print("El correo ha sido movido a la carpeta de spam.")
    # Hemos terminado de procesar este correo
    return {}


def draft_response(state: EmailState):
    """Alfred redacta una respuesta preliminar para correos legítimos"""
    email = state["email"]
    category = state["email_category"] or "general"
    # Preparar nuestro prompt para el LLM
    prompt = f"""
    Como Alfred el mayordomo, redacta una respuesta preliminar cortés a este correo electrónico.
    Correo:
    De: {email['sender']}
    Asunto: {email['subject']}
    Cuerpo: {email['body']}
    Este correo ha sido categorizado como: {category}
    Redacta una respuesta breve y profesional que el Sr. Hugg pueda revisar y personalizar antes de enviar.
    """
    # Llamar al LLM
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)
    # Actualizar mensajes para seguimiento
    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content},
    ]
    # Devolver actualizaciones de estado
    return {"email_draft": response.content, "messages": new_messages}


def notify_mr_hugg(state: EmailState):
    """Alfred notifica al Sr. Hugg sobre el correo y presenta el borrador de respuesta"""
    email = state["email"]
    print("\n" + "=" * 50)
    print(f"Señor, ha recibido un correo electrónico de {email['sender']}.")
    print(f"Asunto: {email['subject']}")
    print(f"Categoría: {state['email_category']}")
    print("\nHe preparado un borrador de respuesta para su revisión:")
    print("-" * 50)
    print(state["email_draft"])
    print("=" * 50 + "\n")
    # Hemos terminado de procesar este correo
    return {}


# Paso 3: Definiendo nuestra lógica de enrutamiento
def route_email(state: EmailState) -> str:
    """Determina el siguiente paso basado en la clasificación de spam"""
    if state["is_spam"]:
        return "spam"
    else:
        return "legitimate"


# Paso 4: Crear el StateGraph y definir las aristas
# Crear el grafo
email_graph = StateGraph(EmailState)

# Añadir nodos
email_graph.add_node("read_email", read_email)
email_graph.add_node("classify_email", classify_email)
email_graph.add_node("handle_spam", handle_spam)
email_graph.add_node("draft_response", draft_response)
email_graph.add_node("notify_mr_hugg", notify_mr_hugg)

# Añadir las aristas
email_graph.add_edge(START, "read_email")

# Añadir las aristas - definiendo el flujo
email_graph.add_edge("read_email", "classify_email")

# Añadir la bifurcación condicional desde classify_email
email_graph.add_conditional_edges(
    "classify_email", route_email, {"spam": "handle_spam", "legitimate": "draft_response"}
)

# Añadir las aristas finales
email_graph.add_edge("handle_spam", END)
email_graph.add_edge("draft_response", "notify_mr_hugg")
email_graph.add_edge("notify_mr_hugg", END)

# Compilar el grafo
compiled_graph = email_graph.compile()


# Función de ejemplo de uso
def run_email_example():
    # Ejemplo de correo legítimo
    legitimate_email = {
        "sender": "juan.perez@ejemplo.com",
        "subject": "Pregunta sobre sus servicios",
        "body": "Estimado Sr. Hugg, me refirió un colega y estoy decepcionado del servicio que me ofrece. Saludos cordiales, Juan Pérez",
    }

    # Ejemplo de correo spam
    spam_email = {
        "sender": "ganador@loteria-intl.com",
        "subject": "¡¡¡HAS GANADO $5,000,000!!!",
        "body": "¡FELICIDADES! Has sido seleccionado como ganador de nuestra lotería internacional. Para reclamar tu premio de $5,000,000, por favor envíanos los datos de tu banco y una tarifa de procesamiento de $100.",
    }

    # Procesar el correo legítimo
    print("\nProcesando correo legítimo...")
    legitimate_result = compiled_graph.invoke(
        {
            "email": legitimate_email,
            "is_spam": None,
            "spam_reason": None,
            "email_category": None,
            "email_draft": None,
            "messages": [],
        }
    )

    # Procesar el correo spam
    print("\nProcesando correo spam...")
    spam_result = compiled_graph.invoke(
        {
            "email": spam_email,
            "is_spam": None,
            "spam_reason": None,
            "email_category": None,
            "email_draft": None,
            "messages": [],
        }
    )

    return legitimate_result, spam_result


if __name__ == "__main__":
    run_email_example()

    # Visualizando Nuestro Grafo
    # LangGraph nos permite visualizar nuestro flujo de trabajo para entender mejor y depurar su estructura:

    # Guardar el diagrama como PNG en la carpeta assets
    try:
        # Crear directorio assets si no existe en la carpeta actual del script
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        os.makedirs(assets_dir, exist_ok=True)

        graph_png = compiled_graph.get_graph().draw_mermaid_png()
        file_path = os.path.join(assets_dir, "email_workflow_graph.png")

        with open(file_path, "wb") as f:
            f.write(graph_png)
        print(f"Gráfico del flujo de trabajo guardado en: {file_path}")
    except Exception as e:
        print(f"Error al guardar el gráfico: {e}")
        print("Nota: Asegúrese de tener instaladas las dependencias necesarias para Mermaid")
