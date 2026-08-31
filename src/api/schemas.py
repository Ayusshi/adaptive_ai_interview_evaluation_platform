from pydantic import BaseModel


class StartInterviewRequest(BaseModel):
    candidate_id: str
    role: str


class StartInterviewResponse(BaseModel):
    candidate_id: str
    role: str
    question_number: int
    question: str
    competency: str
    difficulty: str


class SubmitAnswerRequest(BaseModel):
    candidate_id: str
    answer: str


class SubmitAnswerResponse(BaseModel):
    question_number: int
    score: int
    feedback: str
    current_difficulty: str
    next_difficulty: str
    next_question: str | None
    interview_complete: bool


class FinalReportResponse(BaseModel):
    candidate_id: str
    role: str
    total_questions: int
    questions_answered: int
    overall_score: float
    recommendation: str
    average_score: float
    competencies: list
    strengths: list[str]
    weaknesses: list[str]