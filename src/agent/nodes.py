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

    total_questions = state["interview_plan"]["total_questions"]

    state["next_difficulty"] = next_difficulty

    if state["question_number"] >= total_questions:
        state["interview_complete"] = True

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
    Ask another question on the current competency.

    Follow-up questions stay within the same competency,
    while the adaptive engine determines the difficulty.
    """

    competency = state["current_competency"]
    difficulty = state["next_difficulty"]

    try:

        selected_question = question_selector.select_question(
            competency=competency,
            difficulty=difficulty,
            questions_asked=state["questions_asked"],
        )

    except ValueError:

        print(
            f"No unused {competency} question found "
            f"at {difficulty} difficulty."
        )

        print(
            "Skipping follow-up and continuing "
            "with the interview."
        )

        return {
            "question_number": (
                state["question_number"] + 1
            ),
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

    competency = get_competency_for_question(state)

    if competency is None:
        return {
            "interview_complete": True,
        }

    question = question_selector.select_question(
        competency=competency,
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

def get_competency_for_question(
    state: InterviewState,
) -> str | None:

    question_number = state["question_number"]

    competencies = state["interview_plan"]["competencies"]

    questions_so_far = 0

    for competency in competencies:

        questions_so_far += competency["question_count"]

        if question_number <= questions_so_far:
            return competency["name"]

    return None