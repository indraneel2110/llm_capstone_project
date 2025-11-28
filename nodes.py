from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from rag_setup import get_retriever
from state import GraphState
from schemas import Quiz

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def retrieve(state: GraphState):
    print("---RETRIEVING DOCUMENTS---")
    question = state["question"]
    retriever = get_retriever()
    documents = retriever.invoke(question)
    return {"documents": documents}

def generate_study(state: GraphState):
    print("---GENERATING STUDY GUIDE---")
    question = state["question"]
    documents = state["documents"]
    
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful study assistant. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, say that you don't know.
        
        Context: {context}
        
        Question: {question}
        """
    )
    
    chain = prompt | llm
    response = chain.invoke({"context": documents, "question": question})
    return {"generation": response.content}

def generate_quiz(state: GraphState):
    print("---GENERATING QUIZ---")
    documents = state["documents"]
    
    structured_llm = llm.with_structured_output(Quiz)
    
    prompt = ChatPromptTemplate.from_template(
        """Generate a short quiz (3 questions) based on the following context.
        Ensure the questions are relevant to the text provided.
        
        Context: {context}
        """
    )
    
    chain = prompt | structured_llm
    response = chain.invoke({"context": documents})
    return {"quiz_data": response}