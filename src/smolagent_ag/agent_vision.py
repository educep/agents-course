# Standard imports
from io import BytesIO

import requests

# Third-party imports
from PIL import Image
from smolagents import CodeAgent, OpenAIServerModel

# Internal imports
from config.settings import settings

model = OpenAIServerModel(
    model_id="gpt-4o",
    api_base="https://api.openai.com/v1",
    api_key=settings.open_api_key,
)

image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/e/e8/The_Joker_at_Wax_Museum_Plus.jpg",  # Joker image
    "https://upload.wikimedia.org/wikipedia/en/9/98/Joker_%28DC_Comics_character%29.jpg",  # Joker image
]

images = []
for url in image_urls:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    images.append(image)


# Instantiate the agent
agent = CodeAgent(tools=[], model=model, max_steps=20, verbosity_level=2)

response = agent.run(
    """
    Describe the costume and makeup that the comic character in these photos is wearing and return the description.
    Tell me if the guest is The Joker or Wonder Woman.
    """,
    images=images,
)

""" --- OUTPUT ---
Out - Final answer: Image 1: The character has a wide, exaggerated smile with prominent white face paint
covering the entire face. There is dark eye makeup around the eyes, and the lips are painted a bold color. Thecharacter wears a bright purple coat and a large colorful bow tie, with hints of green in the hair, paired
with a yellow shirt.
Image 2: The character has exaggerated features with green hair. They are wearing a dark suit with a
distinctive flower on the lapel and are holding a playing card.
Character: The Joker
[Step 1: Duration 53.41 seconds| Input tokens: 5,845 | Output tokens: 319]
"""
