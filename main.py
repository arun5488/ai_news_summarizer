import streamlit as st
from src.ai_news_summarizer.ui.streamlitui.loadui import LoadStreamlitUI
from src.ai_news_summarizer.ui.streamlitui.display_result import DisplayResultStreamlit
from src.ai_news_summarizer import logger
from src.ai_news_summarizer.llm.openai_llm import OpenAILLM
from src.ai_news_summarizer.graph.graph_builder import GraphBuilder
from src.ai_news_summarizer.ui.streamlitui.display_result import DisplayResultStreamlit

def load_ai_new_summarizer():
    """
    loads and run the AI News Summary agentic AI app with streamlit UI.
    this function initializes the UI, handles the user input, configures the LLM model and displays the output
    """
    #load UI

    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load input from UI")
        return 
    
    if st.session_state.IsFetchButtonClicked:
        try:
            obj_llm_config = OpenAILLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()
            logger.info(f"model:{type(model)}")
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph()
                DisplayResultStreamlit(graph, user_message=user_input['frequency']).display_result_on_ui()
            except Exception as e:
                logger.error(f"Error: Graph setup failed:{e}")
                return
        except Exception as e:
            logger.error(f"error occured in UI:{e}")