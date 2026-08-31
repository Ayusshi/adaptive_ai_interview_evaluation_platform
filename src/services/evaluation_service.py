import json

from pydantic import ValidationError

from src.models.evaluation import AnswerEvaluation
from src.prompts.evaluation_prompt import (
    SYSTEM_PROMPT,
    build_evaluation_prompt,
)
from src.services.llm import LocalLLM


class AnswerEvaluator:

    def __init__(self, llm: LocalLLM):
        self.llm = llm

    def evaluate(
        self,
        role: str,
        competency: str,
        difficulty: str,
        question: str,
        candidate_answer: str,
        expected_concepts: list[str],
    ) -> AnswerEvaluation:

        prompt = build_evaluation_prompt(
            role=role,
            competency=competency,
            difficulty=difficulty,
            question=question,
            candidate_answer=candidate_answer,
            expected_concepts=expected_concepts,
        )

        full_prompt = f"""
{SYSTEM_PROMPT}

{prompt}
"""

        response = self.llm.generate(full_prompt)

        try:
            parsed_response = json.loads(response)

            # Normalize nullable list fields
            parsed_response["strengths"] = (
                parsed_response.get("strengths") or []
            )

            parsed_response["weaknesses"] = (
                parsed_response.get("weaknesses") or []
            )

            parsed_response["missing_concepts"] = (
                parsed_response.get("missing_concepts") or []
            )

            # Normalize nullable scalar fields
            parsed_response["feedback"] = (
                parsed_response.get("feedback") or ""
            )

            parsed_response["needs_followup"] = bool(
                parsed_response.get(
                    "needs_followup",
                    False,
                )
            )

            parsed_response["score"] = int(
                parsed_response.get(
                    "score",
                    0,
                )
            )

            return AnswerEvaluation.model_validate(
                parsed_response
            )

        except (
            json.JSONDecodeError,
            ValidationError,
            TypeError,
            ValueError,
        ) as exc:

            print(
                "Warning: LLM response could not be validated."
            )

            print(
                f"Raw response: {response}"
            )

            raise ValueError(
                "LLM response does not match the "
                "answer evaluation schema."
            ) from exc