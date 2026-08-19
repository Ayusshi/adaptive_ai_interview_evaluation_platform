from pydantic import BaseModel


class Candidate(BaseModel):
    name: str
    experience_years: float
    resume_text: str