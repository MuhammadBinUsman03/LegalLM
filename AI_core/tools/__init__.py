"""
Legal Assistant tools initialization.
"""
from langchain.tools import Tool

from AI_core.tools.summarization_tool import SummarizationTool
from AI_core.tools.report_generation_tool import ReportGenerationTool
from AI_core.tools.evidence_analysis_tool import EvidenceAnalysisTool
from AI_core.tools.legal_qa_tool import LegalQATool
from AI_core.tools.element_extraction_tool import ElementExtractionTool

# Create tool instances
summarization_tool = SummarizationTool()
report_generation_tool = ReportGenerationTool()
evidence_analysis_tool = EvidenceAnalysisTool()
legal_qa_tool = LegalQATool()
element_extraction_tool = ElementExtractionTool()

# Create tools list for the agent
tools = [
    Tool.from_function(
        func=summarization_tool._run,
        name="document_summarization_tool",
        description="Summarizes legal documents. Input should be a file path to a PDF or text document."
    ),
    report_generation_tool,
    evidence_analysis_tool,
    Tool.from_function(
        func=legal_qa_tool._run,
        name="legal_qa_tool",
        description="Answers legal questions. Input should be a clear legal question."
    ),
    element_extraction_tool
]

__all__ = ['tools', 'summarization_tool', 'report_generation_tool', 
           'evidence_analysis_tool', 'legal_qa_tool', 'element_extraction_tool']