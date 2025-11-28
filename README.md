
## Title: Efficient Study Guide- A RAG Study Assistant Using Langgraph

## Overview

The general idea is that this Study Guide will help students convert unstructured course materials (PDFs, lecture notes, lecture slides, textbooks) into an interactive study assistant, and help the students be smarter with their time and resources. The program will use semantic search and RAG to answer questions with citations, generate quizzes and flashcards, produce step-by-step explanations, and adapt quiz difficulty automatically based on the student's performance. The system will use a LangGraph flow (stateful graph), with LLM nodes for prompting and structured responses, tool-calls for computation, and LangSmith traces for debugging. This Guide will also be particularly useful for preparing certain explaination points that are expected in our courses as taught in the classes and provided in the notes, that generic chatgpt or gemini models won't be able to provide.

## Reason for picking up this project

"Think about all the problems which you cannot have solved earlier, but are now possible to solve with the concepts learned in this course."
I thought about this and then came up with this project idea.
This project will integrate the following tools that I learnt throughout the course:
- Prompting: to guide the LLM to answer in exam-style formats, or to generate quizzes and explanations the way I want
- Structured Output: so the model always returns answers in clear JSON formats ,for example: answers with citations, quiz questions, flashcards
- Semantic Search: which allows the system to actually find the relevant sections from my uploaded materials instead of guessing
- Retrieval-Augmented Generation (RAG): which ensures that all answers come from my course content, with citations, so the system doesn’t try to over or undercompensate or go outside the syllabus, and provide me exactly the content I require
- Tool calling & MCP: which I use for things like small calculations, grading quiz answers, and other helper functions
- LangGraph: to organise the whole application as a series of nodes: like routing the user’s request, retrieving documents, generating answers, grading quizzes, explaining mistakes, and adapting difficulty

## Plan

[DONE] Step 1:
Setting up the Environment: make a virtual environment, create a .env file, install all requirements

[DONE] Step 2: 
Building the Search Engine (Data Layer): create rag_setup.py to handle PDF loading and text splitting. Set up the Vector Database (ChromaDB) and run a test to ensure the system can actually find specific keywords in my document.

[DONE] Step 3: 
Defining the Graph Structure: create state.py to define exactly what data (questions, documents, answers) flows between the steps. I will also create schemas.py using Pydantic to ensure that when I ask for a quiz, the AI gives me perfect JSON instead of messy text.

[TODO] Step 4: 
Coding the Worker Nodes: this will be the core logic. I will create nodes.py to write the specific functions for Retrieval (fetching data), Study Generation (RAG), and Quiz Generation.

[TODO] Step 5: 
Wiring the Graph: to bring everything together in main.py. This involves defining the LangGraph workflow and the conditional edges :the Router that decides whether to generate a quiz or a study guide.

So far this is the plan, i'll update anything else accordingly after doing this first
## Conclusion:

I had planned to achieve {this this}. I think I have/have-not achieved the conclusion satisfactorily. The reason for your satisfaction/unsatisfaction.

----------

  
