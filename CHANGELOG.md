# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and the project aims to follow
[Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-06-02

Initial release.

### Added
- Provider catalog (`providers.toml`) covering 9 free-tier providers and 24
  models: Groq, Cerebras, OpenRouter, Google Gemini, GitHub Models, Cloudflare
  Workers AI, Mistral, Cohere, SambaNova.
- Quota-aware, least-used-first router with automatic failover across providers.
- Persistent per-provider/day quota tracking (`~/.config/llmbuffet/quota.json`,
  resets at UTC midnight).
- OpenAI-compatible proxy server (`llmbuffet proxy`) exposing
  `/v1/chat/completions` and `/v1/models` — a drop-in `OPENAI_BASE_URL`.
- CLI: `ask`, `providers`, `quota`, `proxy`.
- Python API: `from llmbuffet import Buffet`.
- Three request/response adapters (openai, gemini, cloudflare) and per-user
  catalog overrides via `~/.config/llmbuffet/providers.toml`.
- Full unit-test suite with a faked transport (no network) and CI on Python
  3.11–3.13.
