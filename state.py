from typing import TypedDict, List
from langchain_core.documents import Document

class GraphState(TypedDict):
    question: str
    generation: str
    pdf_documents: List[Document]
    web_documents: List[Document]
    final_documents: List[Document]
    quiz_data: dict
    difficulty: str
    topic: str
    source: str