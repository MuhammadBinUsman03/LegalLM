"""
Configuration settings for the Legal AI Assistant.
"""
from dotenv import load_dotenv
load_dotenv()  # by default looks for .env in current directory

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# LLM configurations
LLM = ChatGroq(temperature=0, model_name="compound-beta")
AGENT_LLM = ChatGroq(temperature=0, model_name="deepseek-r1-distill-llama-70b")

# Embedding configuration
EMBEDDINGS = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Text splitting configuration
TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150,
)

# API endpoints
DEEPSEARCH_API_URL = 'https://deepsearch.jina.ai/v1/chat/completions'


