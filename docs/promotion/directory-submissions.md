# Directory submission checklist

Some directories still need browser/account actions. This file keeps the exact
copy and status in one place for promotion work.

## Already done

- GitHub About description updated.
- GitHub topics updated.
- Good-first issues filed and refreshed.
- Official MCP Registry published.
- MCP.so submission comment posted.

## Manual GitHub UI

- Social preview upload:
  - Use `assets/social-preview.png`.
  - Open <https://github.com/0xzr/freellmpool/settings>.
  - Social preview -> Edit -> Upload an image.
- Profile pin:
  - Already reported done by operator.

## Glama

Submit: <https://glama.ai/mcp/servers>

Repository:

```text
https://github.com/0xzr/freellmpool
```

Short description:

```text
Local stdio MCP server for pooling free LLM provider tiers. Includes one-shot asks, multi-model panels, tokenmax fan-out, routing previews, model listing, quota status, and lifetime stats.
```

Paste more detail from:

```text
docs/mcp-listings/glama-submission.md
```

## PulseMCP

Submit: <https://www.pulsemcp.com/>

Repository:

```text
https://github.com/0xzr/freellmpool
```

Server manifest:

```text
https://github.com/0xzr/freellmpool/blob/main/server.json
```

Paste more detail from:

```text
docs/mcp-listings/pulsemcp-submission.md
```

## Smithery

Smithery's URL flow is for Streamable HTTP servers. `freellmpool` currently
ships a local stdio MCP server, so Smithery needs an MCPB bundle or an HTTP
wrapper before the listing is clean.

Use:

```text
docs/mcp-listings/smithery.md
```

## Optional directories after launch

- AlternativeTo, if it accepts developer tools.
- Product Hunt, only if a polished landing screenshot and demo are ready.
- Awesome MCP server lists, using the official registry listing as proof.
- Python/package newsletters, after PyPI release notes are stable.

