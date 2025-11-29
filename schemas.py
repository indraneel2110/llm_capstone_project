from pydantic import BaseModel, Field
from typing import List

class QuizQuestion(BaseModel):
    question: str = Field(description="The quiz question text")
    options: List[str] = Field(description="List of 4 multiple choice options")
    correct_answer: str = Field(description="The correct option from the list")
    explanation: str = Field(description="Why this answer is correct")

class Quiz(BaseModel):
    title: str = Field(description="Title of the quiz")
    questions: List[QuizQuestion] = Field(description="A list of 5 questions")