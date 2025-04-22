# Agent Architecture

The First Agent is built on the SmolaAgent framework, which provides a structured approach to creating AI agents. This document explains the overall architecture of the agent, its main components, and how they interact.

## High-Level Architecture

The agent follows a modular architecture with the following key components:

1. **Language Model (LLM)** - The brain of the agent, responsible for understanding user queries and generating responses
2. **Tools** - Specialized functions that the agent can use to perform tasks
3. **Prompt Templates** - Guide the agent's behavior and thinking process
4. **Web Interface** - Allows users to interact with the agent

```
        ┌────────────────────────────┐
        │    User                    │
        │  (via Gradio or Streamlit) │
        └─────────────┬──────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────┐
│                 Agent Core                    │
│  ┌───────────────┐      ┌──────────────────┐  │
│  │    LLM        │◄────►│  Prompt Templates│  │
│  │(Qwen2.5-Coder)│      │  (prompts.yaml)  │  │
│  └──────┬────────┘      └──────────────────┘  │
│         │                                     │
│         ▼                                     │
│  ┌─────────────┐                              │
│  │   Tools     │                              │
│  │ Management  │                              │
│  └─────────────┘                              │
└───────────┬───────────────────────────────────┘
            │
            ▼
┌─────────────────────────────┐
│      Available Tools        │
│                             │
│ ┌─────────────────────────┐ │
│ │   get_current_time      │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │     web_search          │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ visit_webpage (unused)  │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │   final_answer          │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │   my_custom_tool        │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

## Core Components

### 1. Language Model

The agent uses the Qwen2.5-Coder model via the Hugging Face API. This model is configured in `app.py`:

```python
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud",
    custom_role_conversions=None,
)
```

The model is responsible for:
- Understanding user queries
- Planning a step-by-step approach to solve tasks
- Generating code to execute tools
- Formulating final answers

### 2. CodeAgent

The agent is implemented as an instance of the `CodeAgent` class, which is specialized for problem-solving using code execution:

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

Key parameters:
- `model`: The language model instance
- `tools`: List of tools available to the agent
- `max_steps`: Maximum number of steps for solving a task
- `verbosity_level`: How detailed the agent's responses should be
- `prompt_templates`: Templates that guide the agent's behavior

### 3. Tools

Tools are specialized functions that extend the agent's capabilities. The agent includes several tools:

- **FinalAnswerTool** (`tools/final_answer.py`): Used to provide the final response to a user query
- **DuckDuckGoSearchTool** (`tools/web_search.py`): Enables web searches to retrieve information
- **VisitWebpageTool** (`tools/visit_webpage.py`): Fetches and parses content from websites
- **get_current_time_in_timezone** (function in `app.py`): Gets current time in different timezones
- **my_custom_tool** (function in `app.py`): A template for custom functionality

Each tool has a standardized interface including:
- Name
- Description
- Input parameters
- Output type
- Implementation logic

### 4. Prompt Templates

The `prompts.yaml` file contains templates that guide the agent's behavior. These include:

- **System prompt**: The main instructions that define how the agent thinks and acts
- **Planning templates**: For initial planning and plan updates
- **Fact gathering templates**: For collecting and organizing facts
- **Managed agent templates**: For sub-agent coordination

### 5. Gradio UI

The `Gradio_UI.py` file implements the web interface using the Gradio library. Key components include:

- Chat interface
- Message formatting and display
- Agent interaction handling
- Optional file upload support

## Data Flow

Here's how data flows through the agent:

1. User submits a query via the Gradio UI
2. UI passes the query to the agent
3. Agent uses the LLM to plan a solution approach
4. Agent executes tools based on the plan
5. Agent collects results from tools
6. Agent formulates a final answer using the FinalAnswerTool
7. Response is formatted and displayed in the UI

## Execution Model

The agent follows a cycle of:

1. **Thought**: The agent reasons about the problem
2. **Code**: The agent writes Python code to execute tools and process information
3. **Observation**: The agent observes the results of code execution

This cycle continues until the agent arrives at a final answer or reaches the maximum number of steps.

## Extensibility

The architecture is designed to be extensible in several ways:

- **New tools** can be added to extend capabilities
- **Prompt templates** can be modified to change behavior
- **UI components** can be customized
- **Agent parameters** can be adjusted
- **Different models** can be used

This flexibility allows the agent to be adapted for various use cases and domains.
