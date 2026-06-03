# 🍽️ llmbuffet — one free LLM API gateway for every free tier

**A free, OpenAI-compatible LLM gateway that pools Groq, Cerebras, Gemini, OpenRouter, GitHub Models, Cloudflare & more behind one endpoint — with automatic failover and quota tracking.**

[![CI](https://github.com/0xzr/llmbuffet/actions/workflows/ci.yml/badge.svg)](https://github.com/0xzr/llmbuffet/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)

> Stop juggling a dozen free LLM SDKs and rate limits. Point your OpenAI client at `llmbuffet` and never pay for a hobby project's inference again.

Groq, Cerebras, Google Gemini, OpenRouter, GitHub Models, Cloudflare Workers AI, Mistral, Cohere, SambaNova — each hands out a generous **free tier**, but each has its own SDK, its own rate limits, and its own daily cap. `llmbuffet` puts all of them into one pool:

- 🔌 **One OpenAI-compatible endpoint.** Point any existing OpenAI SDK / tool at `llmbuffet` and it just works — no code changes.
- 🔁 **Automatic failover.** Hit a rate limit or a 5xx on one provider? `llmbuffet` transparently moves to the next.
- 📊 **Quota-aware routing.** Spreads load least-used-first and respects each provider's free daily limit, so you squeeze the most out of every tier.
- 🧩 **One catalog, your keys.** Drop in the keys you have; `llmbuffet` skips the rest. No key is ever stored in the repo.
- 🪶 **Tiny.** Pure-Python, one dependency (`httpx`). The proxy runs on the standard library.

> Why it exists: stitching together a dozen free LLM tiers by hand is fiddly and breaks constantly. `llmbuffet` makes "never pay for a hobby project's LLM calls again" a one-command setup.

---

## Install

```bash
pip install llmbuffet      # or: pipx install llmbuffet
```

## 60-second quickstart

1. Grab one or more free API keys — **all free, no credit card**. You only need
   **one** to start (Groq and Cerebras are the fastest to sign up for).
   👉 **[docs/ACCOUNTS.md](docs/ACCOUNTS.md) has 1-minute, click-by-click steps for every provider.**

   | Provider | Get a key |
   |---|---|
   | Groq | <https://console.groq.com/keys> |
   | Cerebras | <https://cloud.cerebras.ai> |
   | OpenRouter | <https://openrouter.ai/keys> |
   | Google Gemini | <https://aistudio.google.com/apikey> |
   | GitHub Models | any GitHub PAT |

2. Export the ones you have (see [`.env.example`](.env.example) for all of them):

   ```bash
   export GROQ_API_KEY=gsk_...
   export CEREBRAS_API_KEY=csk-...
   ```

3. Ask something:

   ```bash
   llmbuffet ask "Explain the CAP theorem in one sentence."
   ```

   or pipe context in:

   ```bash
   cat error.log | llmbuffet ask "What's the root cause here?"
   ```

Check what's wired up:

```bash
llmbuffet providers
```

```
llmbuffet catalog: 9 providers, 24 models

  ✓ groq         Groq                          4 models   [configured]
  ✓ cerebras     Cerebras                      3 models   [configured]
  · openrouter   OpenRouter (free models)      3 models   [set OPENROUTER_API_KEY]
  · gemini       Google Gemini                 2 models   [set GEMINI_API_KEY]
  ...
```

## The killer feature: a drop-in OpenAI proxy

Run the gateway:

```bash
llmbuffet proxy --port 8080
```

Now point **any** OpenAI-compatible app or SDK at it — no other changes:

```bash
export OPENAI_BASE_URL=http://localhost:8080/v1
export OPENAI_API_KEY=anything        # llmbuffet ignores it
```

```python
from openai import OpenAI

client = OpenAI()  # picks up OPENAI_BASE_URL
resp = client.chat.completions.create(
    model="auto",                      # or "groq", or "groq/llama-3.3-70b-versatile"
    messages=[{"role": "user", "content": "Say hi in French."}],
)
print(resp.choices[0].message.content)
```

The `model` field controls routing:

| `model` value | Routes to |
|---|---|
| `auto` (or omitted) | any configured provider, least-used first |
| `groq` | any model on Groq |
| `groq/llama-3.3-70b-versatile` | that exact model |
| `llama-3.3-70b-versatile` | that model on any provider that has it |

## Use it as the free LLM backend for your AI agent

Coding agents and agent frameworks (aider, Continue, Cline, the OpenAI Agents SDK, LangChain, ...) almost all speak the OpenAI API — so they can run on pooled free inference through `llmbuffet`, with **failover when one provider rate-limits you mid-run** (exactly when long agent loops tend to die):

```bash
llmbuffet proxy --port 8080
export OPENAI_BASE_URL=http://localhost:8080/v1 OPENAI_API_KEY=anything
aider --model openai/auto          # or point any OpenAI-compatible tool here
```

Full integration snippets (aider, LangChain, Continue/Cline, OpenAI Agents SDK) are in **[docs/AGENTS.md](docs/AGENTS.md)**.

## Use it as a library

```python
from llmbuffet import Buffet

buffet = Buffet.from_default_config()
reply = buffet.ask("Summarize the plot of Hamlet in 20 words.")
print(reply.text)
print(f"served by {reply.provider_id}/{reply.model}")
```

## How routing works

For each request `llmbuffet` builds the list of `(provider, model)` candidates you have keys for, orders them **least-used-today first** (providers already over their free daily hint sink to the bottom), then tries them in order until one returns a non-empty completion. Every success is recorded to a small per-day counter at `~/.config/llmbuffet/quota.json` (reset at UTC midnight). See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full picture.

## Adding or overriding providers

The built-in catalog lives in [`src/llmbuffet/providers.toml`](src/llmbuffet/providers.toml). To add a provider or override a model list without forking, drop a `providers.toml` at `~/.config/llmbuffet/providers.toml` (or point `LLMBUFFET_CONFIG` at one). Same-`id` entries override the built-ins; new ids are appended. See [CONTRIBUTING.md](CONTRIBUTING.md) for the (small) anatomy of a provider.

## Comparison

| | llmbuffet | Calling each SDK by hand | A paid gateway |
|---|---|---|---|
| Free tiers pooled | ✅ 9 providers | ⚠️ you wire each one | ❌ |
| Automatic failover | ✅ | ❌ | ✅ |
| Quota tracking | ✅ per-day | ❌ | varies |
| Drop-in OpenAI proxy | ✅ | ❌ | ✅ |
| Cost | $0 | $0 | 💸 |
| Dependencies | 1 (`httpx`) | many | a service |

## Status

`llmbuffet` is `0.1` and moving fast. Provider endpoints and free-tier limits drift — if something breaks, please [open an issue](https://github.com/0xzr/llmbuffet/issues) or send a one-line PR to `providers.toml`. Contributions of new free providers are especially welcome.

## Found this useful?

⭐ **Star the repo** — it's the single biggest thing that helps others discover llmbuffet, and it keeps the free-provider catalog maintained. New free providers and one-line limit fixes are always welcome ([CONTRIBUTING.md](CONTRIBUTING.md)).

## License

MIT — see [LICENSE](LICENSE).

