from fastapi import FastAPI

from src.api.routes import router


app = FastAPI(
    title="Adaptive AI Interview Evaluation Platform",
    description=(
        "An adaptive AI-powered interview "
        "evaluation system."
    ),
    version="1.0.0",
)


app.include_router(router)