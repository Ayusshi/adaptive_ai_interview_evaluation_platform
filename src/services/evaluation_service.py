import json

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

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            json_mode=True,
        )

        try:
            raw_evaluation = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON during answer evaluation."
            ) from exc

        # Small robustness improvement:
        # if the model wraps the object inside "evaluation",
        # unwrap it.
        if (
            isinstance(raw_evaluation, dict)
            and "evaluation" in raw_evaluation
        ):
            raw_evaluation = raw_evaluation["evaluation"]

        try:
            return AnswerEvaluation.model_validate(
                raw_evaluation
            )
        except Exception as exc:
            raise ValueError(
                "LLM response does not match the "
                "answer evaluation schema."
            ) from exc