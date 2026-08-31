from pydantic import BaseModel, Field


class AnswerEvaluation(BaseModel):
    score: int = Field(ge=0, le=10)

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    missing_concepts: list[str] = Field(
        default_factory=list
    )

    feedback: str = Field(min_length=1)

    needs_followup: bool