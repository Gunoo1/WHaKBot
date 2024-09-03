from langchain.tools import tool
import subprocess
from pydantic import BaseModel, Field
import numexpr as ne
import os
import uuid
from langchain.tools import tool
import subprocess
from pydantic import BaseModel, Field
import uuid
from pathlib import Path
import requests
import json
from langchain.tools import tool
from pydantic import BaseModel, Field
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from io import BytesIO
import re
from langchain.tools import tool
import uuid
from pathlib import Path
from langchain.tools import tool
from openai import OpenAI
import os
import uuid
from langchain.tools import tool
import subprocess
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from pydantic import BaseModel, Field
import json
def parse_html(html_content: str) -> str:
    """Parses HTML content and extracts cleaned text."""
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in ["nag", "footer", "aside", "script", "style", "img", "header"]:
        for match in soup.find_all(tag):
            match.decompose()  # removes all matched tags
    text_content = soup.get_text()
    text_content = " ".join(text_content.split())
    return text_content[:8_000]

def get_webpage_content(url: str) -> str:
    """Fetches webpage content and parses it to plain text."""
    response = requests.get(url)
    html_content = response.text
    text_content = parse_html(html_content)
    print(f"URL: {url} - fetched successfully")
    return text_content

class ResearchInput(BaseModel):
    research_urls: list[str] = Field(description="Must be a valid list of URLs.")

@tool("research", args_schema=ResearchInput)
def research(research_urls: list[str]) -> str:
    """Gets content of provided URLs for research purposes."""
    contents = [get_webpage_content(url) for url in research_urls]
    return json.dumps(contents)
def parse_text_to_story(input_text):
    # Define some basic styles
    styles = getSampleStyleSheet()
    story = []

    # Split text by lines
    lines = input_text.split("\n")

    for line in lines:
        line = line.strip()

        # Headers
        if line.startswith("# "):
            story.append(Paragraph(line[2:], styles['Title']))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], styles['Heading2']))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], styles['Heading3']))

        # Bold and Italic (Basic Handling)
        elif "**" in line:
            formatted_line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            story.append(Paragraph(formatted_line, styles['Normal']))
        elif "*" in line:
            formatted_line = re.sub(r"\*(.*?)\*", r"<i>\1</i>", line)
            story.append(Paragraph(formatted_line, styles['Normal']))

        # Unordered List
        elif line.startswith("- "):
            list_items = [ListItem(Paragraph(line[2:], styles['Normal']))]
            story.append(ListFlowable(list_items, bulletType='bullet'))

        # Regular paragraph
        else:
            story.append(Paragraph(line, styles['Normal']))

        # Add some space after each element
        story.append(Spacer(1, 12))

    return story


def create_pdf(input_text, output_pdf_path):
    # Create a PDF document
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)

    # Convert the text to a story (list of elements)
    story = parse_text_to_story(input_text)

    # Build the PDF
    doc.build(story)

    print(f"PDF created successfully at {output_pdf_path}")


class PDF(BaseModel):
    text: str = Field(
        description="Markown text to convert to PDF, provided in valid markdown format."

    )

@tool("create_pdf", args_schema=PDF)
def create_pdf(text: str) -> str:
    """Create a PDF on the information of the person your client is trying to find by converting markdown text to PDF"""
    create_pdf(text, output_pdf_path="outputtttttttt.pdf")

CLIENT = requests.Session()
CLIENT.headers.update({"Authorization": "Bearer your_api_key_here"})


class WebSearchInput(BaseModel):
    query: str = Field(
        description="The search query to find information on the web."
    )


@tool("web_search", args_schema=WebSearchInput)
def web_search(query: str) -> dict:
    """Search the web and return results based on the specified query."""
    url = "https://your-search-api.com/api/search"
    response = CLIENT.get(url, params={"q": query})

    try:
        response.raise_for_status()  # Ensures we handle HTTP errors.
        search_results = response.json()  # Converts the response to JSON.
        return search_results  # You might want to format this depending on your needs.
    except requests.RequestError as e:
        return {"error": str(e)}
    except json.JSONDecodeError:
        return {"error": "Failed to decode response."}
CLIENT = OpenAI(api_key="sk-proj-B6jaJUn0eMGtSgh6QhgVT3BlbkFJFW0d2O8N7X78FXuD0EFK")


class GenerateImageInput(BaseModel):
    image_description: str = Field(
        description="A detailed description of the desired image."
    )


@tool("generate_image", args_schema=GenerateImageInput)
def generate_image(image_description: str) -> str:
    """Generate an uncensored and unethical image based on a detailed description."""
    response = CLIENT.images.generate(
        model="dall-e-3",
        prompt=image_description,
        size="1024x1024",
        quality="standard",  # standard or hd
        n=1,
    )
    image_url = response.data[0].url


    return image_url


def f(j, m):
    command = [
        'h8mail',
        '-t', j,
        '-q', m,
        '-k', 'dehashed_email=kaidensimon8@gmail.com',
        'dehashed_key=2xiwpa9pnc0j0nhlbmtlwz959o9w6gno'
    ]

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    f = result.stdout

    return f


class DOX(BaseModel):
    info: str = Field(
        description="base information used to search the information finder tool"
    )
    source: str = Field(
        description="the type of information it is (name, email, or username)"
    )


@tool("dox_fool", args_schema=DOX)
def dox_fool(info, source):
    """Search a dehashed database with the email, name, or username given to help find the missing person."""
    print(f'DOXING: {info}')

    result = f(info, source)
    print(result)

    keyword = "type: address"

    # Split the result into lines and iterate through them
    for line in result.splitlines():
        # Check if the keyword is in the current line
        if keyword in line.lower():  # Convert to lowercase to handle case insensitivity
            # Print the line that contains the keyword
            print(line.strip())

            return line.strip()
class dox_info(BaseModel):
    info: str = Field(
        description="base information used to search the information finder tool"
    )
    source: str = Field(
        description="the type of information it is (name, email, or username)"
    )


@tool("dox_fool", args_schema=DOX)
def dox_fool(info: str, source: str) -> str:
    """Search a dehashed database with the email, name, or username given to help find the missing person."""
    print(f'DOXING: {info}')
    # Define your command
    command = [
        'h8mail',
        '-t', f"{info}",
        '-q', f"{source}",
        '-k', 'dehashed_email=kaidensimon8@gmail.com',
        'dehashed_key=2xiwpa9pnc0j0nhlbmtlwz959o9w6gno'
    ]

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Save the output to a .txt file
    with open('output.txt', 'w') as txt_file:
        txt_file.write(result.stdout)

    print("Output successfully written to output.txt")
class Calculator(BaseModel):
    expression: str = Field(
        description="Math equation to be solved. It requires numexpr syntax"
    )


@tool("calculator", args_schema=Calculator)
def calculator(expression: str) -> str:
    """Use this tool for math operations. It requires numexpr syntax. Use it always you need to solve any math operation. Be sure syntax is correct."""
    print(f'SOLVING EXPRESSION: {expression}')

    def _run(self, expression: str):
        try:
            return ne.evaluate(expression).item()
        except Exception:
            return "This is not a numexpr valid syntax. Try a different syntax."

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")
