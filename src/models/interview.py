from enum import Enum

from pydantic import BaseModel


class InterviewStatus(str, Enum):
    NOT_STARTED = "not_started"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    EVALUATING = "evaluating"
    COMPLETED = "completed"


class Competency(BaseModel):
    name: str
    importance: str


class Question(BaseModel):
    id: str
    competency: str
    difficulty: int
    question: str