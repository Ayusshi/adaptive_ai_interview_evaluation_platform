from src.agent.graph import interview_graph


class InterviewService:

    def start_interview(
        self,
        candidate_id: str,
        role: str,
        interview_plan: dict,
    ):
        thread_id = f"{candidate_id}_interview"

        initial_state = {
            "candidate_id": candidate_id,
            "role": role,
            "interview_plan": interview_plan,

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
                "thread_id": thread_id,
            }
        }

        state = interview_graph.invoke(
            initial_state,
            config=config,
        )

        return state

    def submit_answer(
        self,
        candidate_id: str,
        answer: str,
    ):
        thread_id = f"{candidate_id}_interview"

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        state = interview_graph.invoke(
            {
                "current_answer": answer,
            },
            config=config,
        )

        return state

    def get_interview_state(
        self,
        candidate_id: str,
    ):
        thread_id = f"{candidate_id}_interview"

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        state = interview_graph.get_state(config)

        if not state.values:
            return None

        return state.values