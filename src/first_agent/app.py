# External imports
import datetime  # import requests
from pathlib import Path

import pytz
import yaml
from Gradio_UI import GradioUI
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, load_tool, tool

# from smolagents import HfApiModel
# Internal imports
from tools.final_answer import FinalAnswerTool

from config.settings import settings


# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:  # it's import to specify the return type
    # Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud'

# model = HfApiModel(
#     max_tokens=2096,
#     temperature=0.5,
#     model_id="https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud",
#     custom_role_conversions=None,
# )

# Define the LLM Model
model = LiteLLMModel(
    model_id="deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    api_key=settings.deepseek_api_key,
    temperature=0.0,
)

print(settings.hf_token)
# Import tool from Hub
image_generation_tool = load_tool(
    "m-ric/text-to-image", trust_remote_code=True, token=settings.hf_token
)

path_to_prompts = Path(__file__).parent / "prompts.yaml"
with open(path_to_prompts) as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        my_custom_tool,
        image_generation_tool,
        get_current_time_in_timezone,
        DuckDuckGoSearchTool(),
    ],
    max_steps=6,
    verbosity_level=2,  # Increased verbosity
    grammar=None,
    planning_interval=None,
    name="TestAgent",
    description="A test agent to verify model responses",
    prompt_templates=prompt_templates,
)

GradioUI(agent).launch(server_name="0.0.0.0", server_port=7860)
