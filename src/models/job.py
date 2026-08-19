from pydantic import BaseModel, Field
from typing import Literal

class Job(BaseModel):
    title: str
    description: str


class Competency(BaseModel):
    name: str
    importance: Literal["low", "medium", "high"]
    description: str


class JobAnalysis(BaseModel):
    role: str
    minimum_experience_years: float | None = None
    maximum_experience_years: float | None = None
    competencies: list[Competency] = Field(default_factory=list)