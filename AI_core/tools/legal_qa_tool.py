"""
Tool for answering legal questions using a knowledge base.
"""
from langchain.tools import BaseTool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from AI_core.config import LLM

class LegalQATool(BaseTool):
    """Tool to answer legal questions using a knowledge base."""
    name: str = "legal_qa_tool"
    description: str = "Answers legal questions using a knowledge base of laws and regulations."
    memory: ConversationBufferMemory = None
    
    def __init__(self):
        """Initialize the legal QA tool with conversation memory."""
        super().__init__()
        # Initialize memory in the constructor
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    def _run(self, query: str) -> str:
        """
        Answer legal questions using a knowledge base.
        
        Args:
            query: Legal question to answer
            
        Returns:
            str: Answer to the legal question
        """
        # In production environment:
        # 1. Load vector store with legal documents
        # 2. Create retriever from vector store
        # 3. Create ConversationalRetrievalChain
        
        template = """
        You are a legal assistant specializing in answering legal questions.
        
        Use your knowledge of laws and regulations to provide an accurate and helpful answer to the question.
        
        Question: {question}
        
        Provide a clear, concise answer citing relevant laws or precedents when appropriate.
        Include a disclaimer that your answer is not legal advice.
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["question"]
        )
        
        qa_chain = LLMChain(
            llm=LLM,
            prompt=prompt
        )
        
        response = qa_chain.run(question=query)
        
        # Update conversation memory
        self.memory.chat_memory.add_user_message(query)
        self.memory.chat_memory.add_ai_message(response)
        
        return response