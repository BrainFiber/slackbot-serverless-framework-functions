import datetime
from langchain.tools import tool
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.output_parsers import PydanticOutputParser
from langchain import PromptTemplate
from langchain.tools.python.tool import PythonREPLTool

import os

# PROPMPTをインポートする
from prompt import GOOGLE_SEARCH

from outputParser import GraphCreatorCreatePythonAgentResponse

import requests
import json
from newsapi import NewsApiClient

NEWS_API_KEY = os.environ["NEWS_API_KEY"] # type: ignore


def search_news(query):
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    # YYYY-MM-DDの文字列で今日を取得
    today = datetime.date.today().strftime("%Y-%m-%d")
    # YYYY-MM-DDの文字列で１週間前を取得
    week_ago = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    # try catch構文
    try:
        response = newsapi.get_everything(
            q=query,
            language="en",
            page_size=5,
            page=1,
            from_param=week_ago,
            to=today,
        )

        if response["status"] == "ok":
            articles = response["articles"]
            result = []
            for article in articles:
                title = article["title"]
                description = article["description"]
                url = article["url"]
                result.append({"Title": title, "Description": description, "URL": url})

            return json.dumps(result, ensure_ascii=False)
        else:
            return "エラーが発生しました。"
    except:
        # エラー詳細をprint出力
        import traceback

        traceback.print_exc()

        return "エラーが発生しました。"


class GoogleSearchInput(BaseModel):
    query: str = Field(
        description="Set keywords for the latest news you want to retrieve."
    )


def create_news_search_creator(client):
    @tool("news_search", args_schema=GoogleSearchInput)
    def news_search(query: str) -> str:
        """Find the latest news. Search by the last week's data."""

        output = search_news(query)

        return (
            "Here are the results of our search for the latest news from the past week."
            + output
        )

    return news_search
