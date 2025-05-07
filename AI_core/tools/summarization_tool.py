"""
Tool for summarizing legal documents.
"""
from langchain.tools import BaseTool
from langchain.chains import LLMChain, MapReduceDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader

from AI_core.config import LLM, TEXT_SPLITTER

class SummarizationTool(BaseTool):
    """Tool to summarize legal documents using a map-reduce approach."""
    name: str = "document_summarization_tool"
    description: str = "Summarizes legal documents. Input should be a file path to a PDF or text document."
    
    def _run(self, file_path: str) -> str:
        """
        Run the document summarization process.
        
        Args:
            file_path: Path to the document to summarize
            
        Returns:
            str: Summarized content
        """
        # Load document
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        else:
            with open(file_path, 'r') as f:
                text = f.read()
            documents = [text]
        
        # Split documents
        docs = TEXT_SPLITTER.split_documents(documents)
        
        # Map step - summarize each chunk
        map_template = """
        You are a legal expert summarizing complex legal documents.
        Summarize the following text in a concise and accurate manner, preserving key legal points:
        
        {text}
        """
        map_prompt = PromptTemplate(template=map_template, input_variables=["text"])
        map_chain = LLMChain(llm=LLM, prompt=map_prompt, output_key="summary")
        
        # Reduce step - combine summaries
        reduce_template = """
        You are a legal expert creating a comprehensive summary from multiple text segments.
        Combine these summaries into a cohesive overview of the entire document, organized by key legal themes and points:
        
        {summaries}
        """
        reduce_prompt = PromptTemplate(template=reduce_template, input_variables=["summaries"])
        reduce_chain = LLMChain(llm=LLM, prompt=reduce_prompt)
        
        # Create MapReduce chain
        map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=map_chain,
            reduce_documents_chain=reduce_chain,
            document_variable_name="text",
        )
        
        return map_reduce_chain.run(docs)