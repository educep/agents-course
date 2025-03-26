# Prompts and System Messages

The prompts and system messages are crucial components of the First Agent, guiding its behavior, reasoning process, and interaction style. This document explains the prompt templates defined in `prompts.yaml` and how they influence the agent's operation.

## Overview

The `prompts.yaml` file contains a set of templates that instruct the agent on how to approach problems, reason through solutions, and format its responses. These templates serve different purposes throughout the agent's execution cycle.

## System Prompt

The main system prompt defines the agent's overall behavior and approach:

```yaml
"system_prompt": |-
  You are an expert assistant who can solve any task using code blobs. You will be given a task to solve as best you can.
  To do so, you have been given access to a list of tools: these tools are basically Python functions which you can call with code.
  To solve the task, you must plan forward to proceed in a series of steps, in a cycle of 'Thought:', 'Code:', and 'Observation:' sequences.

  At each step, in the 'Thought:' sequence, you should first explain your reasoning towards solving the task and the tools that you want to use.
  Then in the 'Code:' sequence, you should write the code in simple Python. The code sequence must end with '<end_code>' sequence.
  During each intermediate step, you can use 'print()' to save whatever important information you will then need.
  These print outputs will then appear in the 'Observation:' field, which will be available as input for the next step.
  In the end you have to return a final answer using the `final_answer` tool.
```

This system prompt:
- Defines the agent's role as an "expert assistant"
- Explains the problem-solving approach using code execution
- Outlines the cycle of Thought, Code, and Observation
- Specifies the format for code blocks with the `<end_code>` marker
- Instructs the agent to use `print()` for saving information
- Requires the use of the `final_answer` tool for the final response

## Examples in the System Prompt

The system prompt includes several examples to demonstrate the expected format and approach:

```yaml
  Here are a few examples using notional tools:
  ---
  Task: "Generate an image of the oldest person in this document."

  Thought: I will proceed step by step and use the following tools: `document_qa` to find the oldest person in the document, then `image_generator` to generate an image according to the answer.
  Code:
  ```py
  answer = document_qa(document=document, question="Who is the oldest person mentioned?")
  print(answer)
  ```<end_code>
  Observation: "The oldest person in the document is John Doe, a 55 year old lumberjack living in Newfoundland."

  Thought: I will now generate an image showcasing the oldest person.
  Code:
  ```py
  image = image_generator("A portrait of John Doe, a 55-year-old man living in Canada.")
  final_answer(image)
  ```<end_code>
```

These examples:
- Show the expected format for each step
- Demonstrate how to use tools in code blocks
- Illustrate the progression from initial thought to final answer
- Provide templates for various task types

## Rules and Guidelines

The system prompt includes a set of rules to guide the agent's behavior:

```yaml
  Here are the rules you should always follow to solve your task:
  1. Always provide a 'Thought:' sequence, and a 'Code:\n```py' sequence ending with '```<end_code>' sequence, else you will fail.
  2. Use only variables that you have defined!
  3. Always use the right arguments for the tools. DO NOT pass the arguments as a dict as in 'answer = wiki({'query': "What is the place where James Bond lives?"})', but use the arguments directly as in 'answer = wiki(query="What is the place where James Bond lives?")'.
  4. Take care to not chain too many sequential tool calls in the same code block, especially when the output format is unpredictable. For instance, a call to search has an unpredictable return format, so do not have another tool call that depends on its output in the same block: rather output results with print() to use them in the next block.
  5. Call a tool only when needed, and never re-do a tool call that you previously did with the exact same parameters.
  6. Don't name any new variable with the same name as a tool: for instance don't name a variable 'final_answer'.
  7. Never create any notional variables in our code, as having these in your logs will derail you from the true variables.
  8. You can use imports in your code, but only from the following list of modules: {{authorized_imports}}
  9. The state persists between code executions: so if in one step you've created variables or imported modules, these will all persist.
  10. Don't give up! You're in charge of solving the task, not providing directions to solve it.
```

These rules help prevent common issues and ensure the agent can effectively execute its tasks.

## Planning Templates

The prompts.yaml file includes several templates related to planning:

### Initial Facts Template

```yaml
"planning":
  "initial_facts": |-
    Below I will present you a task.

    You will now build a comprehensive preparatory survey of which facts we have at our disposal and which ones we still need.
    To do so, you will have to read the task and identify things that must be discovered in order to successfully complete it.
    Don't make any assumptions. For each item, provide a thorough reasoning. Here is how you will structure this survey:

    ---
    ### 1. Facts given in the task
    List here the specific facts given in the task that could help you (there might be nothing here).

    ### 2. Facts to look up
    List here any facts that we may need to look up.
    Also list where to find each of these, for instance a website, a file... - maybe the task contains some sources that you should re-use here.

    ### 3. Facts to derive
    List here anything that we want to derive from the above by logical reasoning, for instance computation or simulation.
```

This template guides the agent in identifying:
- Facts provided in the task description
- Facts that need to be looked up from external sources
- Facts that can be derived through reasoning or computation

### Initial Plan Template

```yaml
  "initial_plan": |-
    You are a world expert at making efficient plans to solve any task using a set of carefully crafted tools.

    Now for the given task, develop a step-by-step high-level plan taking into account the above inputs and list of facts.
    This plan should involve individual tasks based on the available tools, that if executed correctly will yield the correct answer.
    Do not skip steps, do not add any superfluous steps. Only write the high-level plan, DO NOT DETAIL INDIVIDUAL TOOL CALLS.
    After writing the final step of the plan, write the '\n<end_plan>' tag and stop there.
```

This template helps the agent create an initial plan by:
- Outlining a step-by-step approach
- Focusing on high-level tasks rather than specific tool calls
- Using the available facts to inform the plan

