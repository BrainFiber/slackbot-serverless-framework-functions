from langchain.tools import tool
from pydantic import BaseModel, Field
from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import AgentType
from langchain.output_parsers import PydanticOutputParser
from langchain import PromptTemplate
import uuid

import os

from tools.dummy import create_dummy

# PROPMPTをインポートする
from prompt.prompt import GRAPH_CREATOR_CREATE_PYTHON_AGENT

from tools.utils.pythonTool import PythonREPLTool

from parsers.outputParser import GraphCreatorCreatePythonAgentResponse

from utils.llm import get_gpt4

GPT4_ENABLED = os.environ.get("GPT4_ENABLED")  # type: ignore


class GraphCreatorInput(BaseModel):
    detail: str = Field(description="Describe all graph display requirements")
    channel: str = Field(description="channel Information")
    ts: str = Field(description="ts Information")


# use gpt4
def create_graph_creator(client):
    # UUIDを文字列を生成する
    uuid_str = str(uuid.uuid4())

    if GPT4_ENABLED == "True":

        @tool("graph_creator", args_schema=GraphCreatorInput)
        def graph_creator(detail: str, channel: str, ts: str) -> str:
            """Create a graph.."""
            parser = PydanticOutputParser(
                pydantic_object=GraphCreatorCreatePythonAgentResponse
            )

            prompt = PromptTemplate(
                template=GRAPH_CREATOR_CREATE_PYTHON_AGENT,
                input_variables=["query", "filename"],
                # partial_variables={"format_instructions": parser.get_format_instructions()},
            )

            _input = prompt.format_prompt(
                query="The following rules must be followed.", filename=uuid_str
            )

            agent_executor = create_python_agent(
                llm=get_gpt4(),
                tool=PythonREPLTool(),  # type: ignore
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                # agent_executor_kwargs={"handle_parsing_errors": True},
                prefix=_input.to_string(),
            )

            output = agent_executor.run("Create a graph." + detail)

            path = f"/tmp/{uuid_str}.png"

            # pathにファイルが存在するか確認する
            if not os.path.exists(path):
                print("ファイルが存在しません")
                return "ファイルが存在しません"
            else:
                client.files_upload(
                    channels=channel, file=path, title="graph", thread_ts=ts
                )

            return output

        return graph_creator
    else:
        # dummy
        return create_dummy(client)
