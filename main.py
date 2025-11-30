import os
import time
from dotenv import load_dotenv
from typing import Literal

from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt, IntPrompt
from rich.rule import Rule
from rich import print as rprint

from langgraph.graph import StateGraph, END, START
from state import GraphState
from nodes import retrieve_pdf, web_search, merge_documents, generate_study, generate_quiz

load_dotenv()
console = Console()

def route_request(state: GraphState) -> Literal["generate_quiz", "generate_study"]:
    q = state["question"].lower()
    if "quiz" in q or "test" in q: return "generate_quiz"
    return "generate_study"

workflow = StateGraph(GraphState)
workflow.add_node("retrieve_pdf", retrieve_pdf)
workflow.add_node("web_search", web_search)
workflow.add_node("merge_documents", merge_documents)
workflow.add_node("generate_study", generate_study)
workflow.add_node("generate_quiz", generate_quiz)

workflow.add_edge(START, "retrieve_pdf")
workflow.add_edge(START, "web_search")

workflow.add_edge("retrieve_pdf", "merge_documents")
workflow.add_edge("web_search", "merge_documents")

workflow.add_conditional_edges("merge_documents", route_request, {
    "generate_quiz": "generate_quiz",
    "generate_study": "generate_study"
})

workflow.add_edge("generate_study", END)
workflow.add_edge("generate_quiz", END)

app = workflow.compile()

def display_study_mode(result):
    content = result["generation"]
    source = result.get("source", "pdf")
    
    console.print("\n")
    console.print(Markdown(content))
    console.print("\n")
    
    if source == "web":
        console.print("[dim]Sources: Web Search (PDFs insufficient)[/dim]")
    else:
        console.print("[dim]Sources: Course Notes[/dim]")
    console.print(Rule(style="dim"))

def run_interactive_quiz(quiz_data):
    console.print(Rule(f"Quiz: {quiz_data.title}", style="bold magenta"))
    score = 0
    total = len(quiz_data.questions)

    for i, q in enumerate(quiz_data.questions):
        console.print(f"\n[bold]{i+1}. {q.question}[/bold]")
        
        for idx, opt in enumerate(q.options):
            console.print(f"   {idx+1}) {opt}")
        
        while True:
            try:
                user_choice = IntPrompt.ask("   Answer")
                if 1 <= user_choice <= 4: break
            except: pass
            
        selected_opt = q.options[user_choice - 1]
        
        if selected_opt == q.correct_answer:
            console.print("   [green]Correct[/green]")
            score += 1
        else:
            console.print(f"   [red]Incorrect.[/red] The answer is [bold]{q.correct_answer}[/bold].")
            console.print(f"   [dim]{q.explanation}[/dim]")
        time.sleep(0.3)

    console.print(f"\n[bold]Score: {score}/{total}[/bold]")
    console.print(Rule(style="dim"))
    
    if score >= 4: return "increase"
    elif score < 3: return "decrease"
    return "same"

if __name__ == "__main__":
    console.clear()
    console.print("[bold]Study Assistant[/bold] is ready.")
    console.print("[dim]Ask a question, or type 'Quiz me'. (Type 'q' to quit)[/dim]\n")
    
    current_difficulty = "Medium"

    while True:
        user_input = Prompt.ask("[bold]You[/bold]")
        
        if user_input.lower() in ["q", "quit", "exit"]: 
            console.print("See you later!")
            break
            
        if user_input.lower() == "level":
             current = f"[bold]{current_difficulty}[/bold]"
             console.print(f"Current difficulty: {current}")
             if Prompt.ask("Change?", choices=["y", "n"]) == "y":
                 current_difficulty = Prompt.ask("Select", choices=["Easy", "Medium", "Hard"], default="Medium")
             continue

        with console.status("[dim]Thinking...[/dim]", spinner="dots"):
            inputs = {"question": user_input, "difficulty": current_difficulty}
            try:
                result = app.invoke(inputs)
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue

        if result.get("quiz_data"):
            suggestion = run_interactive_quiz(result["quiz_data"])
            
            if suggestion == "increase" and current_difficulty != "Hard":
                console.print("\n[bold]Great job.[/bold] That seemed too easy.")
                if Prompt.ask("   Want to try Hard mode next?", choices=["y", "n"]) == "y": 
                    current_difficulty = "Hard"
                    console.print("   [dim]Difficulty set to Hard.[/dim]")
            
            elif suggestion == "decrease" and current_difficulty != "Easy":
                console.print("\n[bold]That was tough.[/bold]")
                if Prompt.ask("   Want to switch to Easy mode for a bit?", choices=["y", "n"]) == "y": 
                    current_difficulty = "Easy"
                    console.print("   [dim]Difficulty set to Easy.[/dim]")
            
        else:
            display_study_mode(result)