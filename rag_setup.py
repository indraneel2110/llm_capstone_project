import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def get_retriever():
    folder_path = "./data"
    
    if not os.path.exists(folder_path) or not os.listdir(folder_path):
        return None

    loader = PyPDFDirectoryLoader(folder_path)
    docs = loader.load()

    if not docs:
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=OpenAIEmbeddings(),
        collection_name="study_guide_rag"
    )
    
    return vectorstore.as_retriever()