from typing import TypedDict, List

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    
    Attributes:
        question: The user's original question.
        generation: The final answer text (for study mode).
        documents: A list of retrieved context chunks.
        quiz_data: The structured quiz object (for quiz mode).
    """
    question: str
    generation: str
    documents: List[str]
    quiz_data: dict