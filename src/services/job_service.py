from src.models.job import Job, JobAnalysis
from src.services.llm import get_llm


class JobAnalysisService:

    def __init__(self):
        self.llm = get_llm()
        self.structured_llm = self.llm.with_structured_output(
            JobAnalysis
        )

    def analyze(self, job: Job) -> JobAnalysis:

        prompt = f"""
You are an expert technical recruiter.

Analyze the following job description.

Extract:
1. The actual job role.
2. Minimum required years of experience.
3. Maximum years of experience if specified.
4. Important technical and soft-skill competencies.
5. A short description of what each competency means
   in the context of this role.

Job Description:

{job.description}
"""

        return self.structured_llm.invoke(prompt)