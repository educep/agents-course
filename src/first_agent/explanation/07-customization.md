# Customization Guide

This guide explains how to extend and modify the First Agent to suit your specific needs. The agent is designed to be flexible and customizable, allowing you to adapt it for various use cases.

## Adding New Tools

One of the most common customizations is adding new tools to extend the agent's capabilities.

### Function-based Tools

For simple tools, use the `@tool` decorator:

```python
from smolagents import tool

@tool
def get_weather(city: str) -> str:
    """Gets current weather for a city
    Args:
        city: Name of the city
    """
    # In a real implementation, you would call a weather API
    # This is a simplified example
    return f"Current weather in {city}: 22°C, Partly Cloudy"
```

Key points:
- Include type hints for parameters and return value
- Add a docstring with a clear description and parameter details
- Implement error handling
- Return results in a format the agent can use

### Class-based Tools

For more complex tools, extend the `Tool` class:

```python
from smolagents.tools import Tool

class WeatherTool(Tool):
    name = "get_weather"
    description = "Gets current weather for a city"
    inputs = {"city": {"type": "string", "description": "Name of the city"}}
    output_type = "string"

    def forward(self, city: str) -> str:
        # Implementation logic
        return f"Current weather in {city}: 22°C, Partly Cloudy"
```

Key points:
- Define class attributes: name, description, inputs, output_type
- Implement the `forward` method with your logic
- Add initialization if needed (in `__init__`)

### Adding Tools to the Agent

After creating a tool, add it to the agent's tools list:

```python
# For function-based tools
agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone,
           DuckDuckGoSearchTool(), get_weather],  # Add the new tool here
    # ... other configuration remains the same
)

# For class-based tools
weather_tool = WeatherTool()
agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone,
           DuckDuckGoSearchTool(), weather_tool],  # Add the tool instance
    # ... other configuration remains the same
)
```

## Modifying System Prompts

You can customize the agent's behavior by modifying the system prompt in `prompts.yaml`:

### Changing the Overall Approach

Edit the main system prompt to change how the agent approaches problems:

```yaml
"system_prompt": |-
  You are an expert data analyst who can solve any data-related task using code blobs.
  To do so, you have been given access to a list of tools: these tools are basically Python functions which you can call with code.
  To solve the task, you must plan forward to proceed in a series of steps, in a cycle of 'Thought:', 'Code:', and 'Observation:' sequences.

  # ... rest of the prompt
```

### Adding Custom Examples

Add examples relevant to your use case:

```yaml
  Here are a few examples using notional tools:
  ---
  Task: "Analyze the sales data for Q1 and create a visualization."

  Thought: I will use the `load_data` tool to read the sales data, then analyze it with pandas, and finally create a visualization.
  Code:
  ```py
  data = load_data("sales_q1.csv")
  print(data.head())
  ```<end_code>
  Observation: "   Date       Product  Sales  Revenue
  0  2025-01-01  ProductA     10    1000.0
  1  2025-01-02  ProductB      5     750.0
  2  2025-01-03  ProductA      8     800.0
  3  2025-01-04  ProductC     12    1440.0
  4  2025-01-05  ProductB      7    1050.0"

  # ... rest of the example
```

### Modifying Rules

Add or change rules to guide the agent's behavior:

```yaml
  Here are the rules you should always follow to solve your task:
  # ... existing rules
  11. When working with data, always check for missing values and data types before proceeding with analysis.
  12. For data visualizations, always include appropriate labels, titles, and legends.
```

## Customizing the UI

You can modify the Gradio UI to change the user experience:

### Changing Appearance

Modify the chatbot appearance in `Gradio_UI.py`:

```python
chatbot = gr.Chatbot(
    label="Data Analysis Assistant",  # Change the label
    type="messages",
    avatar_images=(
        None,
        "path/to/custom/avatar.png",  # Change the avatar image
    ),
    resizeable=True,
    scale=1,
)
```

### Adding Custom Components

Add new components to the UI:

