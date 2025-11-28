import os
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

from langgraph.graph import StateGraph, END
from state import GraphState
from nodes import retrieve, generate_study, generate_quiz

def route_request(state: GraphState) -> Literal["generate_study", "generate_quiz"]:
    """
    Decides if the user wants a study explanation or a quiz 
    based on keywords in the question.
    """
    question = state["question"].lower()
    if "quiz" in question or "test" in question:
        return "generate_quiz"
    return "generate_study"

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate_study", generate_study)
workflow.add_node("generate_quiz", generate_quiz)

workflow.set_entry_point("retrieve")

workflow.add_conditional_edges(
    "retrieve",
    route_request,
    {
        "generate_study": "generate_study",
        "generate_quiz": "generate_quiz"
    }
)

workflow.add_edge("generate_study", END)
workflow.add_edge("generate_quiz", END)

app = workflow.compile()

if __name__ == "__main__":
    print("Study Assistant Ready.")
    
    while True:
        user_input = input("\nEnter your question (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
            
        inputs = {"question": user_input}
        
        result = app.invoke(inputs)
        
        if result.get("quiz_data"):
            print(f"\n[QUIZ MODE]: {result['quiz_data'].title}")
            for i, q in enumerate(result['quiz_data'].questions):
                print(f"\nQ{i+1}: {q.question}")
                for opt in q.options:
                    print(f" - {opt}")
                print(f"(Correct: {q.correct_answer})")
        else:
            print(f"\n[STUDY MODE]:\n{result['generation']}")