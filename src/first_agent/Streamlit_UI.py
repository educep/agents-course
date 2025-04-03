#!/usr/bin/env python
# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import mimetypes
import os
import re
from datetime import datetime
from typing import Any

import streamlit as st
from loguru import logger

# Importing different agent types that can handle various output formats (text, audio, images)
from smolagents.agent_types import AgentAudio, AgentImage, AgentText, handle_agent_output_types

# Core agent components: MultiStepAgent for complex tasks and ActionStep for tracking agent actions
from smolagents.agents import ActionStep, MultiStepAgent

# Memory component to help agents maintain context and history of their actions
from smolagents.memory import MemoryStep
from smolagents.utils import _is_package_available


def process_message_for_streamlit(content: str) -> str:
    """Process message content for proper rendering in Streamlit"""
    # Format content for Streamlit display
    content = content.strip()
    # Remove any trailing <end_code> and extra backticks, handling multiple possible formats
    content = re.sub(r"```\s*<end_code>", "```", content)
    content = re.sub(r"<end_code>\s*```", "```", content)
    content = re.sub(r"```\s*\n\s*<end_code>", "```", content)
    return content.strip()


def serialize_step_log(step_log: MemoryStep) -> dict[str, Any]:
    """Serialize step log to a dictionary format suitable for JSON"""
    serialized = {}

    if isinstance(step_log, ActionStep):
        # Basic information
        serialized["type"] = "ActionStep"
        serialized["step_number"] = (
            step_log.step_number if hasattr(step_log, "step_number") else None
        )
        serialized["timestamp"] = datetime.now().isoformat()

        # Model output
        if hasattr(step_log, "model_output"):
            serialized["model_output"] = step_log.model_output

        # Tool calls
        if hasattr(step_log, "tool_calls") and step_log.tool_calls:
            tool_call = step_log.tool_calls[0]
            serialized["tool_calls"] = {"name": tool_call.name, "arguments": tool_call.arguments}

        # Observations and errors
        if hasattr(step_log, "observations"):
            serialized["observations"] = step_log.observations
        if hasattr(step_log, "error"):
            serialized["error"] = str(step_log.error) if step_log.error else None

        # Performance metrics
        if hasattr(step_log, "input_token_count"):
            serialized["input_token_count"] = step_log.input_token_count
        if hasattr(step_log, "output_token_count"):
            serialized["output_token_count"] = step_log.output_token_count
        if hasattr(step_log, "duration"):
            serialized["duration"] = step_log.duration

    return serialized


def save_step_log(step_log: MemoryStep) -> None:
    """Save step log to a JSON file"""
    try:
        # Create logs directory if it doesn't exist
        log_dir = "agent_logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"step_log_{timestamp}.json"
        filepath = os.path.join(log_dir, filename)

        # Serialize and save
        serialized_log = serialize_step_log(step_log)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serialized_log, f, indent=2, ensure_ascii=False)

        logger.info(f"Step log saved to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save step log: {e}")


