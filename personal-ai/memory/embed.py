import os
import requests


def embed(text: str) -> list[float]:
    url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    model = os.environ.get("EMBED_MODEL", "nomic-embed-text")
    resp = requests.post(f"{url}/api/embeddings", json={"model": model, "prompt": text})
    resp.raise_for_status()
    return resp.json()["embedding"]
