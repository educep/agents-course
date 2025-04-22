# External imports
from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    Tool,
    ToolCallingAgent,
    VisitWebpageTool,
    tool,
)
from smolagents.models import LiteLLMModel

# Internal imports
from config.settings import settings

"""
# Agent Implementation Analysis:
# =============================
# This file demonstrates two different approaches to building AI agents using SmolaAgents:
# 1. Code Agent: Uses Python code execution approach with step-by-step reasoning
# 2. Tool Calling Agent: Uses direct tool invocation with less intermediate processing
#
# Key differences in behavior:
# - Code Agent uses multiple tools and follows a multi-step approach (theme generation → search → final answer)
# - Tool Calling Agent uses only web search and takes a more direct approach
# - Different prompts lead to different strategies (specific theme vs. general request)
# - Different output formats (specific link vs. categorized recommendations)
#
# These differences highlight how agent architecture, available tools, and prompt specificity
# significantly impact problem-solving approaches and final results.
"""


@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion: The type of occasion for the party.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."


@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.

    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }

    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)

    return best_service


class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""

    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }

    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic Gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets.",
        }

        return themes.get(
            category.lower(),
            "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.",
        )


# Define the LLM Model
model = LiteLLMModel(
    model_id="deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    api_key=settings.deepseek_api_key,
    temperature=0.0,
)

# ------------------------------ CODE AGENT ------------------------------------
# Alfred, the butler, preparing the menu for the party
agent = CodeAgent(
    tools=[
        DuckDuckGoSearchTool(),
        VisitWebpageTool(),
        suggest_menu,
        catering_service_tool,
        SuperheroPartyThemeTool(),
    ],
    model=model,
    max_steps=10,
    verbosity_level=2,
)

step_log = agent.run(
    """Give me the best playlist for a party at the Wayne's mansion.
    The party idea is a 'villain masquerade' theme
    """
)

"""
Out - Final answer: The best playlist for a 'villain masquerade' themed party at
Wayne's mansion is the 'Gotham Rogues' playlist on Spotify:
https://open.spotify.com/playlist/3cejFigsE9RrSdG4xUCmay.
It features 42 songs perfectfor a mysterious and villainous atmosphere.
"""

# ------------------------------ TOOL CALLING AGENT ------------------------------------
agent = ToolCallingAgent(tools=[DuckDuckGoSearchTool()], model=model)

step_log_tool = agent.run(
    "Search for the best music recommendations for a party at the Wayne's mansion."
)

# Note: The key difference between these agents is:
# 1. The Code Agent has access to multiple tools and uses Python code execution
# 2. The Tool Calling Agent only has access to web search and uses direct tool invocation
# 3. The prompts are different (specific theme vs. general request)
# This explains the different approaches and results seen in execution
