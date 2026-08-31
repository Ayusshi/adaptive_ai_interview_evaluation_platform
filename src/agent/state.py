from typing import TypedDict


class InterviewState(TypedDict):

    candidate_id: str
    role: str

    interview_plan: dict

    current_question: str
    current_answer: str
    current_expected_concepts: list[str]

    questions_asked: list[str]
    answers: list[str]

    evaluations: list[dict]

    current_competency: str
    current_difficulty: str
    next_difficulty: str

    question_number: int
    interview_complete: bool