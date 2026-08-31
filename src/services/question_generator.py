import json
from collections import Counter

from src.models.interview import GeneratedQuestions, InterviewQuestion
from src.prompts.question_generation import (
    SYSTEM_PROMPT,
    build_question_generation_prompt,
)
from src.services.llm import LocalLLM


class QuestionGenerator:

    def __init__(self, llm: LocalLLM):
        self.llm = llm

    def generate(
        self,
        role: str,
        plan: dict,
    ) -> list[InterviewQuestion]:

        prompt = build_question_generation_prompt(
            role=role,
            plan=plan,
        )

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            json_mode=True,
        )

        try:
            raw_questions = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON."
            ) from exc
        print("\n========== RAW LLM RESPONSE ==========")
        print(response)
        print("======================================\n")

        try:
            generated_questions = GeneratedQuestions.model_validate(
                raw_questions
            )
        except Exception as exc:
            raise ValueError(
                "LLM response does not match the expected question schema."
            ) from exc

        questions = generated_questions.questions

        if len(questions) != plan["total_questions"]:
            raise ValueError(
                f"Expected {plan['total_questions']} questions, "
                f"but received {len(questions)}."
            )

        self._validate_against_plan(
            questions,
            plan,
        )

        return questions

    def _validate_against_plan(
        self,
        questions: list[InterviewQuestion],
        plan: dict,
    ) -> None:

        expected_counts = {
            competency["name"]: competency["question_count"]
            for competency in plan["competencies"]
        }

        actual_counts = Counter(
            question.competency
            for question in questions
        )

        for competency, expected_count in expected_counts.items():

            actual_count = actual_counts.get(
                competency,
                0,
            )

            if actual_count != expected_count:
                raise ValueError(
                    f"Competency '{competency}' expected "
                    f"{expected_count} questions, "
                    f"but received {actual_count}."
                )