# main.py

from dotenv import load_dotenv
load_dotenv()

import os
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import wikipedia_tool, search_tool, arxiv_tool


class ResearchResponse(BaseModel):
    topic: str = Field(description="The main topic of the research query.")
    summary: str = Field(description="A comprehensive, synthesized summary of the research findings.")
    key_points: list[str] = Field(description="A bulleted list of the most important facts or findings.")
    sources: list[str] = Field(description="A list of URLs for the primary sources used.")
    tools_used: list[str] = Field(description="The names of the tools that were used to find the information.")
    conflicting_information: str = Field(description="A brief note on any conflicting or contradictory information found, if any.")


# Using the reliable model for tool calling
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Set up the parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# MODIFIED: Updated the prompt to use the correct default tool name 'tavily_search'
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a world-class research analyst. Your goal is to provide a detailed and synthesized analysis of the user's topic.

            Follow these steps:
            1.  **Plan:** First, think about what you need to find out. Formulate a plan and decide which tool is best for each piece of information (e.g., Wikipedia for general knowledge, ArXiv for scientific papers, web search for recent news).
            2.  **Execute:** Use the available tools to gather information. You can use multiple tools if needed.
            3.  **Synthesize:** Once you have the information, combine it into a cohesive summary. Do not just list the tool outputs.
            4.  **Structure Output:** Format your final answer according to the provided JSON schema. Ensure you list the source URLs and the names of the tools you used. If you find conflicting information, note it down.

            Available tools:
            - search_wikipedia: For foundational, encyclopedic information.
            - tavily_search: For general web searches, recent events, and diverse perspectives.
            - search_arxiv: For scientific papers, academic research, and technical topics.

            {format_instructions}
            """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{user_input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
).partial(format_instructions=parser.get_format_instructions())

# Include all available tools
tools = [wikipedia_tool, search_tool, arxiv_tool]

# Create the agent and agent executor
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# Main loop for conversational interaction
def main():
    chat_history = []
    print("🤖 Hello! I am your advanced research assistant. What can I help you with today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🤖 Goodbye!")
            break

        try:
            # Invoke the agent with the user input and chat history
            raw_response = agent_executor.invoke(
                {
                    "user_input": user_input,
                    "chat_history": chat_history
                }
            )

            # Append the current turn to chat history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=raw_response.get("output", "")))

            # Attempt to parse and print the structured response
            try:
                structured_response = parser.parse(raw_response.get("output"))
                print("\n✅ Research Complete!")
                print("="*30)
                print(f"**Topic:** {structured_response.topic}")
                print(f"**Summary:** {structured_response.summary}\n")
                print("**Key Points:**")
                for point in structured_response.key_points:
                    print(f"- {point}")
                print(f"\n**Conflicting Info:** {structured_response.conflicting_information}")
                print(f"**Sources:** {', '.join(structured_response.sources)}")
                print(f"**Tools Used:** {', '.join(structured_response.tools_used)}")
                print("="*30 + "\n")
            except Exception as e:
                print("\n⚠️ Could not parse the structured output. Displaying raw response:")
                print(raw_response.get("output"))
                print(f"(Parsing Error: {e})\n")
        except Exception as e:
            print(f"\nAn error occurred during agent execution: {e}")


if __name__ == "__main__":
    main()