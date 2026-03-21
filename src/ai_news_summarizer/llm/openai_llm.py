import os 
from src.ai_news_summarizer import logger
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
class OpenAILLM:
    def __init__(self, user_controls_input) -> None:
        logger.info("Initialized OpenAI LLM")
        self.user_controls_input = user_controls_input
    
    def get_llm_model(self):
        logger.info("inside get_llm_model method")
        try:
            openai_api_key = os.environ["OPENAI_API_KEY"]
            logger.info("openai_key loaded")
            selected_openai_model = self.user_controls_input["selected_openai_model"]
            logger.info(f"selected_openai_model:{selected_openai_model}")
            llm = ChatOpenAI(api_key=openai_api_key, model=selected_openai_model)
            return llm
        except Exception as e:
            logger.error(f"error occured inside get_llm_model:{e}")
        