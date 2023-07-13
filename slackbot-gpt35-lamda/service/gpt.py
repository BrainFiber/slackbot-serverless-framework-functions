from langchain import PromptTemplate
from langchain.agents import initialize_agent, Tool, AgentType

# PROPMPTをインポートする
from prompt.prompt import GPT35

from tools.graph import create_graph_creator
from tools.newApi import create_news_search_creator

from utils.llm import get_gpt35


def return_answer(text):
    return text


# ユーザ問い合わせからGPTで回答を生成する関数を定義する
def gpt35(query, channel, ts, client, historyStr=""):
    model_name = "gpt-3.5-turbo-0613"
    temperature = 0.5
    llm = get_gpt35(model_name, temperature)

    prompt = PromptTemplate(
        template=GPT35,
        input_variables=["query", "historyStr", "channel", "ts"],
    )

    _input = prompt.format_prompt(
        query=query, historyStr=historyStr, channel=channel, ts=ts
    )
    # output = llm(_input.to_string())
    # chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

    tools = [
        Tool.from_function(
            func=return_answer,
            name="return_answer",
            description="Returning answers to questions"
            # coroutine= ... <- you can specify an async method if desired as well
        ),
        create_graph_creator(client),
        create_news_search_creator(client),
    ]

    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
    output = agent.run(_input.to_string())

    return output
