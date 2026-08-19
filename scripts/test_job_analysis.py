from src.models.job import Job
from src.services.job_service import JobAnalysisService


job = Job(
    title="AI Engineer",
    description="""
    We are looking for an AI Engineer with 2–4 years
    of experience. The candidate should have strong
    Python programming skills and experience building
    REST APIs using FastAPI. Experience with SQL,
    Docker, LLM applications, RAG pipelines and vector
    databases is preferred. Candidates should also have
    good problem-solving and communication skills.
    """
)

service = JobAnalysisService()

result = service.analyze(job)

print(result.model_dump_json(indent=2))