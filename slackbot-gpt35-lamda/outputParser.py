from typing import List
from pydantic import BaseModel, Field, validator


# Define your desired data structure.
class GraphCreatorCreatePythonAgentResponse(BaseModel):
    filepath: str = Field(description="Set the file full path of the output image data")


# Define your desired data structure.
class GraphCreatorCodeGenerateResponse(BaseModel):
    pythonCode: str = Field(description="Set up all Python code to create the graph.")
    filepath: str = Field(description="Set the output destination for the graph")
