"""
Tool for generating legal case reports.
"""
from typing import Type
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate

from AI_core.config import LLM
from AI_core.models.input_schemas import ReportGenerationInput

class ReportGenerationTool(BaseTool):
    """Tool to generate comprehensive legal case reports."""
    name: str = "case_report_generation_tool"
    description: str = "Generates comprehensive legal case reports based on provided case information, input to this tool must be a SINGLE JSON STRING"
    args_schema: Type[ReportGenerationInput] = ReportGenerationInput
    
    def _run(self, case_name: str, case_facts: str, legal_issues: str, applicable_laws: str) -> str:
        """
        Generate a comprehensive legal case report.
        
        Args:
            case_name: Name of the legal case
            case_facts: Key facts of the case
            legal_issues: Legal issues identified in the case
            applicable_laws: Laws and regulations applicable to this case
            
        Returns:
            str: Formatted legal case report
        """
        report_template = """
        You are a legal professional drafting a formal case report.
        
        Create a comprehensive legal case report with the following structure:
        
        # CASE REPORT: {case_name}
        
        ## EXECUTIVE SUMMARY
        Provide a brief overview of the case, its significance, and the outcome (if known).
        
        ## CASE FACTS
        {case_facts}
        
        ## LEGAL ISSUES
        {legal_issues}
        
        ## APPLICABLE LAWS AND REGULATIONS
        {applicable_laws}
        
        ## LEGAL ANALYSIS
        Analyze how the applicable laws relate to the facts and issues of this case. Include relevant legal precedents if appropriate.
        
        ## POTENTIAL ARGUMENTS
        Outline possible arguments for both sides of the case.
        
        ## CONCLUSION
        Provide a concluding assessment of the case's legal position, potential outcomes, and recommendations.
        """
        
        report_prompt = PromptTemplate(
            template=report_template,
            input_variables=["case_name", "case_facts", "legal_issues", "applicable_laws"]
        )

        report_chain = report_prompt | LLM 
        
        output = report_chain.invoke(
            {
                "case_name": case_name,
                "case_facts": case_facts,
                "legal_issues": legal_issues,
                "applicable_laws": applicable_laws
            }
        )
        return output.content