import os
import uuid
from langchain.tools import tool
import subprocess
from pydantic import BaseModel, Field

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







