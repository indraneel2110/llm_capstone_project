import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def get_retriever():
    # 1. Load Data
    # Ensure "course_notes.pdf" is in your folder and is NOT a scanned image.
    loader = PyPDFLoader("course_notes.pdf")
    docs = loader.load()

    # 2. Split Data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Embed & Store
    # We use a persistent directory so we don't have to rebuild the DB every time
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=OpenAIEmbeddings(),
        collection_name="study_guide_rag"
    )
    
    return vectorstore.as_retriever()