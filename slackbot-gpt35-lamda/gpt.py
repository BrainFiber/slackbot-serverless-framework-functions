from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool

import os

# Jokeクラスをインポートする
from outputParser import Response

# PROPMPTをインポートする
from prompt import GPT35

from tools.graph import create_graph_creator


def return_answer(text):
    return text


# ユーザ問い合わせからGPTで回答を生成する関数を定義する
def gpt35(query, channel, ts,client, historyStr=""):
    model_name = "gpt-3.5-turbo-0613"
    temperature = 0.5
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model_name=model_name, # type: ignore
        temperature=temperature,
    )  # type: ignore

    prompt = PromptTemplate(
        template=GPT35,
        input_variables=["query", "historyStr", "channel", "ts"],
    )

    _input = prompt.format_prompt(query=query, historyStr=historyStr, channel=channel, ts=ts)
    # output = llm(_input.to_string())
    # chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

    tools = [
        Tool.from_function(
            func=return_answer,
            name="return_answer",
            description="Returning answers to questions"
            # coroutine= ... <- you can specify an async method if desired as well
        ),
        create_graph_creator(client)
    ]

    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
    output = agent.run(_input.to_string())

    # output = chain.run(query=query, historyStr=historyStr)

    # print(output)

    return output