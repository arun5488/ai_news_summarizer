from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from src.ai_news_summarizer import logger 
from src.ai_news_summarizer import constants as const
from dotenv import load_dotenv
import os
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
        Fetch AI news based on the specified frequency
        state variable contains the frequency details
        """
        logger.info("inside fetch_news method")
        frequency = state["messages"][0].content.lower()
        logger.info(f"llm inside fetch_news:{self.llm}")
        logger.info(f"frequency:{frequency}")
        self.state['frequency'] = frequency
        time_range_map = {'daily':'d','weekly':'w','monthly':'m'}
        days_map = {'daily':1,'weekly':7,'monthly':30,'year':366}

        response = self.tavily.search(
            query="Top AI technology news India and globally",
            topic= "news",
            time_range= time_range_map[frequency],
            include_answer="advanced",
            max_results = const.MAX_RESULTS,
            days = days_map[frequency]

        )
        self.state['news_data'] = response.get('results',[])
        return state
    
    def summarize_news(self, state: dict) -> dict:
        logger.info("inside summarize_news method")
        """
        summarize fetched news using LLM
        """
        news_item = self.state['news_data']
        logger.info(f"llm:{self.llm}")
        prompt_template = ChatPromptTemplate.from_messages([
            ("system",""" Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise setences summary from latest news
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
        return self.state
    
    def save_result(self, state):
        logger.info("inside save_result method")
        frequency = self.state['frequency']
        logger.info(f"frequency:{frequency}")
        summary = self.state['summary']
        logger.info(f"summary:{summary}")
        filename = f"{const.AI_NEWS_PATH}_{frequency}_summary.md"
        logger.info(f"filename:{filename}")
        with open(filename, 'w') as f:
            f.write(f" # {frequency} AI News Summary \n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state

        