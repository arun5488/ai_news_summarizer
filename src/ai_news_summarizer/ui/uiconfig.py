from configparser import ConfigParser
from src.ai_news_summarizer import logger
from src.ai_news_summarizer import constants as const

class Config:
    def __init__(self) -> None:
        logger.info("Initializing Config object")
        self.config = ConfigParser()
        self.config.read(const.UICONFIG_FILE_PATH)
    
    def get_llm_options(self):
        logger.info("Inside get_llm_options method")
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")

    def get_page_tile(self):
        logger.info("Inside get_page_title method")
        return self.config["DEFAULT"].get("PAGE_TITLE")