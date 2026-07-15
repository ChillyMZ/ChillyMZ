import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from memory.store import add_memory, search_memories

load_dotenv()

CONSTITUTION_PATH = Path(__file__).resolve().parent.parent / "constitution.md"


def build_system_prompt(user_query: str) -> str:
    constitution = CONSTITUTION_PATH.read_text()
    top_k = int(os.environ.get("MEMORY_TOP_K", "5"))
    memories = search_memories(user_query, top_k)
    memory_block = "\n".join(f"- {m}" for m in memories) if memories else "(no relevant memories yet)"
    return f"{constitution}\n\n## Retrieved memories\n{memory_block}"


def chat(user_query: str) -> str:
    url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    model = os.environ.get("CHAT_MODEL", "llama3.1")
    system_prompt = build_system_prompt(user_query)

    resp = requests.post(
        f"{url}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            "stream": False,
        },
    )
    resp.raise_for_status()
    reply = resp.json()["message"]["content"]

    add_memory(user_query, role="user")
    add_memory(reply, role="assistant")

    return reply


def main() -> None:
    print("Personal AI (local, private). Ctrl+C to exit.")
    while True:
        try:
            user_query = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_query:
            continue
        reply = chat(user_query)
        print(f"\nai> {reply}")


if __name__ == "__main__":
    main()
