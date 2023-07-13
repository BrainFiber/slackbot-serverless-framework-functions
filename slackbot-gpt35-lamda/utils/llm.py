from langchain.chat_models import ChatOpenAI


# gpt3.5 の ChatOpenAIを返す
def get_gpt35(model_name = "gpt-3.5-turbo-0613", temperature=0.1):
    model_name = "gpt-3.5-turbo-0613"
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],  # type: ignore
        model_name=model_name,  # type: ignore
        temperature=temperature,
    )  # type: ignore
    return llm

# gpt4 の ChatOpenAIを返す
def get_gpt4(model_name = "gpt-4-0613", temperature=0.1):
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],  # type: ignore
        model_name=model_name,  # type: ignore
        temperature=temperature,
    )  # type: ignore
    return llm