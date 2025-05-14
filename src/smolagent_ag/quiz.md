# Code Review Assessment 📚

This feedback should help you improve your skills.

> ⛔️ The feedback uses Qwen/Qwen2.5-Coder-32B-Instruct to compare your response to a gold standard solution. As we know, LLMs are not perfect. You should compare your work against the assessment criteria if you doubt the feedback.

## Question 1: Create a Basic Code Agent with Web Search Capability

**Your Solution:**
```python
# Create a CodeAgent with DuckDuckGo search capability
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

# Initialize the search tool
search_tool = DuckDuckGoSearchTool()
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    custom_role_conversions=None,
)

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],  # Add search tool here
    model=model,  # Add model here
)
```

**Reference Solution:**
```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")
)
```

### Assessment Criteria:
- Correct imports are included
- DuckDuckGoSearchTool is added to tools list
- HfApiModel is properly configured
- Model ID is correctly specified

### Feedback:
**Overall Assessment**

The student's solution meets the assessment criteria and demonstrates a good understanding of the task. Here is a detailed breakdown of the feedback for each criterion:

- **Correct imports are included**
  ✅ The student correctly imported the necessary modules from the smolagents package.

- **DuckDuckGoSearchTool is added to tools list**
  ✅ The student added the DuckDuckGoSearchTool to the tools list in the CodeAgent initialization.

- **HfApiModel is properly configured**
  ✅ The student properly configured the HfApiModel with additional parameters such as max_tokens, temperature, and model_id.

- **Model ID is correctly specified**
  ✅ The student correctly specified the model ID as 'Qwen/Qwen2.5-Coder-32B-Instruct'.

## Question 2: Set Up a Multi-Agent System with Manager and Web Search Agents

**Your Solution:**
```python
from smolagents import (
    ToolCallingAgent,
    CodeAgent,
    GoogleSearchTool,
    HfApiModel,
    VisitWebpageTool,
    FinalAnswerTool,
)

model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct", provider="together")
# Create web agent and manager agent structure
web_agent = ToolCallingAgent(
    tools=[
        GoogleSearchTool(provider="serper"),
        VisitWebpageTool(),
    ],  # Add required tools
    model=model,  # Add model
    max_steps=5,  # Adjust steps
    name="web_agent",
    description="Browses the web to find information",
)

manager_model = HfApiModel("deepseek-ai/DeepSeek-R1", provider="together")
manager_agent = CodeAgent(
    model=manager_model,
    managed_agents=[web_agent],
    tools=[FinalAnswerTool()],
    additional_authorized_imports=[
        "json",
        "pandas",
        "numpy",
    ],
    planning_interval=5,
    verbosity_level=2,
    max_steps=15,
)

manager_agent.run("find me the best places to visit in the world")
```

**Reference Solution:**
```python
web_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), visit_webpage],
    model=model,
    max_steps=10,
    name="search",
    description="Runs web searches for you."
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[web_agent],
    additional_authorized_imports=["time", "numpy", "pandas"]
)
```

### Assessment Criteria:
- Web agent has correct tools configured
- Manager agent properly references web agent
- Appropriate max_steps value is set
- Required imports are authorized

### Feedback:
**Overall Assessment**

The student's solution meets the assessment criteria with some minor adjustments needed.

- **Web agent has correct tools configured**
  ✅ The web agent is configured with GoogleSearchTool and VisitWebpageTool, which are appropriate tools for web searching and browsing.

- **Manager agent properly references web agent**
  ✅ The manager agent correctly references the web agent in its managed_agents list.

- **Appropriate max_steps value is set**
  ❌ The web agent has a max_steps value of 5, which might be too low for complex tasks. The manager agent has a max_steps value of 15, which is reasonable.

- **Required imports are authorized**
  ✅ The manager agent authorizes the necessary imports: json, pandas, and numpy.

## Question 3: Configure Agent Security Settings

**Your Solution:**
```python
from smolagents import CodeAgent, E2BSandbox

agent = CodeAgent(
    tools=[], model=model, sandbox=E2BSandbox(), additional_authorized_imports=["numpy"]
)
```

**Reference Solution:**
```python
from smolagents import CodeAgent, E2BSandbox

agent = CodeAgent(
    tools=[],
    model=model,
    sandbox=E2BSandbox(),
    additional_authorized_imports=["numpy"]
)
```

