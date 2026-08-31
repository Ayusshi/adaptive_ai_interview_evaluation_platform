from src.models.interview import (
    Competency,
    InterviewPlan,
)


class InterviewPlanner:

    def __init__(self, total_questions: int = 15):
        self.total_questions = total_questions

    def create_plan(
        self,
        competencies: list[dict],
    ) -> InterviewPlan:

        if not competencies:
            raise ValueError("At least one competency is required.")

        competencies = self._normalize_importance(
            competencies
        )

        planned_competencies = self._allocate_questions(
            competencies
        )

        return InterviewPlan(
            total_questions=self.total_questions,
            competencies=planned_competencies,
            easy_percentage=0.20,
            medium_percentage=0.50,
            hard_percentage=0.30,
        )

    def _normalize_importance(
        self,
        competencies: list[dict],
    ) -> list[dict]:

        total_importance = sum(
            competency["importance"]
            for competency in competencies
        )

        if total_importance <= 0:
            raise ValueError(
                "Total competency importance must be greater than 0."
            )

        for competency in competencies:
            competency["importance"] = (
                competency["importance"]
                / total_importance
            )

        return competencies

    def _allocate_questions(
        self,
        competencies: list[dict],
    ) -> list[Competency]:

        raw_counts = [
            competency["importance"] * self.total_questions
            for competency in competencies
        ]

        question_counts = [
            max(1, int(count))
            for count in raw_counts
        ]

        current_total = sum(question_counts)

        while current_total < self.total_questions:

            largest_index = max(
                range(len(competencies)),
                key=lambda i: (
                    raw_counts[i] - int(raw_counts[i])
                ),
            )

            question_counts[largest_index] += 1
            current_total += 1

        while current_total > self.total_questions:

            largest_index = max(
                range(len(competencies)),
                key=lambda i: question_counts[i],
            )

            if question_counts[largest_index] > 1:
                question_counts[largest_index] -= 1
                current_total -= 1
            else:
                break

        result = []

        for competency, question_count in zip(
            competencies,
            question_counts,
        ):

            result.append(
                Competency(
                    name=competency["name"],
                    importance=competency["importance"],
                    question_count=question_count,
                    difficulty=competency.get(
                        "difficulty",
                        ["easy", "medium"],
                    ),
                    question_types=competency.get(
                        "question_types",
                        ["conceptual", "practical"],
                    ),
                )
            )

        return result