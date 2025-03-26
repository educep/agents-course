# Main Application (app.py)

The `app.py` file is the entry point of the First Agent application. It sets up all the components needed for the agent to function including the language model, tools, and the web interface.

## File Overview

The main application file performs the following tasks:

1. Imports necessary libraries and components
2. Defines custom tools
3. Configures the language model
4. Sets up the agent with tools and parameters
5. Launches the Gradio web interface

## Code Walkthrough

Let's break down the code in `app.py` section by section:

### Imports

```python
import datetime
import pytz
import yaml
from Gradio_UI import GradioUI
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool
from tools.final_answer import FinalAnswerTool
```

These imports include:
- Standard libraries (`datetime`, `pytz`) for time handling
- `yaml` for reading prompt templates
- `GradioUI` from the local module for the web interface
- Core components from `smolagents`: `CodeAgent`, `HfApiModel`, etc.
- Custom tools from the `tools` package

### Custom Tool Definitions

The file defines custom tools using the `@tool` decorator:

```python
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"
```

This is a placeholder tool that takes two arguments but doesn't do anything useful yet. It serves as a template for custom tool development.

```python
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
```

This tool fetches the current time in a specified timezone using the `pytz` library. It:
1. Takes a timezone name as input
2. Creates a timezone object
3. Gets the current time in that timezone
4. Formats and returns the time as a string
5. Handles exceptions with an error message

### Tool Instantiation

```python
final_answer = FinalAnswerTool()
```

This line instantiates the `FinalAnswerTool` defined in `tools/final_answer.py`, which is used to provide the final response to user queries.

### Language Model Configuration

```python
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud",
    custom_role_conversions=None,
)
```

This configures the language model using `HfApiModel` from SmolaAgent:
- `max_tokens`: Maximum length of responses (2096 tokens)
- `temperature`: Controls randomness (0.5 is moderately deterministic)
- `model_id`: URL of the Hugging Face endpoint for the Qwen2.5-Coder model
- `custom_role_conversions`: Set to None, using default role mappings

### Loading Prompt Templates

```python
with open("prompts.yaml") as stream:
    prompt_templates = yaml.safe_load(stream)
```

This loads the prompt templates from the `prompts.yaml` file, which contains system prompts and templates that guide the agent's behavior.

### Agent Initialization

```python
agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone, DuckDuckGoSearchTool()],
    max_steps=6,
    verbosity_level=2,
    grammar=None,
    planning_interval=None,
    name="TestAgent",
    description="A test agent to verify model responses",
    prompt_templates=prompt_templates,
)
```

This creates an instance of the `CodeAgent` class with the following configuration:
- `model`: The language model instance configured earlier
- `tools`: List of tools available to the agent
  - `final_answer`: For providing final responses
  - `my_custom_tool`: The placeholder custom tool
  - `get_current_time_in_timezone`: The timezone tool
  - `DuckDuckGoSearchTool()`: For web searches
- `max_steps`: Limits the agent to 6 steps when solving tasks
- `verbosity_level`: Set to 2 for detailed logs
- `grammar`: Set to None, using default grammar
- `planning_interval`: Set to None, no planning intervals
- `name` and `description`: Metadata for the agent
- `prompt_templates`: The templates loaded from prompts.yaml

### Model Testing

```python
try:
    test_response = agent.model.chat_completion(
        messages=[{"role": "user", "content": "Say 'test' if you can hear me"}]
    )
    print("Model test response:", test_response)
except Exception as e:
    print("Error testing model:", str(e))
```

This block tests the language model to ensure it's working properly before launching the agent:
1. It sends a simple test message to the model
2. Prints the response
3. Catches and reports any errors that occur

### Launching the UI

```python
GradioUI(agent).launch(server_name="0.0.0.0", server_port=7860)
```

This final line:
1. Creates an instance of the `GradioUI` class with the agent
2. Launches the web interface on all interfaces (0.0.0.0) on port 7860

## Flow of Execution

When `app.py` is run, the execution flows as follows:

1. Custom tools are defined
2. The `FinalAnswerTool` is instantiated
3. The language model is configured
4. Prompt templates are loaded from prompts.yaml
5. The agent is initialized with the model, tools, and templates
6. A test query is sent to the model to verify it's working
7. The Gradio web interface is launched

This sets up a complete agent system ready to process user queries through the web interface.

## Customization Points

The `app.py` file offers several opportunities for customization:

1. **Adding new tools**: Define new functions with the `@tool` decorator
2. **Changing model parameters**: Adjust temperature, max tokens, etc.
3. **Using a different model**: Change the model_id to a different endpoint
4. **Modifying agent behavior**: Adjust max_steps, verbosity, etc.
5. **UI configuration**: Change server parameters or UI options

By modifying these aspects, you can adapt the agent for different use cases and requirements.
