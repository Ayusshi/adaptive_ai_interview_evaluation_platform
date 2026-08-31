from src.agent.state import InterviewState
from src.services.evaluation_service import AnswerEvaluator
from src.services.llm import LocalLLM
from src.services.question_selector import QuestionSelector
from src.services.adaptive_engine import AdaptiveEngine


llm = LocalLLM()
question_selector = QuestionSelector()
answer_evaluator = AnswerEvaluator(llm)
adaptive_engine = AdaptiveEngine()


def start_interview(
    state: InterviewState,
):
    print("Starting interview...")

    return {
        "question_number": 1,
        "interview_complete": False,
    }


def ask_question(
    state: InterviewState,
):
    plan = state["interview_plan"]

    competencies = plan["competencies"]

    competency_index = (
        state["question_number"] - 1
    ) % len(competencies)

    competency = competencies[competency_index]

    selected_question = question_selector.select_question(
        competency=competency["name"],
        difficulty=competency["difficulty"][0],
        questions_asked=state["questions_asked"],
    )

    return {
        "current_question": selected_question["question"],
        "current_competency": selected_question["competency"],
        "current_difficulty": selected_question["difficulty"],
        "current_expected_concepts": selected_question[
            "expected_concepts"
        ],
        "questions_asked": [
            *state["questions_asked"],
            selected_question["question"],
        ],
    }


def receive_answer(
    state: InterviewState,
):
    # Temporary simulated candidate answer.
    # This will eventually come from the API/UI.

    answer = (
        "RAG retrieves relevant information from an "
        "external knowledge base and provides it to "
        "the language model as context."
    )

    return {
        "current_answer": answer,
        "answers": [
            *state["answers"],
            answer,
        ],
    }


def evaluate_answer(
    state: InterviewState,
):
    evaluation = answer_evaluator.evaluate(
        role=state["role"],
        competency=state["current_competency"],
        difficulty=state["current_difficulty"],
        question=state["current_question"],
        candidate_answer=state["current_answer"],
        expected_concepts=state[
            "current_expected_concepts"
        ],
    )

    return {
        "evaluations": [
            *state["evaluations"],
            evaluation.model_dump(),
        ],
    }


def decide_next_step(
    state: InterviewState,
) -> InterviewState:

    evaluation = state["evaluations"][-1]

    score = evaluation["score"]

    next_difficulty = adaptive_engine.decide_next_difficulty(
        score=score,
        current_difficulty=state["current_difficulty"],
    )

    state["next_difficulty"] = next_difficulty

    print(
        f"Evaluation score: {score}"
    )

    print(
        f"Current difficulty: "
        f"{state['current_difficulty']}"
    )

    print(
        f"Next difficulty: "
        f"{next_difficulty}"
    )

    return state


def route_after_decision(
    state: InterviewState,
) -> str:

    total_questions = state["interview_plan"]["total_questions"]

    if state["question_number"] >= total_questions:
        return "complete"

    evaluation = state["evaluations"][-1]

    if evaluation["needs_followup"]:
        return "follow_up"

    return "next_question"


def ask_follow_up(
    state: InterviewState,
):
    """
    Select a follow-up question for the same competency.

    We first try the adaptive difficulty calculated by
    AdaptiveEngine. If the question pool does not contain
    an unused question at that difficulty, we fall back
    to the current difficulty.

    This is temporary behavior while the question bank
    is still small.
    """

    competency = state["current_competency"]
    next_difficulty = state["next_difficulty"]

    try:
        selected_question = question_selector.select_question(
            competency=competency,
            difficulty=next_difficulty,
            questions_asked=state["questions_asked"],
        )

    except ValueError:

        print(
            f"No unused {competency} question found "
            f"at {next_difficulty} difficulty."
        )

        print(
            "Falling back to current difficulty."
        )

        try:
            selected_question = question_selector.select_question(
                competency=competency,
                difficulty=state["current_difficulty"],
                questions_asked=state["questions_asked"],
            )

        except ValueError:

            print(
                "No unused follow-up question available. "
                "Continuing to next question."
            )

            return {
                "question_number": (
                    state["question_number"] + 1
                ),
                "interview_complete": False,
            }

    return {
        "current_question": selected_question["question"],
        "current_competency": selected_question["competency"],
        "current_difficulty": selected_question["difficulty"],
        "current_expected_concepts": selected_question[
            "expected_concepts"
        ],
        "questions_asked": [
            *state["questions_asked"],
            selected_question["question"],
        ],
        "question_number": (
            state["question_number"] + 1
        ),
    }


def ask_next_question(
    state: InterviewState,
) -> InterviewState:

    question = question_selector.select_question(
        competency=state["current_competency"],
        difficulty=state["next_difficulty"],
        questions_asked=state["questions_asked"],
    )

    return {
        "current_question": question["question"],
        "current_competency": question["competency"],
        "current_expected_concepts": question[
            "expected_concepts"
        ],
        "current_difficulty": question["difficulty"],
        "questions_asked": [
            *state["questions_asked"],
            question["question"],
        ],
        "question_number": (
            state["question_number"] + 1
        ),
    }