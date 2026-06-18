# Reddit / open-source communities draft

## Title options

- freellmpool: an MIT-licensed local gateway for pooling free LLM API tiers
- I built a free/open-source LLM gateway that starts without API keys
- Open-source local proxy over free LLM provider tiers, with failover and MCP

## Body

I released `freellmpool`, a small MIT-licensed Python project that pools free
LLM provider tiers behind one local API.

GitHub: https://github.com/0xzr/freellmpool

It is meant for developers who want free-tier inference capacity for scripts,
coding agents, docs, triage, and side tasks without wiring every provider
separately.

Features:

- CLI: `freellmpool ask`, `tokenmax`, `providers`, `capacity status`, `stats`
- Python library
- local OpenAI-compatible proxy
- experimental Anthropic-compatible proxy path
- MCP server
- OpenAI-compatible speech-to-text endpoint
- provider failover and local quota tracking
- keyless start when default keyless routes are available; optional free-tier
  keys unlock more models and capacity

The current packaged catalog has 19 cataloged providers, 235 enabled chat routes, and 355
cataloged chat models.

The project is intentionally honest about limitations:

- prompts go to the selected upstream provider;
- it respects provider rate limits and does not try to evade them;
- free-tier model quality varies;
- catalog maintenance matters because free routes change.

The repo now has scoped good-first issues for docs, CLI JSON output, catalog
status docs, capacity fixtures, and agent recipe tests:

https://github.com/0xzr/freellmpool/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22

Feedback and small provider-catalog fixes would be useful.
