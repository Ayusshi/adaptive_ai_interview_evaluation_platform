from pydantic import BaseModel


class CompetencyReport(BaseModel):
    competency: str
    score: float
    questions: int


class InterviewReport(BaseModel):
    candidate_id: str
    role: str

    total_questions: int
    questions_answered: int

    overall_score: float
    recommendation: str

    competencies: list[CompetencyReport]

    strengths: list[str]
    weaknesses: list[str]

    average_score: float