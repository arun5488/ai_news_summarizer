from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from src.ai_news_summarizer import logger 
from src.ai_news_summarizer import constants as const
from dotenv import load_dotenv
import os
import regex as re
from src.ai_news_summarizer.tools.extract_year import _extract_year, _in_year
load_dotenv()

class AINewsNode:
    def __init__(self, llm) -> None:
        logger.info("Initialized AINewsNode")
        self.tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
        self.llm = llm
        logger.info(f"llm: {self.llm}")
        self.state = {}
    
    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI news based on the specified chat input and frequency
        state variable contains the frequency details
        """
        logger.info("inside fetch_news method")
        user_input = state["user_chat_input"][0].content.lower()
        logger.info(f"user chat input inside fetch_news:{user_input}")

        year = _extract_year(user_input)

        # If year found, remove it from semantic query text so query is cleaner
        query_text = re.sub(r"\b(19|20)\d{2}\b", "", user_input).strip()
        logger.info(f" query_text inside fetch_news:{query_text}")
        if not query_text:
            query_text = user_input

        
        frequency = state["messages"][0].content.lower()
        logger.info(f"llm inside fetch_news:{self.llm}")
        logger.info(f"frequency:{frequency}")
        self.state['frequency'] = state["messages"]
        time_range_map = {'daily':'d','weekly':'w','monthly':'m'}
        days_map = {'daily':1,'weekly':7,'monthly':30,'year':366}

        search_kwargs = {
            "query": query_text,
            "topic": "news",
            "include_answer": "advanced",
            "max_results": const.MAX_RESULTS,
        }

        if year:
            search_kwargs["start_date"] = f"{year}-01-01"
            search_kwargs["end_date"] = f"{year}-12-31"
            # NO days, NO time_range here
        else:
            search_kwargs["time_range"] = time_range_map[frequency]
            search_kwargs["days"] = days_map[frequency]
            # NO start_date/end_date here

        response = self.tavily.search(**search_kwargs)
        results = response.get('results',[])
        state['news_data'] = results
        self.state["user_chat_input"] = state["user_chat_input"]
        state["requested_year"] = year
        state["query_text"] = query_text
        self.state["news_data"] = state['news_data']
        return state
    
    def summarize_news(self, state: dict) -> dict:
        logger.info("inside summarize_news method")
        """
        summarize fetched news using LLM
        """
        news_item = self.state['news_data']
        logger.info(f"llm:{self.llm}")
        frequency = state["messages"][0].content.lower()
        time_range_map = {'daily':'d','weekly':'w','monthly':'m'}
        days_map = {'daily':1,'weekly':7,'monthly':30}
        prompt_template = ChatPromptTemplate.from_messages([
            ("system",f""" Summarize news articles for the topic user has asked is passed as news_data into markdown format. 
            You have to summarize the news articles based on the frequency {days_map[frequency]}
            For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from  news. atleast 3 sentences.
            - sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date] 
            - [Summary][URL]"""),("user","Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content:{item.get('content','')}\nURL:{item.get('url','')}\nDate:{item.get('published_date','')}"
            for item in news_item
        ])

        response = self.llm.invoke(prompt_template.format(articles = articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return state
    
    def save_result(self, state):
        logger.info("inside save_result method")
        user_input = self.state["user_chat_input"][0].content.lower()
        logger.info(f"user chat input inside save_result method:{user_input}")
        frequency = self.state['frequency'][0].content.lower()
        logger.info(f"frequency:{frequency}")
        summary = self.state['summary']
        logger.info(f"summary:{summary}")
        filename = f"{const.AI_NEWS_PATH}_{user_input}_{frequency}_summary.md"
        logger.info(f"filename:{filename}")
        with open(filename, 'w') as f:
            f.write(f" # {user_input} {frequency} News Summary \n\n")
            f.write(summary)
        self.state['filename'] = filename
        return state

        