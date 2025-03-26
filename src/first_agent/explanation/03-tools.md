# Tools

Tools are a key component of the First Agent, providing the agent with capabilities to perform specific tasks. This document explains the tools implemented in the agent, how they work, and how to create custom tools.

## Tool Overview

In the SmolaAgent framework, tools are functions or classes that can be called by the agent to perform specific operations. Each tool has:

- A name
- A description
- Input parameters with types and descriptions
- An output type
- Implementation logic

The First Agent includes several built-in tools and demonstrates how to create custom tools.

## Tools in the First Agent

### 1. FinalAnswerTool (tools/final_answer.py)

This tool is used to provide the final response to a user query.

```python
from typing import Any
from smolagents.tools import Tool

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides a final answer to the given problem."
    inputs = {"answer": {"type": "any", "description": "The final answer to the problem"}}
    output_type = "any"

    def forward(self, answer: Any) -> Any:
        return answer

    def __init__(self, *args, **kwargs):
        self.is_initialized = False
```

The `FinalAnswerTool` is a simple pass-through tool that returns its input as the final answer. It's designed to mark the completion of the agent's task and provide the final result.

### 2. DuckDuckGoSearchTool (tools/web_search.py)

This tool enables web searches to retrieve information from the internet.

```python
from smolagents.tools import Tool

class DuckDuckGoSearchTool(Tool):
    name = "web_search"
    description = "Performs a duckduckgo web search based on your query (think a Google search) then returns the top search results."
    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    def __init__(self, max_results=10, **kwargs):
        super().__init__()
        self.max_results = max_results
        try:
            from duckduckgo_search import DDGS
        except ImportError as e:
            raise ImportError(
                "You must install package `duckduckgo_search` to run this tool: for instance run `pip install duckduckgo-search`."
            ) from e
        self.ddgs = DDGS(**kwargs)

    def forward(self, query: str) -> str:
        results = self.ddgs.text(query, max_results=self.max_results)
        if len(results) == 0:
            raise Exception("No results found! Try a less restrictive/shorter query.")
        postprocessed_results = [
            f"[{result['title']}]({result['href']})\n{result['body']}" for result in results
        ]
        return "## Search Results\n\n" + "\n\n".join(postprocessed_results)
```

This tool:
1. Takes a search query as input
2. Uses the DuckDuckGo search API to retrieve results
3. Formats the results in Markdown with titles, links, and snippets
4. Returns the formatted results as a string

### 3. VisitWebpageTool (tools/visit_webpage.py)

This tool fetches and parses content from websites for the agent to process.

```python
import re
from smolagents.tools import Tool

class VisitWebpageTool(Tool):
    name = "visit_webpage"
    description = "Visits a webpage at the given url and reads its content as a markdown string. Use this to browse webpages."
    inputs = {"url": {"type": "string", "description": "The url of the webpage to visit."}}
    output_type = "string"

    def forward(self, url: str) -> str:
        try:
            import requests
            from markdownify import markdownify
            from requests.exceptions import RequestException
            from smolagents.utils import truncate_content
        except ImportError as e:
            raise ImportError(
                "You must install packages `markdownify` and `requests` to run this tool: for instance run `pip install markdownify requests`."
            ) from e
        try:
            # Send a GET request to the URL with a 20-second timeout
            response = requests.get(url, timeout=20)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Convert the HTML content to Markdown
            markdown_content = markdownify(response.text).strip()

            # Remove multiple line breaks
            markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

            return truncate_content(markdown_content, 10000)

        except requests.exceptions.Timeout:
            return "The request timed out. Please try again later or check the URL."
        except RequestException as e:
            return f"Error fetching the webpage: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def __init__(self, *args, **kwargs):
        self.is_initialized = False
```

This tool:
1. Takes a URL as input
2. Fetches the webpage content using the requests library
3. Converts the HTML content to Markdown using markdownify
4. Cleans up the content (removing excess line breaks)
5. Truncates the content to a reasonable length
6. Handles various error cases with informative messages

### 4. get_current_time_in_timezone (app.py)

This is a function-based tool for retrieving the current time in different timezones.

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

This tool demonstrates creating a function-based tool using the `@tool` decorator:
1. It takes a timezone string as input
2. Uses the pytz library to create a timezone object
3. Gets the current time in that timezone
4. Formats and returns the time as a string
5. Handles exceptions with informative error messages

