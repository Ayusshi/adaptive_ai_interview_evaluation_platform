from src.services.interview_service import InterviewPlanner


def test_interview_plan():

    competencies = [
        {
            "name": "Python",
            "importance": 8,
            "difficulty": ["easy", "medium", "hard"],
            "question_types": [
                "conceptual",
                "practical",
                "debugging",
            ],
        },
        {
            "name": "Machine Learning",
            "importance": 9,
            "difficulty": ["medium", "hard"],
            "question_types": [
                "conceptual",
                "scenario",
            ],
        },
        {
            "name": "LLMs",
            "importance": 10,
            "difficulty": ["medium", "hard"],
            "question_types": [
                "conceptual",
                "scenario",
                "system_design",
            ],
        },
        {
            "name": "RAG",
            "importance": 10,
            "difficulty": ["medium", "hard"],
            "question_types": [
                "conceptual",
                "practical",
                "scenario",
            ],
        },
        {
            "name": "Docker",
            "importance": 4,
            "difficulty": ["easy", "medium"],
            "question_types": [
                "conceptual",
                "practical",
            ],
        },
    ]

    planner = InterviewPlanner(total_questions=15)

    plan = planner.create_plan(competencies)

    assert plan.total_questions == 15

    assert sum(
        competency.question_count
        for competency in plan.competencies
    ) == 15