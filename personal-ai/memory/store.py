import os
import time
import uuid

import chromadb

from memory.embed import embed

COLLECTION_NAME = "personal_ai_memory"


def get_collection():
    host = os.environ.get("CHROMA_HOST", "localhost")
    port = int(os.environ.get("CHROMA_PORT", "8000"))
    client = chromadb.HttpClient(host=host, port=port)
    return client.get_or_create_collection(COLLECTION_NAME)


def add_memory(text: str, role: str) -> None:
    collection = get_collection()
    collection.add(
        ids=[str(uuid.uuid4())],
        embeddings=[embed(text)],
        documents=[text],
        metadatas=[{"role": role, "ts": time.time()}],
    )


def search_memories(query: str, top_k: int) -> list[str]:
    collection = get_collection()
    if collection.count() == 0:
        return []
    results = collection.query(query_embeddings=[embed(query)], n_results=min(top_k, collection.count()))
    return results["documents"][0]
