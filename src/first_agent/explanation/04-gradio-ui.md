# Gradio UI

The Gradio UI component of the First Agent provides a web-based interface for users to interact with the agent. This document explains how the Gradio UI is implemented, its features, and how it integrates with the agent.

## Overview

The `Gradio_UI.py` file implements a web interface using the Gradio library, which is a popular framework for creating user interfaces for machine learning models. The interface allows users to:

- Submit queries through a chat interface
- See the agent's step-by-step thinking and tool usage
- View the final response
- (Optionally) Upload files for the agent to process

## Key Components

The Gradio UI implementation consists of several key components:

### 1. GradioUI Class

This is the main class that creates and manages the UI:

```python
class GradioUI:
    """A one-line interface to launch your agent in Gradio"""

    def __init__(self, agent: MultiStepAgent, file_upload_folder: str | None = None):
        if not _is_package_available("gradio"):
            raise ModuleNotFoundError(
                "Please install 'gradio' extra to use the GradioUI: `pip install 'smolagents[gradio]'`"
            )
        self.agent = agent
        self.file_upload_folder = file_upload_folder
        if self.file_upload_folder is not None:
            if not os.path.exists(file_upload_folder):
                os.mkdir(file_upload_folder)
```

This class takes two parameters:
- `agent`: The SmolaAgent instance to use for processing queries
- `file_upload_folder`: (Optional) A folder for storing uploaded files

### 2. interact_with_agent Method

This method handles user interaction with the agent:

```python
def interact_with_agent(self, prompt, messages):
    import gradio as gr

    messages.append(gr.ChatMessage(role="user", content=prompt))
    yield messages
    for msg in stream_to_gradio(self.agent, task=prompt, reset_agent_memory=False):
        messages.append(msg)
        yield messages
    yield messages
```

It:
1. Adds the user's prompt to the message list
2. Yields the updated messages to update the UI
3. Streams the agent's responses by calling `stream_to_gradio`
4. Updates the UI with each new message as it's generated

### 3. upload_file Method

If file upload is enabled, this method handles file uploads:

```python
def upload_file(
    self,
    file,
    file_uploads_log,
    allowed_file_types=(
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    ),
):
    """
    Handle file uploads, default allowed types are .pdf, .docx, and .txt
    """
    # Implementation details...
```

This method:
1. Validates the uploaded file type
2. Sanitizes the file name
3. Saves the file to the specified folder
4. Returns a status message and updates the file upload log

### 4. launch Method

This method creates and launches the Gradio interface:

```python
def launch(self, **kwargs):
    import gradio as gr

    with gr.Blocks(fill_height=True) as demo:
        stored_messages = gr.State([])
        file_uploads_log = gr.State([])
        chatbot = gr.Chatbot(
            label="Agent",
            type="messages",
            avatar_images=(
                None,
                "https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/communication/Alfred.png",
            ),
            resizeable=True,
            scale=1,
        )
        # File upload setup if enabled
        # ...
        text_input = gr.Textbox(lines=1, label="Chat Message")
        text_input.submit(
            self.log_user_message,
            [text_input, file_uploads_log],
            [stored_messages, text_input],
        ).then(self.interact_with_agent, [stored_messages, chatbot], [chatbot])

    demo.launch(debug=True, share=True, **kwargs)
```

This method:
1. Creates a Gradio Blocks interface
2. Sets up state variables for messages and file uploads
3. Creates a chatbot component with custom styling
4. Adds a text input for user messages
5. Sets up event handlers for user interactions
6. Launches the interface with the specified options

### 5. stream_to_gradio Function

This utility function converts agent steps into Gradio chat messages:

```python
def stream_to_gradio(
    agent,
    task: str,
    reset_agent_memory: bool = False,
    additional_args: dict | None = None,
):
    """Runs an agent with the given task and streams the messages from the agent as gradio ChatMessages."""
    # Implementation details...
```

