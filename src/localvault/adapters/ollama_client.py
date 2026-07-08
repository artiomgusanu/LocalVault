import ollama


class OllamaClient:

    def __init__(self, model: str = "qwen3:8b"):
        self.model = model

    def chat(self, prompt: str, format: dict | str | None = None) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            format=format,
            think=False,
        )

        return response["message"]["content"]