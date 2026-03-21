import streamlit as st
from src.ai_news_summarizer import logger
from src.ai_news_summarizer import constants as const
import json
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

class DisplayResultStreamlit:
    def __init__(self, graph, user_message) -> None:
        logger.info("Initialized DisplayResultStreamlit")
        self.graph = graph
        logger.info(f"graph:{self.graph}")
        self.user_message = user_message
        logger.info(f"user_message = {self.user_message}")
    
    def display_result_on_ui(self):
        logger.info("inside display_result_on_ui method")
        graph = self.graph
        logger.info(f"graph:{graph}")
        frequency = self.user_message
        logger.info(f"frequency:{frequency}")
        with st.spinner("Fetching and summarizer news ...."):
            result = graph.invoke({"messages":frequency})
            try:
                ai_news_path = f"{const.AI_NEWS_PATH}_{frequency.lower()}_summary.md"
                with open(ai_news_path,"r") as file:
                    markdown_content = file.read()
                
                st.markdown(markdown_content, unsafe_allow_html=True)
            except FileNotFoundError:
                st.error(f"File {ai_news_path} not found")
            except Exception as e:
                st.error(f"error occured inside display_result_on_ui:{e}")
