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
    model=model,
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
  ✅ The web agent is configured with the correct tools: GoogleSearchTool and VisitWebpageTool.

- **Manager agent properly references web agent**
  ❌ The manager agent is configured with the correct web agent, but the model used for the manager agent should be 'manager_model' instead of 'model'.

- **Appropriate max_steps value is set**
  ✅ The max_steps value for both agents is set appropriately.

- **Required imports are authorized**
  ✅ The required imports are authorized in the manager agent.

## Question 3: Configure Agent Security Settings

**Your Solution:**
```python
# Set up secure code execution environment
from smolagents import CodeAgent

manager_model = HfApiModel("deepseek-ai/DeepSeek-R1", provider="together")
agent = CodeAgent(
    tools=[],
    model=model,
    executor_type="e2b",
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

The student's solution has some issues that need to be addressed to meet the assessment criteria.

- **E2B sandbox is properly configured**
  ❌ The student's solution does not use the E2BSandbox class as specified in the reference solution. Instead, it uses an executor_type parameter which is not mentioned in the reference solution. This indicates that the E2B sandbox is not properly configured.

- **Authorized imports are appropriately limited**
  ❌ The student's solution does not specify any authorized imports, which means that the agent can potentially import any module, which is a security risk. The reference solution specifies 'numpy' as an additional authorized import, which is a good practice to limit the imports to only those that are necessary.

- **Security settings are correctly implemented**
  ❌ The student's solution does not implement any security settings that are specified in the reference solution. The reference solution specifies the use of the E2BSandbox and limits the authorized imports, which are important security measures. The student's solution does not include these security measures.

- **Basic agent configuration is maintained**
  ❌ The student's solution does not maintain the basic agent configuration as specified in the reference solution. The reference solution specifies the use of the CodeAgent class with a model parameter, while the student's solution uses a manager_model variable and does not specify the model parameter. This indicates that the basic agent configuration is not maintained.

## Question 4: Implement a Tool-Calling Agent

**Your Solution:**
```python
# External imports
from smolagents import (
    DuckDuckGoSearchTool,
    VisitWebpageTool,
)

manager_model = HfApiModel("deepseek-ai/DeepSeek-R1", provider="together")

agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=manager_model,
    "name"="tool_calling_agent",
    "description"="Agent can visit WebPages",
)

step_log_tool = agent.run(
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

The student's solution is mostly correct but has a few issues that need to be addressed.

- **Tools are properly configured**
  ✅ The student has correctly configured the tools by passing instances of DuckDuckGoSearchTool and VisitWebpageTool to the ToolCallingAgent.

- **Step limit is set appropriately**
  ❌ The student has not set the step limit, which is a required parameter for the ToolCallingAgent.

- **Agent name and description are provided**
  ❌ The student has incorrectly used quotes around the keys for the name and description parameters, which will cause a syntax error.

- **Basic configuration is complete**
  ❌ The student's solution is missing the step limit parameter and has syntax errors in the name and description parameters.

## Question 5: Set Up Model Integration

**Your Solution:**
```python
# Configure model integration
from smolagents import HfApiModel

model = HfApiModel("deepseek-ai/DeepSeek-R1", provider="together")

alt_model = LiteLLMModel(
    model_id="deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    temperature=0.0,
)
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

The student's solution meets the assessment criteria with some minor adjustments needed.

- **Correct model imports are included**
  ✅ The student correctly imported HfApiModel from smolagents. However, LiteLLMModel was not imported, which is required for the alternative model option.

- **Model is properly initialized**
  ✅ Both models are properly initialized with the required parameters.

- **Model ID is correctly specified**
  ❌ The model ID for the HfApiModel is correct, but the model ID for the LiteLLMModel is incorrect. The reference solution uses 'anthropic/claude-3-sonnet', while the student's solution uses 'deepseek-chat'.

- **Alternative model option is provided**
  ❌ The alternative model option is provided, but it is not correctly initialized. The LiteLLMModel is not imported, and the model ID is incorrect.
