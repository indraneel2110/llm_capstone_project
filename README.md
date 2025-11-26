
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

I plan to excecute these steps to complete my project.

- [TODO] Step 1 involves blah blah
- [TODO] Step 2 involves blah blah
- [TODO] Step 3 involves blah blah
- ...
- [TODO] Step n involves blah blah

## Conclusion:

I had planned to achieve {this this}. I think I have/have-not achieved the conclusion satisfactorily. The reason for your satisfaction/unsatisfaction.

----------

- Creativity: 5
  
