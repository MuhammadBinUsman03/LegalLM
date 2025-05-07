"""
Tool for extracting specific legal elements from texts.
"""
from langchain.tools import BaseTool
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

from AI_core.config import AGENT_LLM

class ElementExtractionTool(BaseTool):
    """Tool to extract specific legal elements from legal texts."""
    name: str = "legal_element_extraction_tool"
    description: str = "Extracts specific legal elements from legal texts such as contracts, judgments, or legal briefs."
    
    def _run(self, query: str) -> str:
        """
        Extract specific legal elements from texts.
        
        Args:
            query: Legal text to extract elements from
            
        Returns:
            str: Extracted legal elements
        """
        # Define extraction schema
        schema = {
            "title": "Extractor",
            "description": "Extract relevant legal elements.",
            "type": "object",            
            "properties": {
                "parties": {"type": "array", "items": {"type": "string"}, "description": "The parties involved in the legal document"},
                "dates": {"type": "array", "items": {"type": "string"}, "description": "Important dates mentioned in the document"},
                "obligations": {"type": "array", "items": {"type": "string"}, "description": "Legal obligations specified in the document"},
                "jurisdiction": {"type": "string", "description": "The legal jurisdiction that applies"},
                "legal_citations": {"type": "array", "items": {"type": "string"}, "description": "Citations of laws, regulations, or precedents"},
                "monetary_values": {"type": "array", "items": {"type": "string"}, "description": "Monetary amounts mentioned in the document"}
            },
            "required": ["parties"]
        }
        
        # Create extraction chain
        extraction_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a legal element extraction expert. Extract the requested information from the provided legal text."),
            HumanMessage(content="Extract the following information from this legal text: {query}")
        ])
        extraction_chain = extraction_prompt | AGENT_LLM.with_structured_output(schema=schema)
        
        # Run extraction
        try:
            result = extraction_chain.invoke({"query": query})
            # Format result for better readability
            formatted_result = "Extracted Legal Elements:\n\n"
            for key, value in result.items():
                if isinstance(value, list):
                    formatted_result += f"{key.capitalize()}:\n"
                    for item in value:
                        formatted_result += f"- {item}\n"
                else:
                    formatted_result += f"{key.capitalize()}: {value}\n"
            return formatted_result
        except Exception as e:
            return f"Error extracting elements: {str(e)}"