"""
Main entry point for the Legal AI Assistant.
"""
import asyncio
from typing import Dict, Any
from AI_core.agent import agent_executor



async def process_legal_request(user_query: str) -> str:
    """
    Process a user's legal request using the multiagent system.
    
    Args:
        user_query (str): The user's legal question or request
        
    Returns:
        str: The response from the legal assistant
    """
    try:
        input_data = {"input": user_query}
        response = await agent_executor.ainvoke(input_data)
        return response["output"]
    except Exception as e:
        return f"Error processing your request: {str(e)}"
