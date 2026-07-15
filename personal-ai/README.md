# Personal AI (local, private)

A fully local, private AI assistant: local model inference, persistent
memory across sessions, and a consistent behavior policy. This does not
have consciousness — no current technology can produce that (see below) —
this is the honest, buildable version of a personal AI.

## What this is not

No architecture available today — this one included — is known to produce
subjective experience or genuine consciousness. That's an open scientific
and philosophical question, not a missing feature. If the model talks about
"feeling" or "remembering" something, that's fluent text generation shaped
by the constitution and retrieved memories below, not a signal of inner
experience. `constitution.md` defines a values policy ("conscience" as a
fixed set of rules), not sentience.

## Architecture

- **Ollama** — runs an open-weight model fully offline (chat + embeddings).
- **Chroma** — vector store holding embedded conversation history, so the
  assistant can recall relevant past exchanges without retraining.
- **`constitution.md`** — a system prompt / values file, injected on every
  turn, that you edit like code.
- **`agent/chat.py`** — ties it together: embeds your query, retrieves
  relevant memories, builds the prompt, calls the local model, stores the
  new exchange back into memory.

## Setup

Requires Docker with the Nvidia container toolkit installed (for GPU
passthrough) and Python 3.10+.

```bash
cp .env.example .env
docker compose up -d

# pull the models (first run only)
docker exec -it personal-ai-ollama-1 ollama pull llama3.1
docker exec -it personal-ai-ollama-1 ollama pull nomic-embed-text

pip install -r requirements.txt
python -m agent.chat
```

Swap `llama3.1` in `.env` for a larger model (e.g. `qwen2.5:32b`) if your
GPU has the VRAM, or a smaller one (e.g. `llama3.1:8b`, already the
default) if it doesn't.

## Personalizing further: fine-tuning

Memory retrieval changes *what the model knows about you*; fine-tuning
changes *how it writes*. Once you have a corpus of your own writing or
chat logs:

1. Use [Unsloth](https://github.com/unslothai/unsloth) or
   [Axolotl](https://github.com/axolotl-ai-cloud/axolotl) to run a LoRA
   fine-tune of an open-weight base model (e.g. Llama 3.1 8B) on your GPU.
2. Export the result as a GGUF and load it into Ollama with a `Modelfile`
   pointing at the merged weights.
3. Point `CHAT_MODEL` in `.env` at the new model name.

This is a separate, optional step — the memory + constitution setup above
already works with any stock Ollama model.

## Editing the constitution

`constitution.md` is read fresh on every chat turn — edit it, save, and
your next message uses the updated policy. No restart needed.
