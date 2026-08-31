from src.models.report import (
    CompetencyReport,
    InterviewReport,
)


class ReportService:

    def generate_report(
        self,
        candidate_id: str,
        role: str,
        evaluations: list[dict],
        interview_plan: dict,
    ) -> InterviewReport:

        if not evaluations:
            return InterviewReport(
                candidate_id=candidate_id,
                role=role,
                total_questions=interview_plan["total_questions"],
                questions_answered=0,
                overall_score=0,
                recommendation="Insufficient data",
                competencies=[],
                strengths=[],
                weaknesses=[],
                average_score=0,
            )

        scores = [
            evaluation["score"]
            for evaluation in evaluations
        ]

        average_score = sum(scores) / len(scores)

        overall_score = average_score * 10

        competency_data = {}

        for evaluation in evaluations:

            competency = evaluation.get(
                "competency",
                "Unknown",
            )

            score = evaluation["score"]

            if competency not in competency_data:
                competency_data[competency] = []

            competency_data[competency].append(score)

        competencies = []

        for competency, competency_scores in competency_data.items():

            competencies.append(
                CompetencyReport(
                    competency=competency,
                    score=(
                        sum(competency_scores)
                        / len(competency_scores)
                    ),
                    questions=len(competency_scores),
                )
            )

        strengths = []
        weaknesses = []

        for evaluation in evaluations:

            strengths.extend(
                evaluation.get("strengths") or []
            )

            weaknesses.extend(
                evaluation.get("weaknesses") or []
            )

        strengths = list(dict.fromkeys(strengths))
        weaknesses = list(dict.fromkeys(weaknesses))

        recommendation = self._get_recommendation(
            overall_score
        )

        return InterviewReport(
            candidate_id=candidate_id,
            role=role,
            total_questions=interview_plan["total_questions"],
            questions_answered=len(evaluations),
            overall_score=round(overall_score, 2),
            recommendation=recommendation,
            competencies=competencies,
            strengths=strengths,
            weaknesses=weaknesses,
            average_score=round(average_score, 2),
        )

    def _get_recommendation(
        self,
        score: float,
    ) -> str:

        if score >= 80:
            return "Strong Candidate"

        if score >= 65:
            return "Good Candidate"

        if score >= 50:
            return "Needs Improvement"

        return "Not Recommended"