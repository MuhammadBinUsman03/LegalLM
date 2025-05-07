"""
Tool for analyzing legal evidence using DEEPresearch.
"""
import requests
import json
from langchain.tools import BaseTool

from AI_core.config import DEEPSEARCH_API_URL

class EvidenceAnalysisTool(BaseTool):
    """Tool to analyze legal evidence using DEEPresearch."""
    name: str = "evidence_analysis_tool"
    description: str = "Analyzes legal evidence using DEEPresearch and builds relationships between entities. Input should be a legal query about evidence or case analysis."
    
    def _run(self, query: str) -> str:
        """
        Analyze legal evidence using DEEPresearch.
        
        Args:
            query: Legal query about evidence or case analysis
            
        Returns:
            str: Analysis results from DEEPresearch
        """
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "jina-deepsearch-v1",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a legal evidence analyst. Your task is to analyze legal evidence, extract key entities, and establish relationships between them."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "stream": False,
            "reasoning_effort": "low",
            "max_attempts": 2,
            "no_direct_answer": False
        }

        try:
            # In production, use actual API call
            response = requests.post(DEEPSEARCH_API_URL, headers=headers, json=data)
            result = response.json()['choices'][0]['message']['content']
            return result
        except Exception as e:
            return f"Error analyzing evidence with DEEPresearch: {str(e)}"