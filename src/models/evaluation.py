from pydantic import BaseModel, Field

class AnswerEvaluation(BaseModel):

    score: int = 0

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    missing_concepts: list[str] = Field(
        default_factory=list
    )

    feedback: str = ""

    needs_followup: bool = False