### Assessment Criteria:
- E2B sandbox is properly configured
- Authorized imports are appropriately limited
- Security settings are correctly implemented
- Basic agent configuration is maintained

### Feedback:
**Overall Assessment**

The student's solution is identical to the reference solution, which means it meets all the assessment criteria. The E2B sandbox is properly configured, the authorized imports are appropriately limited to only 'numpy', and the security settings are correctly implemented as per the reference solution. The basic agent configuration is also maintained. No further changes are needed.

- **E2B sandbox is properly configured**
  ✅ The E2B sandbox is correctly instantiated and passed to the CodeAgent.

- **Authorized imports are appropriately limited**
  ✅ The authorized imports are limited to only 'numpy', which is the same as in the reference solution.

- **Security settings are correctly implemented**
  ✅ The security settings are correctly implemented as per the reference solution, with no unauthorized imports or other security issues.

- **Basic agent configuration is maintained**
  ✅ The basic agent configuration is maintained, with the tools, model, sandbox, and additional_authorized_imports parameters set correctly.

## Question 4: Implement a Tool-Calling Agent

**Your Solution:**
```python
# External imports
from smolagents import (
    DuckDuckGoSearchTool,
    VisitWebpageTool,
    ToolCallingAgent,
    HfApiModel,
)

agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=HfApiModel("deepseek-ai/DeepSeek-R1", provider="together"),
    max_steps=5,
    "name"="tool_calling_agent",
    "description"="Agent can visit WebPages",
)

agent.run(
    "Search for the best music recommendations for a party at the Wayne's mansion."
)
```

**Reference Solution:**
```python
from smolagents import ToolCallingAgent

agent = ToolCallingAgent(
    tools=[custom_tool],
    model=model,
    max_steps=5,
    name="tool_agent",
    description="Executes specific tools based on input"
)
```

### Assessment Criteria:
- Tools are properly configured
- Step limit is set appropriately
- Agent name and description are provided
- Basic configuration is complete

### Feedback:
**Overall Assessment**

The student's solution meets the assessment criteria with some minor issues.

- **Tools are properly configured**
  ✅ The student has used DuckDuckGoSearchTool and VisitWebpageTool, which are appropriate for the task. However, the VisitWebpageTool might not be fully functional without additional configuration.

- **Step limit is set appropriately**
  ✅ The student has set the max_steps to 5, which is a reasonable limit for the task.

- **Agent name and description are provided**
  ❌ The student has provided the agent name and description, but they are enclosed in quotes, which is incorrect syntax in Python.

- **Basic configuration is complete**
  ✅ The student has provided all the necessary configuration for the ToolCallingAgent, including tools, model, max_steps, name, and description.

## Question 5: Set Up Model Integration

**Your Solution:**
```python
from smolagents import HfApiModel, LiteLLMModel

# Hugging Face model
hf_model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")

# Alternative model via LiteLLM
other_model = LiteLLMModel("anthropic/claude-3-sonnet")
```

**Reference Solution:**
```python
from smolagents import HfApiModel, LiteLLMModel

# Hugging Face model
hf_model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")

# Alternative model via LiteLLM
other_model = LiteLLMModel("anthropic/claude-3-sonnet")
```

### Assessment Criteria:
- Correct model imports are included
- Model is properly initialized
- Model ID is correctly specified
- Alternative model option is provided

### Feedback:
**Overall Assessment**

The student's solution meets all the assessment criteria. The correct model imports are included, the models are properly initialized, the model IDs are correctly specified, and an alternative model option is provided. The solution is identical to the reference solution, which is a perfect match in terms of functionality and structure.

- **Correct model imports are included**
  ✅ The student's solution correctly imports HfApiModel and LiteLLMModel from the smolagents module.

- **Model is properly initialized**
  ✅ Both models are properly initialized with their respective constructors.

- **Model ID is correctly specified**
  ✅ The model IDs 'Qwen/Qwen2.5-Coder-32B-Instruct' and 'anthropic/claude-3-sonnet' are correctly specified for the HfApiModel and LiteLLMModel respectively.

- **Alternative model option is provided**
  ✅ The student's solution provides an alternative model option using LiteLLMModel with the model ID 'anthropic/claude-3-sonnet'.
