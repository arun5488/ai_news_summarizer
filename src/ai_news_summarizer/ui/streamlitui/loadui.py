import streamlit as st
import os 
from src.ai_news_summarizer import logger
from src.ai_news_summarizer.ui.uiconfig import Config
from src.ai_news_summarizer import constants as const

class LoadStreamlitUI:
    def __init__(self):
        logger.info("Initializing LoadSreamlitUI")
        self.config = Config()
        self.user_controls = {}
    
    def load_streamlit_ui(self):
        logger.info("inside load_streamlit_ui method")
        page_title = self.config.get_page_tile()
        logger.info(f"page_title:{page_title}")
        st.set_page_config(page_title= page_title)
        st.header(page_title)
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            logger.info(f"llm_options:{llm_options}")

            #llm selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
            logger.info(f"selected llm option:{self.user_controls['selected_llm']}")

            if self.user_controls["selected_llm"] == "OpenAI":
                model_options = const.OPENAI_MODEL_OPTIONS
                logger.info(f"model options:{model_options}")
                selected_openai_model = self.user_controls["selected_openai_model"]=st.selectbox("select model", model_options)
                logger.info(f"selected_openai_model:{selected_openai_model}")
            
                st.subheader("AI News Explorer")

                with st.sidebar:
                    time_frame = st.selectbox("Select Time Frame",["Daily","Weekly","Monthly"], index=0)
                    if st.button("Fetch latest AI News", use_container_width= True):
                        st.session_state.IsFetchButtonClicked = True
                        logger.info(f"time frame:{time_frame}")
                        st.session_state.timeframe = time_frame
                        self.user_controls['frequency'] = time_frame
                    
        return self.user_controls