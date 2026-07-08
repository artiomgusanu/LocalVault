import json

from localvault.domain.models import Classification
from localvault.adapters.ollama_client import OllamaClient
from localvault.domain.errors import ClassificationError
from localvault.domain.categories import KNOWN_CATEGORIES


CATEGORIES_LINE = ", ".join(sorted(KNOWN_CATEGORIES))


PROMPT_TEMPLATE = """
Classify the document below.

The "category" field MUST be exactly one of these values, in English,
written exactly as shown:
__CATEGORIES__

Respond ONLY with valid JSON, no text before or after.

DOCUMENT:
__DOCUMENT_TEXT__
"""


client = OllamaClient()


def classify_document(document_text: str) -> Classification:
    prompt = PROMPT_TEMPLATE.replace("__CATEGORIES__", CATEGORIES_LINE)
    prompt = prompt.replace("__DOCUMENT_TEXT__", document_text)

    response = client.chat(
        prompt,
        format=Classification.model_json_schema(),
    )

    try:
        data = json.loads(response)
        return Classification(**data)
    except (json.JSONDecodeError, ValueError) as e:
        raise ClassificationError(f"Could not parse LLM output: {e}") from e