### 5. my_custom_tool (app.py)

This is a placeholder tool that demonstrates the structure of a function-based tool.

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

This tool shows how to:
1. Use the `@tool` decorator
2. Define input parameters with types
3. Specify a return type
4. Document the tool with docstrings

## Tool Implementation Approaches

The First Agent demonstrates two approaches to implementing tools:

### Class-based Tools

Class-based tools extend the `Tool` class from SmolaAgent:

```python
from smolagents.tools import Tool

class MyClassTool(Tool):
    name = "tool_name"
    description = "Tool description"
    inputs = {
        "param1": {"type": "string", "description": "First parameter"},
        "param2": {"type": "integer", "description": "Second parameter"}
    }
    output_type = "string"

    def forward(self, param1: str, param2: int) -> str:
        # Implementation logic
        return "Result"
```

Class-based tools are useful for:
- Complex tools with multiple methods
- Tools that require initialization
- Tools with shared state between calls

### Function-based Tools

Function-based tools use the `@tool` decorator:

```python
from smolagents import tool

@tool
def my_function_tool(param1: str, param2: int) -> str:
    """Tool description
    Args:
        param1: First parameter description
        param2: Second parameter description
    """
    # Implementation logic
    return "Result"
```

Function-based tools are simpler and more concise, suitable for:
- Straightforward operations
- Stateless tools
- Quick prototyping

## How Tools Are Used by the Agent

The agent uses tools through a structured process:

1. The agent receives a user query
2. It uses the language model to reason about which tool to use
3. It generates Python code to call the appropriate tool
4. It executes the code and observes the results
5. It uses the results to inform further steps or provide a final answer

For example, when asked "What time is it in Tokyo?", the agent might:

```
Thought: I need to find the current time in Tokyo. I can use the get_current_time_in_timezone tool with "Asia/Tokyo" as the timezone parameter.

Code:
```py
result = get_current_time_in_timezone(timezone="Asia/Tokyo")
print(result)
```<end_code>

Observation: "The current local time in Asia/Tokyo is: 2025-03-26 22:45:12"

Thought: I now have the current time in Tokyo. I can provide this as the final answer.

Code:
```py
final_answer("The current local time in Tokyo is 2025-03-26 22:45:12")
```<end_code>
```

## Creating Custom Tools

To extend the agent with new capabilities, you can create custom tools. Here's a step-by-step guide:

### Function-based Custom Tool

1. Import the `tool` decorator from `smolagents`
2. Define a function with typed parameters and return value
3. Add a docstring describing the tool and its parameters
4. Apply the `@tool` decorator
5. Add the tool to the agent's tools list

Example:

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

# Then add it to the agent's tools list
agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone,
           DuckDuckGoSearchTool(), get_weather],  # Add the new tool here
    # ... other configuration remains the same
)
```

### Class-based Custom Tool

1. Import the `Tool` class from `smolagents.tools`
2. Create a class that extends `Tool`
3. Define class attributes: name, description, inputs, output_type
4. Implement the `forward` method with the tool's logic
5. Add the tool instance to the agent's tools list

Example:

```python
from smolagents.tools import Tool

class WeatherTool(Tool):
    name = "get_weather"
    description = "Gets current weather for a city"
    inputs = {"city": {"type": "string", "description": "Name of the city"}}
    output_type = "string"

    def forward(self, city: str) -> str:
        # In a real implementation, you would call a weather API
        # This is a simplified example
        return f"Current weather in {city}: 22°C, Partly Cloudy"

# Create an instance of the tool
weather_tool = WeatherTool()

# Then add it to the agent's tools list
agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone,
           DuckDuckGoSearchTool(), weather_tool],  # Add the new tool here
    # ... other configuration remains the same
)
```

## Best Practices for Tool Development

When creating tools for your agent, consider these best practices:

1. **Clear Description**: Provide a clear description of what the tool does
2. **Detailed Parameter Docs**: Document each parameter with type and description
3. **Error Handling**: Handle exceptions gracefully with informative messages
4. **Input Validation**: Validate inputs to prevent unexpected behavior
5. **Return Type**: Ensure the return type matches the declared output_type
6. **Statelessness**: Prefer stateless tools when possible
7. **Modularity**: Design tools for a single responsibility
8. **Dependencies**: Check for required dependencies and provide guidance for installation

By following these guidelines, you can create effective tools that enhance your agent's capabilities.
