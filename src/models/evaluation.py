from pydantic import BaseModel


class AnswerEvaluation(BaseModel):
    question_id: str
    score: float
    strengths: list[str]
    weaknesses: list[str]
    follow_up_required: bool