```python
def launch(self, **kwargs):
    import gradio as gr

    with gr.Blocks(fill_height=True) as demo:
        # ... existing components

        # Add a dropdown for selecting analysis type
        analysis_type = gr.Dropdown(
            choices=["Sales Analysis", "Customer Segmentation", "Inventory Forecasting"],
            label="Analysis Type",
            value="Sales Analysis"
        )

        # Modify the submit logic to include the new component
        text_input.submit(
            self.log_user_message_with_type,
            [text_input, file_uploads_log, analysis_type],
            [stored_messages, text_input],
        ).then(self.interact_with_agent, [stored_messages, chatbot], [chatbot])
```

### Enabling File Upload

To enable file uploads, provide a folder when creating the UI:

```python
# In app.py
GradioUI(agent, file_upload_folder="./uploads").launch(server_name="0.0.0.0", server_port=7860)
```

This allows users to upload files for the agent to process.

## Changing the Model

You can use a different language model by modifying the model configuration:

```python
# Using a different Hugging Face model
model = HfApiModel(
    max_tokens=2096,
    temperature=0.7,  # Adjust temperature for more creativity
    model_id="different_model_endpoint",
    custom_role_conversions=None,
)

# Or using OpenAI models
from smolagents import OpenAIModel

model = OpenAIModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="gpt-4",
    api_key="your_openai_api_key"
)
```

Consider these factors when choosing a model:
- Capabilities and limitations
- Token limits
- Processing speed
- Cost per request
- Reasoning abilities

## Modifying Agent Parameters

You can adjust the agent's behavior by changing its parameters:

```python
agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone, DuckDuckGoSearchTool()],
    max_steps=10,           # Increase the maximum steps for complex tasks
    verbosity_level=3,      # Increase verbosity for more detailed logs
    grammar=None,
    planning_interval=2,    # Plan every 2 steps
    name="DataAnalysisAgent",
    description="A specialized agent for data analysis tasks",
    prompt_templates=prompt_templates,
)
```

Key parameters to consider:
- `max_steps`: Maximum number of steps for solving a task
- `verbosity_level`: Detail level in logs and responses
- `planning_interval`: How often to revisit the plan
- `name` and `description`: Metadata for the agent

## Adding Specialized Functionality

You can extend the agent with specialized functionality for specific domains:

### Data Analysis Tools

```python
@tool
def analyze_data(csv_path: str, analysis_type: str) -> str:
    """Analyzes data in a CSV file
    Args:
        csv_path: Path to the CSV file
        analysis_type: Type of analysis to perform (summary, correlation, trend)
    """
    import pandas as pd

    # Load the data
    df = pd.read_csv(csv_path)

    # Perform the requested analysis
    if analysis_type == "summary":
        return df.describe().to_string()
    elif analysis_type == "correlation":
        return df.corr().to_string()
    elif analysis_type == "trend":
        # Simple trend analysis
        if 'date' in df.columns or 'Date' in df.columns:
            date_col = 'date' if 'date' in df.columns else 'Date'
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.sort_values(by=date_col)
            numeric_cols = df.select_dtypes(include=['number']).columns
            return f"Trend analysis for {', '.join(numeric_cols)}: {df[numeric_cols].diff().mean().to_dict()}"
        else:
            return "No date column found for trend analysis"
    else:
        return f"Unknown analysis type: {analysis_type}"
```

### Image Processing Tools

```python
@tool
def process_image(image_path: str, operation: str) -> str:
    """Processes an image file
    Args:
        image_path: Path to the image file
        operation: Operation to perform (resize, grayscale, blur)
    """
    from PIL import Image, ImageFilter
    import os

    try:
        img = Image.open(image_path)
        output_path = os.path.splitext(image_path)[0] + "_processed" + os.path.splitext(image_path)[1]

        if operation == "resize":
            img = img.resize((img.width // 2, img.height // 2))
        elif operation == "grayscale":
            img = img.convert('L')
        elif operation == "blur":
            img = img.filter(ImageFilter.BLUR)
        else:
            return f"Unknown operation: {operation}"

        img.save(output_path)
        return f"Image processed with {operation} and saved to {output_path}"
    except Exception as e:
        return f"Error processing image: {str(e)}"
```

## Creating Domain-Specific Agents

You can create specialized agents for specific domains by combining:
- Custom tools
- Tailored system prompts
- Specialized UI components

### Example: Data Analysis Agent

