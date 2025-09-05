# tools.py

from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
# MODIFIED: Corrected the import name from TavilySearchResults to TavilySearch
from langchain_tavily import TavilySearch
from langchain.tools import Tool

load_dotenv()

# Wikipedia Tool remains the same
def search_wikipedia_full_content(query: str):
    """Get full Wikipedia content, not just summary"""
    api_wrapper = WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=4000
    )
    return api_wrapper.run(query)

wikipedia_tool = Tool(
    name="search_wikipedia",
    func=search_wikipedia_full_content,
    description="Searches Wikipedia for the given query and returns the full page content. Use for foundational, encyclopedic knowledge."
)

# MODIFIED: Changed TavilySearchResults to the correct class name, TavilySearch
search_tool = TavilySearch(max_results=3)


# ArXiv Tool for academic and scientific research
arxiv_tool = ArxivQueryRun()
arxiv_tool.name = "search_arxiv"
arxiv_tool.description = "Searches ArXiv.org for scientific and academic papers. Use for topics related to science, technology, AI, physics, etc."