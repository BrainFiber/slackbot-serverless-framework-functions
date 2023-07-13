from langchain.tools import tool
from pydantic import BaseModel, Field


class GraphCreatorInput(BaseModel):
    query: str = Field(description="Describe all graph display requirements")


def create_dummy(client):
    @tool("dummy", args_schema=GraphCreatorInput)
    def dummy(query) -> str:
        """this is dummy.do not use this."""

        return query

    return dummy
