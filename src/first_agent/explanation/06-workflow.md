# Workflow and Execution

This document explains how the First Agent processes and responds to user queries, detailing the execution workflow from user input to final response.

## Execution Flow Overview

The First Agent follows a structured workflow when processing user queries:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   User Input    │────▶│   Agent Plans   │────▶│ Execute & Adapt │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
┌─────────────────┐     ┌─────────────────┐             │
│                 │     │                 │             │
│  Final Answer   │◀────│ Process Results │◀────────────┘
│                 │     │                 │
└─────────────────┘     └─────────────────┘
```

## Step 1: Receiving User Input

The process begins when a user submits a query through the Gradio UI:

```python
# In Gradio_UI.py
def interact_with_agent(self, prompt, messages):
    messages.append(gr.ChatMessage(role="user", content=prompt))
    yield messages
    for msg in stream_to_gradio(self.agent, task=prompt, reset_agent_memory=False):
        messages.append(msg)
        yield messages
    yield messages
```

The UI:
1. Adds the user's message to the conversation history
2. Calls the agent's run method with the user's query
3. Streams the agent's responses back to the UI

## Step 2: Planning the Approach

Before taking action, the agent plans its approach:

### Initial Fact Gathering

If planning is enabled, the agent first identifies facts from the user query:

```
### 1. Facts given in the task
- The user wants to know the current time in Tokyo

### 2. Facts to look up
- The current time in Tokyo timezone (Asia/Tokyo)

### 3. Facts to derive
- None required for this simple task
```

### Initial Plan Creation

The agent then creates a step-by-step plan:

```
1. Determine the correct timezone identifier for Tokyo
2. Use the get_current_time_in_timezone tool with the Tokyo timezone
3. Format the result and provide the final answer

<end_plan>
```

## Step 3: Task Execution

The agent executes its plan through a cycle of Thought, Code, and Observation:

### Thinking Phase

The agent first reasons about what to do:

```
Thought: I need to find the current time in Tokyo. I can use the get_current_time_in_timezone tool with "Asia/Tokyo" as the timezone parameter.
```

This phase shows the agent's reasoning process and decision-making.

### Code Generation Phase

The agent then generates Python code to execute its plan:

```
Code:
```py
result = get_current_time_in_timezone(timezone="Asia/Tokyo")
print(result)
```<end_code>
```

This code:
1. Calls the appropriate tool with the necessary parameters
2. Uses `print()` to output the result for observation

### Observation Phase

The agent observes the results of executing the code:

```
Observation: "The current local time in Asia/Tokyo is: 2025-03-26 22:45:12"
```

These observations inform the agent's next steps.

### Adaptive Cycle

The agent repeats this cycle, adapting as needed:

```
Thought: I now have the current time in Tokyo. I can provide this as the final answer.

Code:
```py
final_answer("The current local time in Tokyo is 2025-03-26 22:45:12")
```<end_code>
```

For more complex tasks, the agent might:
- Execute multiple tools
- Process intermediate results
- Handle errors or unexpected outcomes
- Update its plan based on new information

## Step 4: Code Execution

The agent doesn't just generate code—it actually executes it:

```python
# In CodeAgent class (SmolaAgent framework)
code_output = self._execute_code(code)
```

This execution:
1. Sets up a safe execution environment
2. Runs the generated Python code
3. Captures outputs from `print()` statements
4. Handles errors and exceptions
5. Returns the results for the agent to observe

The code execution maintains state between steps, allowing the agent to build on previous results.

## Step 5: Final Answer Generation

Once the agent has gathered all necessary information, it provides a final answer:

```
Code:
```py
final_answer("The current local time in Tokyo is 2025-03-26 22:45:12")
```<end_code>
```

The `final_answer` tool:
1. Marks the completion of the task
2. Formats the response appropriately
3. Returns the result to the user

## Step 6: UI Response Formatting

The Gradio UI formats the agent's responses for display:

```python
# In stream_to_gradio function
if isinstance(final_answer, AgentText):
    yield gr.ChatMessage(
        role="assistant",
        content=f"**Final answer:**\n{final_answer.to_string()}\n",
    )
