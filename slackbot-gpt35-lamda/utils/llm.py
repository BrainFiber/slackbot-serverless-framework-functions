from langchain.chat_models import ChatOpenAI, AzureChatOpenAI

import os

USE_AZURE_OPENAI_SERVICE = os.environ.get("USE_AZURE_OPENAI_SERVICE")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
OPENAI_API_VERSION=os.environ.get("OPENAI_API_VERSION")

# gpt3.5 の ChatOpenAIを返す
def get_gpt35(model_name="gpt-3.5-turbo-0613", temperature=0.1):
    if USE_AZURE_OPENAI_SERVICE == "True":
        model_name = "gpt-35-turbo-16k-001"
    return get_llm(model_name, temperature)


# gpt4 の ChatOpenAIを返す
def get_gpt4(model_name="gpt-4-0613", temperature=0.1):
    return get_llm(model_name, temperature)


def get_llm(model_name, temperature):
    # USE_AZURE_OPENAI_SERVICE = True の場合は
    # Azure OpenAI Serviceを使用する
    if USE_AZURE_OPENAI_SERVICE == "True":
        print("Using Azure OpenAI Service")
        llm = AzureChatOpenAI(
            deployment_name=model_name,
            openai_api_base=OPENAI_API_BASE,
            openai_api_key=OPENAI_API_KEY,
            openai_api_version=OPENAI_API_VERSION,
        ) # type: ignore
    else:
        print("Using OpenAI API")
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name=model_name, # type: ignore
            temperature=temperature,
        )  # type: ignore
    return llm
