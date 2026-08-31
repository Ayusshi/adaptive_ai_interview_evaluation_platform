from typing import Literal

from pydantic import BaseModel, Field


Difficulty = Literal["easy", "medium", "hard"]

QuestionType = Literal[
    "conceptual",
    "practical",
    "scenario",
    "debugging",
    "system_design",
]


class Competency(BaseModel):
    name: str = Field(min_length=1)
    importance: float = Field(ge=0.0, le=1.0)
    question_count: int = Field(ge=1)
    difficulty: list[Difficulty]
    question_types: list[QuestionType]


class InterviewPlan(BaseModel):
    total_questions: int = Field(ge=1)
    competencies: list[Competency]

    easy_percentage: float = Field(ge=0.0, le=1.0)
    medium_percentage: float = Field(ge=0.0, le=1.0)
    hard_percentage: float = Field(ge=0.0, le=1.0)


class InterviewQuestion(BaseModel):
    question: str = Field(min_length=10)

    competency: str = Field(min_length=1)

    difficulty: Difficulty

    question_type: QuestionType

    expected_concepts: list[str] = Field(
        default_factory=list
    )

class GeneratedQuestions(BaseModel):
    questions: list[InterviewQuestion]