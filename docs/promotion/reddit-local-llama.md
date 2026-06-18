# Reddit / r/LocalLLaMA draft

## Title options

- I built a local router that pools free LLM API tiers behind one OpenAI-compatible endpoint
- freellmpool: one local proxy over Groq, Cerebras, Gemini, Mistral, OpenRouter, NVIDIA, and other free tiers
- Pool free hosted LLM tiers for coding agents and scripts with one local proxy

## Body

I built `freellmpool`, an MIT-licensed Python tool for pooling legitimate free
LLM API tiers behind one local interface.

Repo: https://github.com/0xzr/freellmpool

Why I wanted this:

- every provider has a different key, SDK, model list, rate limit, and failure
  mode;
- several free tiers are useful but individually small;
- coding agents and scripts usually just want one OpenAI-compatible base URL;
- free provider catalogs drift constantly.

What it does:

- `freellmpool ask "..."` for one-shot CLI calls;
- local OpenAI-compatible proxy for existing clients;
- experimental Anthropic-compatible proxy path for coding agents;
- MCP server for Claude Desktop/Code/Cursor;
- provider failover on 429s, timeouts, server errors, empty replies, and stale
  routes;
- local quota tracking so traffic can be spread across free tiers;
- `tokenmax` mode that fans out to many available models and synthesizes a
  result.

Current catalog:

- 19 providers
- 235 enabled chat routes
- 355 cataloged chat models
- no API key required to start, more capacity when you add your own free keys

Example:

```bash
pip install freellmpool
freellmpool ask "Explain KV cache in one paragraph."

freellmpool proxy
export OPENAI_BASE_URL=http://localhost:8080/v1
export OPENAI_API_KEY=anything
```

It is not a privacy layer. Prompts go to the selected upstream provider. I wrote
the FAQ to make that explicit:

https://github.com/0xzr/freellmpool/blob/main/FAQ.md

I would like feedback from this community on provider quality, missing free-tier
providers, and whether the routing behavior matches how people actually use
hosted free models alongside local models.

