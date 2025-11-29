from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.documents import Document
from rag_setup import get_retriever
from state import GraphState
from schemas import Quiz

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
web_search_tool = DuckDuckGoSearchRun()

def retrieve_pdf(state: GraphState):
    print("   [Parallel] Scanning PDF Database...")
    question = state["question"]
    try:
        retriever = get_retriever()
        if retriever:
            docs = retriever.invoke(question)
            return {"pdf_documents": docs}
    except:
        pass
    return {"pdf_documents": []}

def web_search(state: GraphState):
    print("   [Parallel] Speculative Web Search...")
    try:
        results = web_search_tool.invoke(state["question"])
        doc = Document(page_content=results, metadata={"source": "web"})
        return {"web_documents": [doc]}
    except:
        return {"web_documents": []}

def merge_documents(state: GraphState):
    print("   [Merge] Evaluating Sources...")
    pdfs = state.get("pdf_documents", [])
    web = state.get("web_documents", [])
    question = state["question"]
    
    if not pdfs:
        print("   [Decision] No PDFs found. Using Web.")
        return {"final_documents": web, "source": "web"}

    print("   [Merge] Grading PDF Relevance...")
    prompt = ChatPromptTemplate.from_template(
        """You are a grader assessing relevance.
        Question: {question}
        Document: {document}
        Does the document contain the semantic meaning to answer the question? 
        Answer only "yes" or "no".
        """
    )
    chain = prompt | llm
    score = chain.invoke({"question": question, "document": pdfs[0].page_content})
    
    if "yes" in score.content.lower():
        print("   [Decision] PDF is relevant. Discarding Web.")
        return {"final_documents": pdfs, "source": "pdf"}
    else:
        print("   [Decision] PDF content irrelevant. Switching to Web.")
        return {"final_documents": web, "source": "web"}

def generate_study(state: GraphState):
    print("---GENERATING EXPLANATION---")
    docs = state["final_documents"]
    source = state.get("source", "pdf")
    
    if not docs:
        return {"generation": "I could not find an answer in your PDF or on the Web."}

    prompt = ChatPromptTemplate.from_template(
        """Answer the question using the provided context.
        
        Current Source: {source}
        
        INSTRUCTIONS:
        - If 'Current Source' is 'web', start by saying "I searched the web and found...".
        - If 'Current Source' is 'pdf', DO NOT say you searched the web. Answer directly from the course notes.
        
        Context: {context}
        Question: {question}
        """
    )
    chain = prompt | llm
    response = chain.invoke({"context": docs, "question": state["question"], "source": source})
    return {"generation": response.content}

def generate_quiz(state: GraphState):
    print("---GENERATING QUIZ---")
    difficulty = state.get("difficulty", "Medium")
    topic = state.get("topic", "General") or "General Concepts"
    
    if difficulty == "Hard":
        instr = "Create 5 complex, conceptual questions testing deep understanding. Focus on 'Why' and 'How'."
    elif difficulty == "Easy":
        instr = "Create 5 straightforward questions about basic definitions."
    else:
        instr = "Create 5 standard difficulty questions."

    structured_llm = llm.with_structured_output(Quiz)
    
    prompt = ChatPromptTemplate.from_template(
        """You are a strict Professor generating a quiz.
        Topic: {topic}
        Difficulty: {difficulty}
        Instructions: {instr}
        
        STRICT RULES:
        1. Questions must be about the TECHNICAL SUBJECT MATTER.
        2. DO NOT ask about metadata (Author, Pages, University).
        3. Make the questions educational.
        
        Context: {context}
        """
    )
    chain = prompt | structured_llm
    response = chain.invoke({
        "context": state["final_documents"], 
        "difficulty": difficulty, 
        "instr": instr,
        "topic": topic
    })
    return {"quiz_data": response}