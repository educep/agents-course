"""
# Splitting the task between two agents
Multi-agent structures allow to separate memories between different sub-tasks,
with two great benefits:

- Each agent is more focused on its core task, thus more performant
- Separating memories reduces the count of input tokens at each step, thus reducing
  latency and cost
"""
# External imports
from smolagents import CodeAgent, GoogleSearchTool, HfApiModel, VisitWebpageTool

# Internal imports
from src.smolagent_ag.cargo_plane_tool import calculate_cargo_travel_time

# from smolagents.models import LiteLLMModel


# from config.settings import settings

# Define the LLM Model
# Hf model using a inference provider explicitly
model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", provider="together")

# stronger model
# model = LiteLLMModel(
#     model_id="deepseek-chat",
#     api_base="https://api.deepseek.com/v1",
#     api_key=settings.deepseek_api_key,
#     temperature=0.0,
# )

task = """Find all Batman filming locations in the world, calculate the time to transfer
via cargo plane to here (we're in Gotham, 40.7128° N, 74.0060° W), and return them to me
as a pandas dataframe.
Also give me some supercar factories with the same cargo plane transfer time.
"""

"""
The GoogleSearchTool uses the Serper API to search the web, so this requires either having
setup env variable SERPER_API_KEY and passing provider="serpapi" or having SERPER_API_KEY
and passing provider=serper.

If you don’t have any Serp API provider setup, you can use DuckDuckGoSearchTool but beware
that it has a rate limit.
"""
agent = CodeAgent(
    model=model,
    tools=[GoogleSearchTool("serper"), VisitWebpageTool(), calculate_cargo_travel_time],
    additional_authorized_imports=["pandas"],
    max_steps=20,
)

result = agent.run(task)
print(result)

task2 = f"""
You're an expert analyst. You make comprehensive reports after visiting many websites.
Don't hesitate to search for many queries at once in a for loop.
For each data point that you find, visit the source url to confirm numbers.

{task}
"""

result2 = agent.run(task2)
print(result2)
