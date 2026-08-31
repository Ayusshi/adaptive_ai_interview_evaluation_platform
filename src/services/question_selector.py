from src.services.question_bank import QUESTION_BANK


class QuestionSelector:

    def select_question(
        self,
        competency: str,
        difficulty: str,
        questions_asked: list[str],
    ) -> dict:

        for question in QUESTION_BANK:

            if question["competency"] != competency:
                continue

            if question["difficulty"] != difficulty:
                continue

            if question["question"] in questions_asked:
                continue

            return question

        raise ValueError(
            f"No unused question found for "
            f"{competency} at {difficulty} difficulty."
        )