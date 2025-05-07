"""
Setup for the legal assistant agent.
"""
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate

from AI_core.config import AGENT_LLM
from AI_core.tools import tools

# Create the main legal assistant agent
system_prompt = """
You are a helpful assistant that can use multiple tools to answer questions. 
You have access to multiple specialized tools:

1. Document Summarization - For summarizing legal documents
2. Case Report Generation - For creating comprehensive legal case reports
3. Evidence Analysis - For analyzing legal evidence using advanced research capabilities 
   (Use this tool when you need updated information regarding laws and public information)
4. Legal Q&A - For answering legal questions using a knowledge base
5. Legal Element Extraction - For extracting specific elements from legal texts
"""

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(AGENT_LLM, tools, agent_prompt)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)