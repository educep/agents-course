from smolagents import CodeAgent
from smolagents.models import LiteLLMModel

# Internal imports
from config.settings import settings

# Define the LLM Model
model = LiteLLMModel(
    model_id="deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    api_key=settings.deepseek_api_key,
    temperature=0.0,
)


agent = CodeAgent(tools=[], model=model, additional_authorized_imports=["datetime"])

agent.run(
    """
    Alfred needs to prepare for the party. Here are the tasks:
    1. Prepare the drinks - 30 minutes
    2. Decorate the mansion - 60 minutes
    3. Set up the menu - 45 minutes
    4. Prepare the music and playlist - 45 minutes

    If we start right now, at what time will the party be ready?
    """
)
