from smolagents import CodeAgent
from smolagents.models import LiteLLMModel

# Internal imports
from config.settings import settings

"""
# Time Calculation Agent Analysis:
# ===============================
# This agent demonstrates a computational approach using CodeAgent without external tools.
#
# Key characteristics:
# - Uses Python code execution to solve time calculation problems
# - Relies on datetime library for time operations (explicitly authorized)
# - Takes a structured, algorithmic approach rather than using tools
# - Processes input data directly from prompt text
#
# The agent is ideal for computational tasks where:
# - The answer can be derived through calculation
# - External information is not needed
# - Python's standard libraries provide sufficient functionality
#
# This implementation shows how CodeAgent can be used for tasks beyond
# information retrieval, focusing on data processing and calculation.
"""

# Define the LLM Model
model = LiteLLMModel(
    model_id="deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    api_key=settings.deepseek_api_key,
    temperature=0.0,  # Deterministic output for calculations
)

# Note: This agent uses no tools, unlike agent_2.py which uses multiple tools
# The additional_authorized_imports parameter allows the agent to use datetime
# which is necessary for time calculations
agent = CodeAgent(
    tools=[],
    model=model,
    additional_authorized_imports=[
        "datetime"
    ],  # Explicitly authorize datetime for time calculations
)

agent.run(
    """
    Alfred needs to prepare for the party. Here are the tasks:
    1. Prepare the drinks - 30 minutes
    2. Decorate the mansion - 60 minutes
    3. Set up the menu - 45 minutes
    4. Prepare the music and playlist - 45 minutes

    If we start right now, at what time will the party be ready?
    """
)

# When executed, this agent:
# 1. Parses the tasks and their durations from the prompt
# 2. Creates a data structure (dictionary) to organize the information
# 3. Calculates the total time required (180 minutes)
# 4. Gets the current time using datetime.now()
# 5. Adds the total duration to get the completion time
# 6. Returns a formatted time string (HH:MM)
# Sample execution code (what the agent executed):
"""
import datetime

# Time required for each task in minutes
tasks = {
    "Prepare the drinks": 30,
    "Decorate the mansion": 60,
    "Set up the menu": 45,
    "Prepare the music and playlist": 45
}

# Calculate total time in minutes
total_minutes = sum(tasks.values())

# Get current time
current_time = datetime.datetime.now()

# Add total time to current time
ready_time = current_time + datetime.timedelta(minutes=total_minutes)

final_answer(ready_time.strftime("%H:%M"))
"""
