from fastapi import APIRouter, HTTPException

from src.models.interview import (
    StartInterviewRequest,
    SubmitAnswerRequest,
)
from src.services.interview_service import InterviewService
from src.services.report_service import ReportService


router = APIRouter()

interview_service = InterviewService()
report_service = ReportService()


# Temporary interview plan.
# Later this will come from the Job Analysis
# + Interview Planner pipeline.
DEFAULT_INTERVIEW_PLAN = {
    "total_questions": 6,

    "competencies": [
        {
            "name": "Python",
            "importance": 0.25,
            "question_count": 2,
            "difficulty": ["easy", "medium"],
            "question_types": [
                "conceptual",
                "practical",
            ],
        },
        {
            "name": "Machine Learning",
            "importance": 0.35,
            "question_count": 2,
            "difficulty": ["medium", "hard"],
            "question_types": [
                "conceptual",
                "scenario",
            ],
        },
        {
            "name": "RAG",
            "importance": 0.40,
            "question_count": 2,
            "difficulty": ["medium", "hard"],
            "question_types": [
                "conceptual",
                "scenario",
            ],
        },
    ],

    "easy_percentage": 0.2,
    "medium_percentage": 0.5,
    "hard_percentage": 0.3,
}


@router.post("/interviews/start")
def start_interview(
    request: StartInterviewRequest,
):

    state = interview_service.start_interview(
        candidate_id=request.candidate_id,
        role=request.role,
        interview_plan=DEFAULT_INTERVIEW_PLAN,
    )

    return {
        "candidate_id": state["candidate_id"],
        "role": state["role"],
        "question_number": state["question_number"],
        "question": state["current_question"],
        "competency": state["current_competency"],
        "difficulty": state["current_difficulty"],
        "interview_complete": state["interview_complete"],
    }


@router.post("/interviews/{candidate_id}/answer")
def submit_answer(
    candidate_id: str,
    request: SubmitAnswerRequest,
):

    state = interview_service.get_interview_state(
        candidate_id
    )

    if state is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        )

    if state.get("interview_complete", False):
        raise HTTPException(
            status_code=400,
            detail="Interview is already complete.",
        )

    state = interview_service.submit_answer(
        candidate_id=candidate_id,
        answer=request.answer,
    )

    response = {
        "candidate_id": candidate_id,
        "question_number": state["question_number"],
        "evaluation": (
            state["evaluations"][-1]
            if state["evaluations"]
            else None
        ),
        "interview_complete": state["interview_complete"],
    }

    if not state["interview_complete"]:
        response["next_question"] = state[
            "current_question"
        ]

        response["competency"] = state[
            "current_competency"
        ]

        response["difficulty"] = state[
            "current_difficulty"
        ]

    return response


@router.get("/interviews/{candidate_id}")
def get_interview(
    candidate_id: str,
):

    state = interview_service.get_interview_state(
        candidate_id
    )

    if state is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        )

    return {
        "candidate_id": state["candidate_id"],
        "role": state["role"],
        "question_number": state["question_number"],
        "current_question": state["current_question"],
        "current_competency": state["current_competency"],
        "current_difficulty": state["current_difficulty"],
        "interview_complete": state[
            "interview_complete"
        ],
    }


@router.get("/interviews/{candidate_id}/report")
def get_report(
    candidate_id: str,
):

    state = interview_service.get_interview_state(
        candidate_id
    )

    if state is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        )

    if not state.get("interview_complete", False):
        raise HTTPException(
            status_code=400,
            detail="Interview is not yet complete.",
        )

    report = report_service.generate_report(
        candidate_id=state["candidate_id"],
        role=state["role"],
        evaluations=state["evaluations"],
        interview_plan=state["interview_plan"],
    )

    return report.model_dump()