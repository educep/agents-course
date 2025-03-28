# External imports
import datetime
import os
import tempfile

import pytz
import yaml
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool
from tools.final_answer import FinalAnswerTool

from config.settings import settings

# Internal imports
from src.first_agent.Streamlit_UI import StreamlitUI


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

model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud",
    custom_role_conversions=None,
)

# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# Reads prompts from prompts.yaml
path_to_prompts = settings.project_path / "src/first_agent/prompts.yaml"
with open(path_to_prompts) as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone, DuckDuckGoSearchTool()],
    max_steps=6,
    verbosity_level=2,  # Increased verbosity
    grammar=None,
    planning_interval=None,
    name="TestAgent",
    description="A test agent to verify model responses",
    prompt_templates=prompt_templates,
)

# Create a temporary directory for file uploads
upload_dir = os.path.join(tempfile.gettempdir(), "streamlit_uploads")
os.makedirs(upload_dir, exist_ok=True)

# Launch the Streamlit interface
StreamlitUI(agent, file_upload_folder=upload_dir).run()