def render_step_log(step_log: MemoryStep, container) -> None:
    """Render a step log in the Streamlit UI"""
    # ActionStep represents a single action taken by the agent (like making a decision or using a tool)
    if isinstance(step_log, ActionStep):
        # save_step_log(step_log)
        # Output the step number
        step_number = f"Step {step_log.step_number}" if step_log.step_number is not None else ""
        if step_number:
            container.markdown(f"**{step_number}**")

        # Display the agent's reasoning/thought process before taking action
        if hasattr(step_log, "model_output") and step_log.model_output is not None:
            model_output = process_message_for_streamlit(step_log.model_output)
            container.markdown(model_output)

        # Handle and display the tools that the agent decided to use
        if hasattr(step_log, "tool_calls") and step_log.tool_calls is not None:
            first_tool_call = step_log.tool_calls[0]
            used_code = first_tool_call.name == "python_interpreter"

            # Process the arguments the agent passed to the tool
            args = first_tool_call.arguments
            if isinstance(args, dict):
                content = str(args.get("answer", str(args)))
            else:
                content = str(args).strip()

            if used_code:
                # Clean up the content by removing any end code tags
                content = re.sub(r"```.*?\n", "", content)
                content = re.sub(r"\s*<end_code>\s*", "", content)
                content = content.strip()
                if not content.startswith("```python"):
                    content = f"```python\n{content}\n```"

            # Display the tool usage in an expandable section
            container.markdown(f"🛠️ **Used tool {first_tool_call.name}**")
            with container.expander("Tool details", expanded=True):
                logger.info(f"tool_call content: {content}")
                container.markdown(content)

                # Show the results/logs from the tool execution
                if (
                    hasattr(step_log, "observations")
                    and step_log.observations
                    and step_log.observations.strip()
                ):
                    logger.info(step_log.observations.strip())
                    log_content = re.sub(r"^Execution logs:\s*", "", step_log.observations.strip())
                    if log_content:
                        container.markdown("📝 **Execution Logs**")
                        container.code(log_content)

                # Display any errors that occurred during tool execution
                if hasattr(step_log, "error") and step_log.error is not None:
                    container.markdown("💥 **Error**")
                    container.error(str(step_log.error))

        # Handle errors that occurred during the agent's decision-making process
        elif hasattr(step_log, "error") and step_log.error is not None:
            container.error(f"💥 **Error**: {str(step_log.error)}")

        # Display metrics about the agent's performance (tokens used and duration)
        step_footnote = f"{step_number}"
        if hasattr(step_log, "input_token_count") and hasattr(step_log, "output_token_count"):
            token_str = f" | Input-tokens:{step_log.input_token_count:,} | Output-tokens:{step_log.output_token_count:,}"
            step_footnote += token_str
        if hasattr(step_log, "duration"):
            step_duration = (
                f" | Duration: {round(float(step_log.duration), 2)}" if step_log.duration else ""
            )
            step_footnote += step_duration

        container.markdown(
            f"<span style='color: #bbbbc2; font-size: 12px;'>{step_footnote}</span>",
            unsafe_allow_html=True,
        )
        container.markdown("-----")


def stream_to_streamlit(
    agent,
    task: str,
    message_container,
    reset_agent_memory: bool = False,
    additional_args: dict[str, Any] | None = None,
) -> Any:
    """Runs an agent with the given task and streams the messages to a Streamlit container."""
    # Track token usage for the entire conversation
    total_input_tokens = 0
    total_output_tokens = 0

    # Add initial status message
    status_placeholder = message_container.empty()
    status_placeholder.info("🔄 Checking model connection...")

    step_containers = []
    final_answer = None

    try:
        # Run the agent with the given task, streaming its progress
        for step_log in agent.run(
            task, stream=True, reset=reset_agent_memory, additional_args=additional_args
        ):
            # Track token usage from the language model
            input_tokens = getattr(agent.model, "last_input_token_count", 0) or 0
            output_tokens = getattr(agent.model, "last_output_token_count", 0) or 0

            total_input_tokens += input_tokens
            total_output_tokens += output_tokens

            # Handle each action step from the agent
            if isinstance(step_log, ActionStep):
                step_log.input_token_count = input_tokens
                step_log.output_token_count = output_tokens

                # Create a new container for this step
                step_container = message_container.container()
                step_containers.append(step_container)
                render_step_log(step_log, step_container)

        # Last log is the run's final_answer
        final_answer = step_log
        final_answer = handle_agent_output_types(final_answer)

        # Process and display the agent's final response based on its type (text, image, or audio)
        result_container = message_container.container()

        if isinstance(final_answer, AgentText):
            logger.debug("is text")
            result_container.markdown(f"**Final answer:**\n{final_answer.to_string()}\n")
        elif isinstance(final_answer, AgentImage):
            result_container.markdown("**Final answer:**")
            # Get the actual image data/path from the AgentImage object
            image_data = final_answer.to_string()
            if image_data:
                result_container.image(image_data)
            else:
                result_container.error("Failed to load image data")
        elif isinstance(final_answer, AgentAudio):
            result_container.markdown("**Final answer:**")
            result_container.audio(final_answer.to_string())
        else:
            # If it's a FinalAnswerStep, try to extract the actual answer
            logger.debug(f"If it's a FinalAnswerStep, the actual answer: {final_answer}")
            if hasattr(final_answer, "final_answer"):
                actual_answer = final_answer.final_answer
                if isinstance(actual_answer, (AgentText, AgentImage, AgentAudio)):
                    if isinstance(actual_answer, AgentText):
                        result_container.markdown(
                            f"**Final answer:**\n{actual_answer.to_string()}\n"
                        )
                    elif isinstance(actual_answer, AgentImage):
                        result_container.markdown("**Final answer:**")
                        image_data = actual_answer.to_string()
                        if image_data:
                            result_container.image(image_data)
                        else:
                            result_container.error("Failed to load image data")
                    elif isinstance(actual_answer, AgentAudio):
                        result_container.markdown("**Final answer:**")
                        result_container.audio(actual_answer.to_string())
                else:
                    result_container.markdown(f"**Final answer:** {str(actual_answer)}")
            else:
                result_container.markdown(f"**Final answer:** {str(final_answer)}")

        # Update status message
        status_placeholder.success("✅ Model responded successfully")

    except Exception as e:
        # Update status with error message
        status_placeholder.error(f"❌ Error: Model failed to respond - {str(e)}")

    return final_answer


