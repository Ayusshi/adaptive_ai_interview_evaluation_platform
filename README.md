# Adaptive AI Interview Evaluation Platform

An AI-powered interview evaluation platform that conducts adaptive technical interviews, evaluates candidate answers using an LLM, retrieves relevant knowledge using RAG, and dynamically adjusts interview difficulty based on candidate performance.

The system is designed as an Applied AI project demonstrating how LLMs, RAG, structured outputs, LangGraph, and FastAPI can be combined to build a practical AI application.

---

## 🚀 Features

- Adaptive technical interview generation
- Competency-based interview planning
- Difficulty adaptation based on candidate performance
- LLM-based answer evaluation
- Structured answer evaluation using Pydantic
- Retrieval-Augmented Generation (RAG)
- Knowledge retrieval using embeddings and FAISS
- Grounded LLM evaluation using retrieved knowledge
- Follow-up question generation
- LangGraph-based interview workflow
- Interview state management
- Persistent interview state using LangGraph checkpointing
- Final candidate evaluation report
- FastAPI REST API
- Interactive Swagger API documentation
- Docker-ready deployment configuration
- Local LLM support using Ollama

---

## 🧠 System Overview

The platform follows this high-level workflow:

```text
Candidate
   │
   ▼
Start Interview
   │
   ▼
Interview Planner
   │
   ▼
Question Selection
   │
   ▼
Candidate Answer
   │
   ▼
RAG Knowledge Retrieval
   │
   ▼
LLM Evaluation
   │
   ▼
Structured Evaluation
   │
   ▼
Adaptive Engine
   │
   ├──────────────► Follow-up Question
   │
   └──────────────► Next Question
                         │
                         ▼
                  Interview Complete
                         │
                         ▼
                  Final Report


Build the image:

docker build -t adaptive-interview-platform .

Run the container:

docker run -p 8000:8000 adaptive-interview-platform

Run the application
uvicorn src.api.app:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs