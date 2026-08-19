from pydantic import BaseModel, Field

from src.models.candidate import Candidate
from src.models.job import Job
from src.models.interview import (
    Competency,
    InterviewStatus,
    Question,
)
from src.models.evaluation import AnswerEvaluation


class InterviewState(BaseModel):
    candidate: Candidate
    job: Job

    competencies: list[Competency] = Field(default_factory=list)
    interview_plan: list[Question] = Field(default_factory=list)

    questions_asked: list[str] = Field(default_factory=list)
    evaluations: list[AnswerEvaluation] = Field(default_factory=list)

    current_question: Question | None = None
    current_answer: str | None = None

    difficulty: int = 1

    status: InterviewStatus = InterviewStatus.NOT_STARTED