import os
import requests


class LocalLLM:

    def __init__(
        self,
        model: str = "llama3.2:3b",
    ):
        self.model = model

        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        )

    def generate(
        self,
        prompt: str,
        json_mode: bool = False,
    ):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        if json_mode:
            payload["format"] = "json"

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

        return response.json()["response"]