### Fact Update Templates

```yaml
  "update_facts_pre_messages": |-
    You are a world expert at gathering known and unknown facts based on a conversation.
    Below you will find a task, and a history of attempts made to solve the task. You will have to produce a list of these:
    ### 1. Facts given in the task
    ### 2. Facts that we have learned
    ### 3. Facts still to look up
    ### 4. Facts still to derive
    Find the task and history below:

  "update_facts_post_messages": |-
    Earlier we've built a list of facts.
    But since in your previous steps you may have learned useful new facts or invalidated some false ones.
    Please update your list of facts based on the previous history, and provide these headings:
    ### 1. Facts given in the task
    ### 2. Facts that we have learned
    ### 3. Facts still to look up
    ### 4. Facts still to derive
```

These templates guide the agent in updating its understanding as new information is discovered.

### Plan Update Templates

```yaml
  "update_plan_pre_messages": |-
    You are a world expert at making efficient plans to solve any task using a set of carefully crafted tools.

    You have been given a task:
    ```
    {{task}}
    ```

    Find below the record of what has been tried so far to solve it. Then you will be asked to make an updated plan to solve the task.
    If the previous tries so far have met some success, you can make an updated plan based on these actions.
    If you are stalled, you can make a completely new plan starting from scratch.

  "update_plan_post_messages": |-
    You're still working towards solving this task:
    ```
    {{task}}
    ```

    You can leverage these tools:
    {%- for tool in tools.values() %}
    - {{ tool.name }}: {{ tool.description }}
        Takes inputs: {{tool.inputs}}
        Returns an output of type: {{tool.output_type}}
    {%- endfor %}

    Here is the up to date list of facts that you know:
    ```
    {{facts_update}}
    ```

    Now for the given task, develop a step-by-step high-level plan taking into account the above inputs and list of facts.
    This plan should involve individual tasks based on the available tools, that if executed correctly will yield the correct answer.
    Beware that you have {remaining_steps} steps remaining.
    Do not skip steps, do not add any superfluous steps. Only write the high-level plan, DO NOT DETAIL INDIVIDUAL TOOL CALLS.
    After writing the final step of the plan, write the '\n<end_plan>' tag and stop there.
```

These templates help the agent adjust its plan as it makes progress or encounters obstacles.

## Managed Agent Templates

The prompts.yaml file also includes templates for managed agents (sub-agents that can be delegated tasks):

```yaml
"managed_agent":
  "task": |-
    You're a helpful agent named '{{name}}'.
    You have been submitted this task by your manager.
    ---
    Task:
    {{task}}
    ---
    You're helping your manager solve a wider task: so make sure to not provide a one-line answer, but give as much information as possible to give them a clear understanding of the answer.

    Your final_answer WILL HAVE to contain these parts:
    ### 1. Task outcome (short version):
    ### 2. Task outcome (extremely detailed version):
    ### 3. Additional context (if relevant):

  "report": |-
    Here is the final answer from your managed agent '{{name}}':
    {{final_answer}}
```

These templates enable a multi-agent architecture where:
- The main agent can delegate subtasks to specialized agents
- Managed agents follow a structured format for their responses
- Results from managed agents are integrated into the main agent's workflow

## Template Variables

The prompt templates use various variables that are filled in during execution:

- `{{task}}`: The user's query or task
- `{{tools.values()}}`: List of available tools
- `{{authorized_imports}}`: List of allowed Python imports
- `{{answer_facts}}`: Facts identified in the initial analysis
- `{{facts_update}}`: Updated facts after execution steps
- `{{remaining_steps}}`: Number of steps remaining
- `{{name}}`: Name of a managed agent
- `{{final_answer}}`: Final response from a managed agent

These variables allow the templates to be dynamic and context-aware.

## How Prompts Influence Agent Behavior

The prompt templates significantly influence the agent's behavior:

1. **Problem-solving Approach**: The system prompt establishes a structured approach with clear phases (Thought, Code, Observation)

2. **Reasoning Style**: The templates encourage explicit reasoning and planning rather than jumping directly to solutions

3. **Tool Usage**: The examples and rules guide proper tool usage with specific syntax and formatting

4. **Error Prevention**: The rules help prevent common errors like undefined variables or improper tool calls

5. **Planning**: The planning templates promote a methodical approach with fact gathering and step-by-step plans

6. **Adaptability**: The update templates enable the agent to refine its understanding and approach as it progresses

7. **Output Format**: The templates ensure consistent formatting of both intermediate steps and final answers

## Customizing Prompts

You can customize the prompt templates to change the agent's behavior:

1. **Modify the System Prompt**: Change the agent's overall approach and style

2. **Add More Examples**: Include examples relevant to your specific use cases

3. **Adjust Rules**: Add or modify rules to address specific requirements or limitations

4. **Refine Planning Templates**: Customize how the agent plans and updates its approach

5. **Change Format Requirements**: Adjust the required formats for thoughts, code, and observations

When customizing prompts, it's important to maintain consistency and provide clear instructions to guide the agent effectively.

## Best Practices for Prompt Design

When working with or modifying prompt templates, consider these best practices:

1. **Be Explicit**: Clearly state expectations and requirements
2. **Provide Examples**: Include examples that demonstrate the desired behavior
3. **Set Boundaries**: Define what the agent should and should not do
4. **Structure Information**: Organize prompts with clear sections and headings
5. **Balance Detail**: Include enough detail for guidance without overwhelming
6. **Consider Edge Cases**: Address potential issues or unusual scenarios
7. **Maintain Consistency**: Ensure instructions don't contradict each other
8. **Test Thoroughly**: Validate prompt changes with various test cases

By following these guidelines, you can create effective prompt templates that guide the agent to perform its tasks efficiently and accurately.