```

This creates a clear and readable presentation of the agent's response.

## Complete Example Workflow

Here's a complete example of how the agent processes a simple query:

### User Query
```
What time is it in Tokyo?
```

### Agent Planning (Internal)
```
### Facts given in the task
- User wants to know the current time in Tokyo

### Initial Plan
1. Identify the correct timezone for Tokyo
2. Use the get_current_time_in_timezone tool
3. Return the result as the final answer
```

### Execution Step 1
```
Thought: I need to find the current time in Tokyo. I can use the get_current_time_in_timezone tool with "Asia/Tokyo" as the timezone parameter.

Code:
```py
result = get_current_time_in_timezone(timezone="Asia/Tokyo")
print(result)
```<end_code>

Observation: "The current local time in Asia/Tokyo is: 2025-03-26 22:45:12"
```

### Execution Step 2
```
Thought: I now have the current time in Tokyo. I can provide this as the final answer.

Code:
```py
final_answer("The current local time in Tokyo is 2025-03-26 22:45:12")
```<end_code>
```

### Final Answer (User-Visible)
```
Final answer: The current local time in Tokyo is 2025-03-26 22:45:12
```

## Complex Task Handling

For more complex tasks, the agent follows the same general workflow but may:

1. **Execute Multiple Tools**: Combine various tools to solve different aspects of the task
2. **Process and Transform Data**: Manipulate data between tool calls
3. **Handle Edge Cases**: Deal with errors or unexpected results
4. **Adapt the Plan**: Update its approach based on intermediate results
5. **Break Down Complex Tasks**: Split complex tasks into manageable subtasks

### Example: Weather Comparison Task
For a query like "Which is warmer today, Tokyo or New York?", the agent might:

1. Get the current time in both cities
2. Use a weather tool to check the temperature in each city
3. Compare the temperatures
4. Provide a conclusion as the final answer

## Error Handling

The agent includes several layers of error handling:

### Code Execution Errors
```
Thought: I'll try to get the weather in Tokyo.

Code:
```py
weather = get_weather("Tokyo")
print(weather)
```<end_code>

Observation: Error: 'get_weather' is not defined
```

When encountering errors, the agent:
1. Recognizes the error in the observation
2. Adjusts its approach in the next step
3. Tries an alternative method

### Tool-specific Errors
```
Thought: I'll try to get the time in an invalid timezone.

Code:
```py
result = get_current_time_in_timezone(timezone="Invalid/Zone")
print(result)
```<end_code>

Observation: "Error fetching time for timezone 'Invalid/Zone': 'Invalid/Zone' is not a valid timezone"
```

Tools include their own error handling to provide informative messages.

### Recovery Strategy
When errors occur, the agent typically:
1. Acknowledges the error
2. Identifies the cause
3. Attempts an alternative approach
4. If necessary, explains limitations in the final answer

## Performance Considerations

The execution workflow includes several factors that affect performance:

1. **Model Response Time**: The time taken by the LLM to generate responses
2. **Tool Execution Time**: Time required to execute external tools
3. **Step Count**: Number of steps needed to solve a task
4. **UI Rendering**: Time to display responses in the Gradio interface

To optimize performance, the agent:
- Limits the maximum number of steps (`max_steps=6`)
- Uses efficient tools
- Streams responses progressively
- Focuses on direct problem-solving rather than verbose explanations

## Best Practices for Efficient Execution

When working with the agent, consider these best practices:

1. **Clear Queries**: Provide clear and specific queries to reduce the number of steps needed
2. **Appropriate Tool Selection**: Ensure the right tools are available for common tasks
3. **Prompt Optimization**: Refine system prompts to guide efficient problem-solving
4. **Step Limitation**: Set reasonable limits on the number of execution steps
5. **Error Resilience**: Design tools with robust error handling
6. **State Management**: Be mindful of state persistence between steps
7. **Progressive Response**: Use streaming to show progress during long-running tasks

By understanding the execution workflow and following these practices, you can create efficient and effective agent interactions.
