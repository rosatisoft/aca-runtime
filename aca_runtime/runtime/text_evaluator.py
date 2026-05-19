import os

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from .evaluator import evaluate_vector


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> np.ndarray:
    load_dotenv()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input=text,
        model=model,
        encoding_format="float",
    )

    vector = np.array(response.data[0].embedding, dtype=float)

    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm

    return vector


def evaluate_text(text: str, atlas: dict, model: str = DEFAULT_EMBEDDING_MODEL) -> dict:
    vector = embed_text(text, model=model)
    result = evaluate_vector(vector, atlas)

    result["input_text"] = text
    result["embedding_model"] = model
    result["embedding_dim"] = int(vector.shape[0])

    return result