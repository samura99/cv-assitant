import os


class ConfigGPT:
    MODEL_PRICE = {
        "gpt-3.5-turbo": {
            "input": 0.5 / 1000000,
            "output": 1.5 / 1000000,
        },
        "gpt-4o-mini": {
            "input": 0.15 / 1000000,
            "output": 0.60 / 1000000,
        },
    }

    DEFAULT_MODEL_NAME = "gpt-4o-mini"

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    PROJECTS_KEYS = ["id", "title", "keywords", "skills", "languages"]

    STRONG_FIELDS = [
        "name",
        "bachelor",
        "university",
        "study_fields",
        "languajes",
        "Knowledge",
        "programming_languajes",
        "skills",
        "about",
        "interests",
    ]
