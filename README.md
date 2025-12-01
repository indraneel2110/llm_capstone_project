
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
-Setting up the Environment: make a virtual environment, create a .env file, install all requirements

[DONE] Step 2: 
-Building the Search Engine (Data Layer): create rag_setup.py to handle PDF loading and text splitting. Set up the Vector Database (ChromaDB) and run a test to ensure the system can actually find specific keywords in my document.

[DONE] Step 3: 
-Defining the Graph Structure: create state.py to define exactly what data (questions, documents, answers) flows between the steps. I will also create schemas.py using Pydantic to ensure that when I ask for a quiz, the AI gives me perfect JSON instead of messy text.

[DONE] Step 4: 
-Coding the Worker Nodes: this will be the core logic. I will create nodes.py to write the specific functions for Retrieval (fetching data), Study Generation (RAG), and Quiz Generation.

[DONE] Step 5: 
-Wiring the Graph: to bring everything together in main.py. This involves defining the LangGraph workflow and the conditional edges :the Router that decides whether to generate a quiz or a study guide.

-So far this is the plan, i'll update anything else accordingly after doing this first

-Update: I have achieved the core objective of the project: uploading a pdf and getting the llm model to be able to 
-1) answer any question from the pdf I want
-2) quiz me on the topics from the pdf

-These are some results after I uploaded an example pdf and ran the program:

<img width="1594" height="586" alt="image" src="https://github.com/user-attachments/assets/6c24f36b-37eb-4110-8632-54b91339d4a1" />

<img width="948" height="631" alt="image" src="https://github.com/user-attachments/assets/116133f4-d1f3-48cb-aaca-dd8620d90650" />

-This however, is still a bit far from what I had envisioned, I still want to add some additional features like adaptable difficulty, web search etc using more tools that I learnt throughout the course. So I will make some more changes in due time

-Update: I have thought about the following next steps now in order to improve my project and add some creative features:

[DONE] Step 6: 
-Scaling Data Ingestion: Upgrade the ingestion pipeline from just processing a single PDF file to a Directory Loader.

[DONE] Step 7: 
-Implement Web Search and Parallelization: Use Web Search (using DuckDuckGo search tool) as a fallback for missing information. Refactor the graph to run PDF Retrieval and Web Search in parallel.

[DONE] Step 8: 
-Merging & Relevance Grading: Implement a Merger Node that evaluates the quality of retrieved PDF documents. Add conditional logic to prioritize PDF data but automatically switch to Web data if the PDF content is graded as irrelevant.

[DONE] Step 9:
-Adaptibility and Strict Output Constraints: Update GraphState to track difficulty levels between 3 levels(easy, medium and hard). Add a feedback loop in the main application that suggests increasing/decreasing difficulty based on the user's score in the previous quiz. Refine the Quiz Generation prompt to include Negative Constraints and ensure the LLM focuses strictly on technical concepts instead of irrelevant questions on document formatting and metadata.

[DONE] Step 10:
-Add minimal UI: Replace the basic input loop with a rich terminal UI using the rich library

## Final Results:

This is the structure of the graph:

<img width="338" height="432" alt="image" src="https://github.com/user-attachments/assets/3d1184ad-a816-4536-8f1b-c4e7c113bc73" />


-The llm uses rag to retreive relevant information from the pdf sets uploaded by user and parallely runs web search on the user asked question, if the question asked is relevant and present in the uploaded pdfs, then the llm discards the web search results and answers on the basis of the pdfs. Else, it answers on the basis of web search.

<img width="1615" height="815" alt="image" src="https://github.com/user-attachments/assets/0ed424f1-5c50-4bc4-a41f-3e0cd95211be" />

-The llm gives the user quizzes with relevant questions as per requirement, keeping their previous quiz results as state memory and based on defined performance metrics, it then suggests the user to switch to easier or harder modes.

<img width="1598" height="756" alt="image" src="https://github.com/user-attachments/assets/7cb5985a-20fb-417a-86c2-a968aaa02ce1" />

<img width="1616" height="665" alt="image" src="https://github.com/user-attachments/assets/97d51610-4985-4d4a-8e42-184a5843b33c" />



## Conclusion:

I had planned to achieve a functional and efficient Study Guide that could help users simplify their study resources by uploading them at one single space, and based on that user-made database, they could clear their doubts, get explanations and quiz themselves. I feel I am satisfied with the conclusion of my project, this is because I first tried to solve the core objective of the project(basic qna and quiz), and then thought about ways of upgrading it. Then I started coming up with some more ideas- like a fallback if the user uploaded pdfs do not contain relevant info that the user requires, in that case the llm will use web searching to solve this issue. Also worked on adaptive quiz logic that helps the llm dynamically provide different quiz difficulties. Based on all this, I think I have achieved the conclusion satisfactorily.

----------

  
## VIDEO:
https://drive.google.com/file/d/1iXKcgq7_EZ5HLc83NMqW_wcNyBt8Ak8w/view?usp=sharing
