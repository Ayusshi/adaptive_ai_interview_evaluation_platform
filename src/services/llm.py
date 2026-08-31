import requests


class LocalLLM:

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2:3b",
    ):
        self.base_url = base_url
        self.model = model

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        json_mode: bool = False,
    ) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
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