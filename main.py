from src.agent.graph import interview_graph


initial_state = {
    "candidate_id": "candidate_001",
    "role": "AI Engineer",
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
    "thread_id": "candidate_001_interview_006"    
    }
}


# --------------------------------------------------
# Start interview
# --------------------------------------------------

result = interview_graph.invoke(
    initial_state,
    config=config,
)


# --------------------------------------------------
# Interview loop
# --------------------------------------------------

while not result.get("interview_complete", False):

    question = result["current_question"]

    print(
        f"\nQuestion {result['question_number']}:"
    )

    print(question)

    answer = input("\nYour answer: ")

    result = interview_graph.invoke(
        {
            "current_answer": answer,
        },
        config=config,
    )

    print(
        f"\nEvaluation score: "
        f"{result['evaluations'][-1]['score']}"
    )

    print(
        f"Current difficulty: "
        f"{result['current_difficulty']}"
    )

    print(
        f"Next difficulty: "
        f"{result['next_difficulty']}"
    )


print("\nInterview completed!")

print("\nFinal State:")
print(result)