This function:
1. Runs the agent with the given task
2. Streams each step of the agent's execution as Gradio chat messages
3. Formats different types of agent outputs (text, images, audio)
4. Handles errors in agent execution

### 6. pull_messages_from_step Function

This helper function extracts chat messages from agent steps:

```python
def pull_messages_from_step(
    step_log: MemoryStep,
):
    """Extract ChatMessage objects from agent steps with proper nesting"""
    # Implementation details...
```

This function:
1. Takes a memory step from the agent's execution
2. Extracts relevant information (thoughts, tool calls, observations, errors)
3. Formats this information as Gradio ChatMessage objects
4. Handles nesting of messages for better readability

## UI Workflow

The Gradio UI implements a conversation workflow:

1. **User Input**: User types a message in the text input box and submits it
2. **Message Processing**: The message is added to the conversation history
3. **Agent Execution**: The agent processes the message and generates responses
4. **Response Streaming**: The agent's responses are streamed to the UI
5. **Final Answer**: The agent provides a final answer
6. **Status Update**: The UI shows whether the agent completed successfully

This workflow creates a natural conversation experience where users can see the agent's thinking process.

## Message Formatting

The UI formats different types of messages:

### Thought Messages

The agent's reasoning is displayed as regular chat messages:

```
I need to find the current time in Tokyo. I can use the get_current_time_in_timezone tool with "Asia/Tokyo" as the timezone parameter.
```

### Tool Calls

Tool calls are displayed with a tool icon and name:

```
🛠️ Used tool get_current_time_in_timezone

timezone="Asia/Tokyo"
```

### Execution Logs

Execution results are displayed as nested messages:

```
📝 Execution Logs

The current local time in Asia/Tokyo is: 2025-03-26 22:45:12
```

### Errors

Errors are displayed with an error icon:

```
💥 Error

Error message details...
```

### Final Answer

The final answer is prominently displayed:

```
Final answer: The current local time in Tokyo is 2025-03-26 22:45:12
```

## File Upload Feature

The UI includes an optional file upload feature that:

1. Allows users to upload files in supported formats (PDF, DOCX, TXT by default)
2. Stores the files in a specified folder
3. Makes the files available to the agent for processing
4. Shows the upload status to the user

This feature is useful for agents that need to process documents or other files.

## Customization Options

The Gradio UI can be customized in several ways:

### Appearance

- Change avatar images
- Adjust layout and sizing
- Modify colors and styling

### Functionality

- Enable/disable file uploads
- Change allowed file types
- Add custom components
- Modify event handlers

### Deployment

- Change server host and port
- Enable/disable sharing
- Set debug mode
- Configure authentication

## Integration with the Agent

The UI is integrated with the agent through the `GradioUI` class:

```python
# In app.py
GradioUI(agent).launch(server_name="0.0.0.0", server_port=7860)
```

This creates a UI instance with the configured agent and launches it on the specified host and port.

The UI communicates with the agent by:
1. Sending user messages to the agent's `run` method
2. Receiving step logs from the agent's execution
3. Converting these logs to UI messages
4. Updating the UI with the agent's responses

## Example Usage

Here's how the UI is used in the First Agent:

```python
# Import the UI class
from Gradio_UI import GradioUI

# Configure the agent
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

# Launch the UI
GradioUI(agent).launch(server_name="0.0.0.0", server_port=7860)
```

This creates a web interface that users can access at `http://localhost:7860` to interact with the agent.

## Best Practices

When working with the Gradio UI, consider these best practices:

1. **Error Handling**: Ensure errors are caught and displayed to the user
2. **Progress Indication**: Show status messages for long-running operations
3. **Responsive Design**: Create interfaces that work well on different devices
4. **Clear Instructions**: Provide guidance on how to use the interface
5. **Consistent Styling**: Maintain a consistent visual style
6. **Accessibility**: Ensure the interface is accessible to all users
7. **Security**: Validate and sanitize user inputs and uploaded files
8. **Performance**: Optimize for efficient message streaming and rendering

By following these guidelines, you can create effective user interfaces for your agents.
