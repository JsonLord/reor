import os
import requests
from dotenv import load_dotenv

load_dotenv()

BLABLADOR_API_KEY = os.getenv("BLABLADOR_API_KEY")
BLABLADOR_API_URL = "https://api.helmholtz-blablador.fz-juelich.de/v1"

def get_embedding(text: str):
    headers = {"Authorization": f"Bearer {BLABLADOR_API_KEY}"}
    response = requests.post(
        f"{BLABLADOR_API_URL}/embeddings",
        headers=headers,
        json={"input": text, "model": "alias-large"},
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def answer_question(question: str, context: str):
    headers = {"Authorization": f"Bearer {BLABLADOR_API_KEY}"}
    response = requests.post(
        f"{BLABLADOR_API_URL}/chat/completions",
        headers=headers,
        json={
            "model": "alias-large",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"},
            ],
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