class StreamlitUI:
    """A one-line interface to launch your agent in Streamlit"""

    def __init__(self, agent: MultiStepAgent, file_upload_folder: str | None = None):
        # Initialize the UI with a MultiStepAgent that can handle complex, multi-step tasks
        if not _is_package_available("streamlit"):
            raise ModuleNotFoundError(
                "Please install 'streamlit' to use the StreamlitUI: `pip install streamlit`"
            )
        self.agent = agent
        self.file_upload_folder = file_upload_folder
        if self.file_upload_folder is not None and not os.path.exists(file_upload_folder):
            os.makedirs(file_upload_folder, exist_ok=True)

    def upload_file(
        self,
        uploaded_file,
        allowed_file_types=(
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        ),
    ):
        """
        Handle file uploads, default allowed types are .pdf, .docx, and .txt
        """
        if uploaded_file is None:
            return None, "No file uploaded"

        try:
            mime_type = uploaded_file.type
            if not mime_type:
                mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        except Exception as e:
            return None, f"Error: {e}"

        if mime_type not in allowed_file_types:
            return None, "File type disallowed"

        # Sanitize file name
        original_name = os.path.basename(uploaded_file.name)
        sanitized_name = re.sub(r"[^\w\-.]", "_", original_name)

        type_to_ext = {}
        for ext, t in mimetypes.types_map.items():
            if t not in type_to_ext:
                type_to_ext[t] = ext

        # Ensure the extension correlates to the mime type
        sanitized_name_parts = sanitized_name.split(".")
        sanitized_name = ".".join(sanitized_name_parts[:-1] or [sanitized_name_parts[0]])

        if mime_type in type_to_ext:
            sanitized_name += type_to_ext[mime_type]

        # Save the uploaded file to the specified folder
        file_path = os.path.join(self.file_upload_folder, sanitized_name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path, f"File uploaded: {file_path}"

    def run(self):
        """Run the Streamlit app"""
        # Configure the Streamlit page with a title and icon
        st.set_page_config(
            page_title="Agent Chat", page_icon="🤖", layout="wide", initial_sidebar_state="expanded"
        )

        # Initialize session state to maintain conversation history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Initialize session state to track uploaded files that the agent can access
        if "file_uploads" not in st.session_state:
            st.session_state.file_uploads = []

        # Title
        st.title("Agent Chat")

        # File upload section in sidebar - allows users to provide documents for the agent to work with
        if self.file_upload_folder is not None:
            with st.sidebar:
                st.header("File Upload")
                uploaded_file = st.file_uploader(
                    "Upload a document (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"]
                )

                if uploaded_file is not None and st.button("Process Upload"):
                    file_path, message = self.upload_file(uploaded_file)
                    if file_path:
                        st.session_state.file_uploads.append(file_path)
                        st.success(message)
                    else:
                        st.error(message)

                if st.session_state.file_uploads:
                    st.subheader("Uploaded Files")
                    for file_path in st.session_state.file_uploads:
                        st.text(os.path.basename(file_path))

        # Display the conversation history between user and agent
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(
                    message["role"], avatar="🧑" if message["role"] == "user" else "🤖"
                ):
                    st.markdown(message["content"])

        # Chat input interface
        if prompt := st.chat_input("What would you like to know?"):
            # Enhance the prompt by informing the agent about available uploaded files
            full_prompt = prompt
            if st.session_state.file_uploads:
                full_prompt += (
                    "\nYou have been provided with these files, which might be helpful or not: "
                    + str(st.session_state.file_uploads)
                )

            # Store the user's message in the conversation history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display the user's message
            with st.chat_message("user", avatar="🧑"):
                st.markdown(prompt)

            # Create a message container for the agent's response
            with st.chat_message("assistant", avatar="🤖"):
                message_container = st.container()

                # Run the agent with the user's prompt and stream its response
                stream_to_streamlit(self.agent, full_prompt, message_container)

                # Store the agent's response in the conversation history
                st.session_state.messages.append(
                    {"role": "assistant", "content": "Response completed"}
                )


__all__ = ["stream_to_streamlit", "StreamlitUI"]
