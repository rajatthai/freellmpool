# Pooling free LLM tiers behind one local API

Every hosted LLM provider has a different shape. One has a generous free tier
but a tiny daily cap. Another is fast but only exposes a few useful models.
Another has a good model list but different failure modes. Some are
OpenAI-compatible; some are close enough; some need custom handling.

The annoying part is not making one API call. The annoying part is making all of
them useful together.

That is what `freellmpool` is for:

https://github.com/0xzr/freellmpool

`freellmpool` is a local, MIT-licensed Python tool that pools legitimate free LLM
provider tiers behind one interface. It can run as a CLI, a Python library, a
local OpenAI-compatible proxy, an experimental Anthropic-compatible proxy path,
or an MCP server.

The current packaged catalog has 19 cataloged providers, 235 enabled chat routes, and 355
cataloged chat models. It can produce a first reply without any API keys, and
users can add their own free-tier provider keys for more capacity.

## Why this exists

Free LLM tiers are useful, but they are fragmented.

For a one-off script, fragmentation is just friction. For a coding agent or local
tool, it becomes operational noise:

- every provider needs different environment variables;
- model ids drift;
- daily limits differ;
- some providers rate-limit quickly;
- failures are inconsistent;
- switching providers usually means editing client config.

The idea behind `freellmpool` is simple: keep the user-facing interface stable
and let the router deal with provider churn.

## What it does

The CLI path is the simplest:

```bash
pip install freellmpool
freellmpool ask "Explain semantic versioning in one paragraph."
```

For existing tools, the local proxy is usually more useful:

```bash
freellmpool proxy
export OPENAI_BASE_URL=http://localhost:8080/v1
export OPENAI_API_KEY=anything
```

For MCP clients, it can run over stdio:

```bash
freellmpool mcp
```

The tool surface includes one-shot asks, multi-model panels, `tokenmax` fan-out,
routing previews, model listing, quota status, and lifetime stats.

## Failover matters more than the model list

The model catalog is large, but the important behavior is failover.

Free tiers are shared capacity. Some routes will return 429. Some will be slow.
Some model ids will disappear. Some providers will return empty replies under
load. A useful free-tier pool needs to treat those as expected operating
conditions, not exceptional surprises.

`freellmpool` can move to another eligible provider when a route fails, and it
tracks local per-day usage so traffic can be spread across tiers.

## What this is not

It is not a privacy layer. Prompts go to the selected upstream provider.

It is not an attempt to evade provider limits. The point is to use legitimate
free tiers carefully, fail over when they are unavailable, and make the
fragmentation less painful.

It is not a frontier-model replacement. Free-tier models are useful for many
developer tasks, but hard reasoning still benefits from stronger paid models.

## Where it fits

I have found it most useful for:

- docs and README drafting;
- commit messages and PR summaries;
- lightweight coding-agent side tasks;
- classification and triage;
- "second opinion" panels across several smaller models;
- MCP tool calls where a free model is good enough.

It also gives contributors a concrete surface for small improvements: provider
catalog fixes, docs, CLI output modes, and tests for capacity behavior.

## Links

- GitHub: https://github.com/0xzr/freellmpool
- Docs: https://0xzr.github.io/freellmpool/
- FAQ: https://github.com/0xzr/freellmpool/blob/main/FAQ.md
- MCP docs: https://github.com/0xzr/freellmpool/blob/main/docs/MCP.md
- Good first issues: https://github.com/0xzr/freellmpool/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22

