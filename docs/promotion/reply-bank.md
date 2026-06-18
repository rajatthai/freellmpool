# Reply bank

Use these as starting points for HN, Reddit, GitHub Discussions, and social
comments.

## Where do prompts go?

Prompts go directly to the selected upstream provider/model. `freellmpool` is a
local router, not a hosted relay and not a privacy layer. The FAQ has a
provider-by-provider table:

https://github.com/0xzr/freellmpool/blob/main/FAQ.md

## Is this evading rate limits?

No. The tool is meant to use legitimate provider free tiers. It tracks local
usage and fails over when a provider is rate-limited, unavailable, or returning
bad responses. It does not bypass provider policies.

## Why not just use OpenRouter?

OpenRouter is a hosted aggregator and is very polished. `freellmpool` is local,
open source, pip-installable, starts without a key, and can use provider free
tiers directly through a CLI, library, proxy, and MCP server. It can also use
OpenRouter as one provider.

## Why not LiteLLM?

LiteLLM is the mature bring-your-own-keys proxy/SDK. `freellmpool` is narrower:
it focuses on pooling legitimate free tiers, first-run keyless usage, a simple
CLI, and the free-tier catalog.

## Why not FreeLLMAPI?

FreeLLMAPI predates this project. The overlap is independent convergence:
free-tier pooling is a useful idea. `freellmpool` focuses on pip-installable
local usage, a one-shot CLI, MCP tools, and keyless start when default routes
are available.

## Is it really free?

The software is MIT-licensed. Provider free tiers are provider-owned and can
change. Some need accounts or keys; several default routes can start without a
key. Add your own free-tier keys for more capacity.

## Can this replace paid frontier models?

No. It is useful for drafting, classification, docs, everyday coding support,
triage, and side tasks. Hard reasoning still benefits from frontier models.

## Does it support coding agents?

Yes, through the local proxy. It speaks the OpenAI API and has an experimental
Anthropic-compatible path. There are recipes for Codex, Claude Code, aider,
Cline, Continue, Cursor, and OpenCode.

## What should contributors help with?

Provider drift reports are the most valuable. Free model ids and limits change
often. The repo also has scoped good-first issues:

https://github.com/0xzr/freellmpool/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22

## What should I not send through it?

Do not send secrets or confidential data unless you are comfortable with the
selected provider's current terms, privacy posture, and retention behavior.
Anonymous keyless routes are convenient, not private.

## Why is OpenCode Zen cataloged but disabled by default?

Some routes are useful to track but not reliable or reviewed enough for default
routing. OpenCode Zen is cataloged as a keyless OpenAI-compatible endpoint, but
its free routes ship disabled by default pending explicit opt-in and provider
policy review.
