from langgraph.graph import StateGraph
from src.ai_news_summarizer.nodes.ai_news_node import AINewsNode 
from src.ai_news_summarizer import logger
from src.ai_news_summarizer.state.state import State
from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition, ToolNode

class GraphBuilder:
    def __init__(self, model) -> None:
        logger.info("Initialized GraphBuilder")
        self.llm = model
        logger.info(f"llm:{type(self.llm)}")
        self.graph_builder = StateGraph(State)
    
    def ai_news_summary(self):
        logger.info("inside ai_news_summary method")
        ai_news_node = AINewsNode(self.llm)
        logger.info(f"ai_news_node:{ai_news_node}")

        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result", END)

    def setup_graph(self):
        logger.info("Inside setup_graph method")
        self.ai_news_summary()
        return self.graph_builder.compile()
        