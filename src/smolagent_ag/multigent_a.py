# External imports
import os

from PIL import Image
from smolagents import CodeAgent, GoogleSearchTool, HfApiModel, OpenAIServerModel, VisitWebpageTool

# from smolagents.models import LiteLLMModel
from smolagents.utils import encode_image_base64, make_image_url

# Internal imports
from src.smolagent_ag.cargo_plane_tool import calculate_cargo_travel_time

# from config.settings import settings


# todo: check with LiteLLMModel to avoid inference limits
# Qwen model to browse the web ("easy" task)
model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct", provider="together", max_tokens=8096)

web_agent = CodeAgent(
    model=model,
    tools=[
        GoogleSearchTool(provider="serper"),
        VisitWebpageTool(),
        calculate_cargo_travel_time,
    ],
    name="web_agent",
    description="Browses the web to find information",
    verbosity_level=0,
    max_steps=10,
)


# The manager agent will need to do some mental heavy lifting.
# So we give it the stronger model DeepSeek-R1, and add a planning_interval to the mix.
# Define the LLM Model
# manager_model = LiteLLMModel(
#     model_id="deepseek-chat",
#     api_base="https://api.deepseek.com/v1",
#     api_key=settings.deepseek_api_key,
#     temperature=0.0,
# )

manager_model = HfApiModel("deepseek-ai/DeepSeek-R1", provider="together", max_tokens=8096)


def check_reasoning_and_plot(final_answer, agent_memory):
    multimodal_model = OpenAIServerModel("gpt-4o", max_tokens=8096)
    filepath = "saved_map.png"
    assert os.path.exists(filepath), "Make sure to save the plot under saved_map.png!"
    image = Image.open(filepath)
    prompt = (
        f"Here is a user-given task and the agent steps: {agent_memory.get_succinct_steps()}. Now here is the plot that was made."
        "Please check that the reasoning process and plot are correct: do they correctly answer the given task?"
        "First list reasons why yes/no, then write your final decision: PASS in caps lock if it is satisfactory, FAIL if it is not."
        "Don't be harsh: if the plot mostly solves the task, it should pass."
        "To pass, a plot should be made using px.scatter_map and not any other method (scatter_map looks nicer)."
    )
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": make_image_url(encode_image_base64(image))},
                },
            ],
        }
    ]
    output = multimodal_model(messages).content
    print("Feedback: ", output)
    if "FAIL" in output:
        raise Exception(output)
    return True


manager_agent = CodeAgent(
    model=manager_model,
    tools=[calculate_cargo_travel_time],
    managed_agents=[web_agent],
    additional_authorized_imports=[
        "geopandas",
        "plotly",
        "shapely",
        "json",
        "pandas",
        "numpy",
    ],
    planning_interval=5,
    verbosity_level=2,
    final_answer_checks=[check_reasoning_and_plot],
    max_steps=15,
)


manager_agent.visualize()

manager_agent.run(
    """
Find all Batman filming locations in the world, calculate the time to transfer via cargo plane to here (we're in Gotham, 40.7128° N, 74.0060° W).
Also give me some supercar factories with the same cargo plane transfer time. You need at least 6 points in total.
Represent this as spatial map of the world, with the locations represented as scatter points with a color that depends on the travel time, and save it to saved_map.png!

Here's an example of how to plot and return a map:
import plotly.express as px
df = px.data.carshare()
fig = px.scatter_map(df, lat="centroid_lat", lon="centroid_lon", text="name", color="peak_hour", size=100,
     color_continuous_scale=px.colors.sequential.Magma, size_max=15, zoom=1)
fig.show()
fig.write_image("saved_image.png")
final_answer(fig)

Never try to process strings using code: when you have a string to read, just print it and you'll see it.
"""
)

"""
I don't know how that went in your run, but in mine, the manager agent skilfully divided tasks
 given to the web agent in
 1. Search for Batman filming locations, then
 2. Find supercar factories, before aggregating the lists and plotting the map.

Let's see what the map looks like by inspecting it directly from the agent state:
"""
manager_agent.python_executor.state["fig"]