```python
# 1. Define data analysis tools
@tool
def load_data(file_path: str) -> str:
    """Loads data from a file and returns info about it
    Args:
        file_path: Path to the data file
    """
    import pandas as pd

    df = pd.read_csv(file_path)
    return f"Loaded data with {len(df)} rows and columns: {', '.join(df.columns)}"

@tool
def visualize_data(file_path: str, x_column: str, y_column: str) -> str:
    """Creates a visualization from data
    Args:
        file_path: Path to the data file
        x_column: Column for x-axis
        y_column: Column for y-axis
    """
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv(file_path)
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{y_column} vs {x_column}")
    output_path = "visualization.png"
    plt.savefig(output_path)
    plt.close()
    return f"Visualization saved to {output_path}"

# 2. Modify the system prompt
with open("prompts.yaml") as stream:
    prompt_templates = yaml.safe_load(stream)

prompt_templates["system_prompt"] = prompt_templates["system_prompt"].replace(
    "You are an expert assistant",
    "You are an expert data analyst"
)

# 3. Create the specialized agent
data_agent = CodeAgent(
    model=model,
    tools=[final_answer, load_data, visualize_data, analyze_data],
    max_steps=10,
    verbosity_level=2,
    grammar=None,
    planning_interval=None,
    name="DataAnalysisAgent",
    description="A specialized agent for data analysis tasks",
    prompt_templates=prompt_templates,
)

# 4. Launch with a custom UI
GradioUI(data_agent, file_upload_folder="./data_uploads").launch(
    server_name="0.0.0.0",
    server_port=7860
)
```

## Deployment Customization

You can customize how the agent is deployed:

### Docker Configuration

Modify the Dockerfile for your needs:

```dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gradio pytz pyyaml matplotlib pandas pillow  # Add your custom dependencies

# Copy the application code
COPY . /app/src/custom_agent/

# Add the app directory to Python path
ENV PYTHONPATH=/app

# Set environment variables
ENV MODEL_API_KEY=your_model_api_key
ENV UPLOAD_FOLDER=/app/uploads

# Create upload directory
RUN mkdir -p /app/uploads

# Expose the port Gradio will run on
EXPOSE 7860

# Set the working directory to where the app.py is located
WORKDIR /app/src/custom_agent

# Command to run the application
CMD ["python", "app.py"]
```

### Production Settings

For production deployment, consider:

```python
# In app.py
import os

# Environment-based configuration
model_id = os.environ.get('MODEL_ENDPOINT', 'default_model_endpoint')
api_key = os.environ.get('API_KEY', None)
port = int(os.environ.get('PORT', 7860))
host = os.environ.get('HOST', '0.0.0.0')
debug = os.environ.get('DEBUG', 'False').lower() == 'true'
upload_folder = os.environ.get('UPLOAD_FOLDER', './uploads')

# Configure model
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id=model_id,
    custom_role_conversions=None,
    api_key=api_key
)

# ... agent configuration

# Launch with production settings
GradioUI(agent, file_upload_folder=upload_folder).launch(
    server_name=host,
    server_port=port,
    debug=debug,
    auth=(os.environ.get('USERNAME'), os.environ.get('PASSWORD')) if os.environ.get('USERNAME') else None,
    ssl_keyfile=os.environ.get('SSL_KEY'),
    ssl_certfile=os.environ.get('SSL_CERT')
)
```

## Best Practices for Customization

When customizing the agent, follow these best practices:

1. **Incremental Changes**: Make and test changes incrementally
2. **Compatibility**: Ensure new tools and components work with existing ones
3. **Error Handling**: Implement robust error handling in all custom components
4. **Documentation**: Document any customizations for future reference
5. **Testing**: Thoroughly test custom tools with a variety of inputs
6. **Performance**: Consider the performance impact of customizations
7. **Security**: Validate inputs and secure any sensitive operations
8. **Maintainability**: Keep customizations modular and maintainable
9. **Graceful Degradation**: Allow the agent to continue functioning if custom components fail
10. **User Experience**: Consider the end-user experience in all customizations

By following these guidelines and leveraging the customization options available, you can adapt the First Agent to a wide range of specialized use cases and requirements.
