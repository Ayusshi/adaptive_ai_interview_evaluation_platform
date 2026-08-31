from fastapi import APIRouter, HTTPException

from src.agent.graph import interview_graph
from src.api.schemas import (
    StartInterviewRequest,
    StartInterviewResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    FinalReportResponse,
)
from src.services.report_service import ReportService


router = APIRouter()

report_service = ReportService()


def build_thread_id(candidate_id: str) -> str:
    return f"{candidate_id}_interview"


@router.post(
    "/interviews/start",
    response_model=StartInterviewResponse,
)
def start_interview(
    request: StartInterviewRequest,
):

    initial_state = {
        "candidate_id": request.candidate_id,
        "role": request.role,
        "interview_plan": {
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
        },
        "current_question": "",
        "current_answer": "",
        "current_competency": "",
        "current_difficulty": "",
        "current_expected_concepts": [],
        "questions_asked": [],
        "answers": [],
        "evaluations": [],
        "next_difficulty": "",
        "question_number": 1,
        "interview_complete": False,
    }

    config = {
        "configurable": {
            "thread_id": build_thread_id(
                request.candidate_id
            ),
        }
    }

    result = interview_graph.invoke(
        initial_state,
        config=config,
    )

    return StartInterviewResponse(
        candidate_id=result["candidate_id"],
        role=result["role"],
        question_number=result["question_number"],
        question=result["current_question"],
        competency=result["current_competency"],
        difficulty=result["current_difficulty"],
    )


@router.post(
    "/interviews/{candidate_id}/answer",
    response_model=SubmitAnswerResponse,
)
def submit_answer(
    candidate_id: str,
    request: SubmitAnswerRequest,
):

    if candidate_id != request.candidate_id:
        raise HTTPException(
            status_code=400,
            detail="Candidate ID mismatch.",
        )

    config = {
        "configurable": {
            "thread_id": build_thread_id(
                candidate_id
            ),
        }
    }

    result = interview_graph.invoke(
        {
            "current_answer": request.answer,
        },
        config=config,
    )

    evaluation = result["evaluations"][-1]

    return SubmitAnswerResponse(
        question_number=result["question_number"],
        score=evaluation["score"],
        feedback=evaluation["feedback"],
        current_difficulty=result["current_difficulty"],
        next_difficulty=result["next_difficulty"],
        next_question=(
            None
            if result["interview_complete"]
            else result["current_question"]
        ),
        interview_complete=result["interview_complete"],
    )


@router.get(
    "/interviews/{candidate_id}/report",
    response_model=FinalReportResponse,
)
def get_report(
    candidate_id: str,
):

    config = {
        "configurable": {
            "thread_id": build_thread_id(
                candidate_id
            ),
        }
    }

    try:
        result = interview_graph.get_state(
            config
        ).values

    except Exception as exc:

        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        ) from exc

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        )

    report = report_service.generate_report(
        candidate_id=result["candidate_id"],
        role=result["role"],
        evaluations=result["evaluations"],
        interview_plan=result["interview_plan"],
    )

    return report.model_dump()