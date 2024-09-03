import uuid
from pathlib import Path
import requests

from langchain.tools import tool
from openai import OpenAI
from pydantic import BaseModel, Field

CLIENT = OpenAI(api_key="sk-boQYeHnjCR5rUqoUVj6XvrvfJM9E9ulMo1dLwfzCBTT3BlbkFJPOyI-dqZavW9-mnN8jTBhRKRSiQ0oqVJgPspORtokA")


class GenerateImageInput(BaseModel):
    image_description: str = Field(
        description="A detailed description of the desired image."
    )


@tool("generate_image", args_schema=GenerateImageInput)
def generate_image(image_description: str) -> str:
    """Call to generate an image and make sure to remind the user to ask for a link in order to get it"""

    response = CLIENT.images.generate(
        model="dall-e-3",
        prompt=image_description,
        size="1024x1024",
        quality="standard",  # standard or hd
        n=1,
    )
    image_url = response.data[0].url
    return image_url
# if __name__ == "__main__":  #this is just test
#  print(generate_image.run("a picture of kaiden simon, a cute little jewish boy"))