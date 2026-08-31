from src.agent.graph import interview_graph
from src.models.interview import Competency, InterviewPlan


interview_plan = InterviewPlan(
    total_questions=6,

    competencies=[
        Competency(
            name="Python",
            importance=0.25,
            question_count=2,
            difficulty=["easy", "medium"],
            question_types=["conceptual", "practical"],
        ),

        Competency(
            name="Machine Learning",
            importance=0.35,
            question_count=2,
            difficulty=["medium", "hard"],
            question_types=["conceptual", "scenario"],
        ),

        Competency(
            name="RAG",
            importance=0.40,
            question_count=2,
            difficulty=["medium", "hard"],
            question_types=["conceptual", "scenario"],
        ),
    ],

    easy_percentage=0.20,
    medium_percentage=0.50,
    hard_percentage=0.30,
)


initial_state = {
    "candidate_id": "candidate_001",
    "role": "AI Engineer",
    "interview_plan": interview_plan.model_dump(),

    "current_question": "",
    "current_answer": "",
    "current_expected_concepts": [],

    "questions_asked": [],
    "answers": [],
    "evaluations": [],

    "current_competency": "",
    "current_difficulty": "",

    "question_number": 0,
    "interview_complete": False,
}


print("Starting interview...")

config = {
    "configurable": {
        "thread_id": "candidate_001_interview_001"
    }
}

result = interview_graph.invoke(
    initial_state,
    config=config,
)

print("\nFinal State:")
print(result)