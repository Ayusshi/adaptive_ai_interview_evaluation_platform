from src.services.retrieval_service import KnowledgeRetriever
from src.agent.state import InterviewState
from src.services.evaluation_service import AnswerEvaluator
from src.services.llm import LocalLLM
from src.services.question_selector import QuestionSelector
from src.services.adaptive_engine import AdaptiveEngine


llm = LocalLLM()

question_selector = QuestionSelector()

knowledge_retriever = KnowledgeRetriever()

answer_evaluator = AnswerEvaluator(
    llm,
    knowledge_retriever,
)

adaptive_engine = AdaptiveEngine()

def route_entry(state: InterviewState) -> str:

    if state.get("current_answer"):
        return "submit_answer"

    return "start_interview"

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
    answer = state["current_answer"]

    return {
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

    # The current question has just been evaluated.
    # If we have reached the total number of planned
    # questions, finish the interview.

    total_questions = state["interview_plan"]["total_questions"]

    if state["question_number"] >= total_questions:
        return "complete"

    evaluation = state["evaluations"][-1]

    # A follow-up stays within the current competency.
    if evaluation["needs_followup"]:

        try:

            question_selector.select_question(
                competency=state["current_competency"],
                difficulty=state["current_difficulty"],
                questions_asked=state["questions_asked"],
            )

            return "follow_up"

        except ValueError:

            print(
                "No unused follow-up question available."
            )

            print(
                "Continuing with the planned "
                "next competency."
            )

    return "next_question"


def ask_follow_up(
    state: InterviewState,
):

    try:

        selected_question = question_selector.select_question(
            competency=state["current_competency"],
            difficulty=state["current_difficulty"],
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
            "question_number": state["question_number"] + 1,
        }

    except ValueError:

        print(
            "No unused follow-up question available."
        )

        print(
            "Skipping follow-up and continuing "
            "with the interview."
        )

        return {
            "question_number": state["question_number"],
        }


def ask_next_question(
    state: InterviewState,
) -> InterviewState:

    plan = state["interview_plan"]
    competencies = plan["competencies"]

    question_number = state["question_number"]

    # --------------------------------------------------
    # Determine which competency should handle this
    # question based on the interview plan.
    #
    # Example:
    # Q1-Q2 -> Python
    # Q3-Q4 -> Machine Learning
    # Q5-Q6 -> RAG
    # --------------------------------------------------

    current_position = 0
    selected_competency = None

    for competency in competencies:

        question_count = competency["question_count"]

        if question_number <= current_position + question_count:
            selected_competency = competency
            break

        current_position += question_count

    # Safety check
    if selected_competency is None:
        return {
            "interview_complete": True,
        }

    competency_name = selected_competency["name"]
    available_difficulties = selected_competency["difficulty"]

    # --------------------------------------------------
    # Start with the difficulty determined by the
    # adaptive engine.
    # --------------------------------------------------

    difficulty = state.get(
        "next_difficulty",
        available_difficulties[0],
    )

    # If the adaptive engine selected a difficulty that
    # isn't available for this competency, use the first
    # difficulty defined by the competency.
    if difficulty not in available_difficulties:

        difficulty = available_difficulties[0]

    print(
        f"Selecting next question: "
        f"{competency_name} / {difficulty}"
    )

    # --------------------------------------------------
    # Try the adaptive difficulty first.
    # --------------------------------------------------

    question = None

    try:

        question = question_selector.select_question(
            competency=competency_name,
            difficulty=difficulty,
            questions_asked=state["questions_asked"],
        )

    except ValueError:

        print(
            f"No unused {competency_name} question "
            f"found at {difficulty} difficulty."
        )

    # --------------------------------------------------
    # If no question exists at the adaptive difficulty,
    # try the other difficulties for THIS competency.
    # --------------------------------------------------

    if question is None:

        for fallback_difficulty in available_difficulties:

            if fallback_difficulty == difficulty:
                continue

            try:

                question = question_selector.select_question(
                    competency=competency_name,
                    difficulty=fallback_difficulty,
                    questions_asked=state["questions_asked"],
                )

                print(
                    f"Falling back to "
                    f"{fallback_difficulty} difficulty."
                )

                break

            except ValueError:
                continue

    # --------------------------------------------------
    # If there are no questions left for this competency,
    # don't crash the entire interview.
    #
    # The interview plan determines the next competency,
    # so simply mark this question as skipped.
    # --------------------------------------------------

    if question is None:

        print(
            f"No unused {competency_name} questions "
            f"available."
        )

        return {
            "question_number": question_number + 1,
        }

    # --------------------------------------------------
    # Store the selected question.
    # --------------------------------------------------

    return {
        "current_question": question["question"],
        "current_competency": question["competency"],
        "current_difficulty": question["difficulty"],
        "current_expected_concepts": question[
            "expected_concepts"
        ],
        "questions_asked": [
            *state["questions_asked"],
            question["question"],
        ],
        "question_number": question_number + 1,
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