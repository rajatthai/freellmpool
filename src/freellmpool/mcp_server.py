"""A tiny Model Context Protocol (MCP) server, zero extra dependencies.

`freellmpool mcp` speaks MCP over stdio (newline-delimited JSON-RPC 2.0), so an
MCP client — Claude Desktop, Claude Code, Cursor, etc. — can offload subtasks to
free LLMs:

    {
      "mcpServers": {
        "freellmpool": { "command": "freellmpool", "args": ["mcp"] }
      }
    }

Tools exposed:
    free_llm_ask     ask a free model a question (prompt + optional system/model/provider)
    free_llm_models  list available provider/model ids

Implemented on the standard library only — no MCP SDK required.
"""

from __future__ import annotations

import json
import sys

from .config import resolve_alias
from .router import Pool

_DEFAULT_PROTOCOL = "2025-06-18"

TOOLS = [
    {
        "name": "free_llm_ask",
        "description": (
            "Ask a free LLM (pooled across 16 free providers, with failover). "
            "Use this to offload a self-contained subtask — drafting, summarizing, "
            "classifying, brainstorming, or a quick lookup — to a free model."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The question or task."},
                "system": {"type": "string", "description": "Optional system instruction."},
                "model": {
                    "type": "string",
                    "description": "Optional model name or provider/model (e.g. groq/llama-3.3-70b-versatile). Default: auto.",
                },
                "provider": {
                    "type": "string",
                    "description": "Optional provider id to restrict to (e.g. groq, cerebras).",
                },
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "free_llm_models",
        "description": "List the available free provider/model ids freellmpool can route to.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def _result(mid, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def _error(mid, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}


def _text(text: str, is_error: bool = False) -> dict:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def _call_tool(pool: Pool, params: dict) -> dict:
    name = params.get("name")
    args = params.get("arguments") or {}
    if name == "free_llm_ask":
        prompt = args.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            return _text("'prompt' is required", is_error=True)
        provider = args.get("provider")
        providers = [provider] if provider else None
        model = args.get("model")
        if isinstance(model, str) and model:
            model = resolve_alias(model, pool.env)
            if model == "auto":
                model = None
            elif "/" in model:
                p, _, m = model.partition("/")
                providers, model = [p], m
        else:
            model = None
        try:
            reply = pool.ask(prompt, system=args.get("system"), model=model, providers=providers)
        except Exception as exc:  # noqa: BLE001 — surface as a tool error
            return _text(f"{type(exc).__name__}: {exc}", is_error=True)
        return _text(reply.text)
    if name == "free_llm_models":
        ids = [f"{p.id}/{m.name}" for p in pool.providers for m in p.models]
        return _text("\n".join(ids) or "no providers configured")
    return _text(f"unknown tool: {name}", is_error=True)


def handle_message(pool: Pool, msg: dict, *, version: str = "0.0.0") -> dict | None:
    """Handle one JSON-RPC message. Returns a response dict, or None for
    notifications (which get no reply)."""
    if not isinstance(msg, dict) or "method" not in msg:
        return None
    method = msg["method"]
    if "id" not in msg:  # notification (e.g. notifications/initialized)
        return None
    mid = msg["id"]
    try:
        if method == "initialize":
            params = msg.get("params") or {}
            protocol = params.get("protocolVersion") or _DEFAULT_PROTOCOL
            return _result(
                mid,
                {
                    "protocolVersion": protocol,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "freellmpool", "version": version},
                },
            )
        if method == "ping":
            return _result(mid, {})
        if method == "tools/list":
            return _result(mid, {"tools": TOOLS})
        if method == "tools/call":
            return _result(mid, _call_tool(pool, msg.get("params") or {}))
        return _error(mid, -32601, f"method not found: {method}")
    except Exception as exc:  # noqa: BLE001 — never crash the loop
        return _error(mid, -32603, f"{type(exc).__name__}: {exc}")


def serve_stdio(pool: Pool, version: str = "0.0.0") -> None:
    """Run the MCP server over stdio until stdin closes."""
    out = sys.stdout
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        response = handle_message(pool, msg, version=version)
        if response is not None:
            out.write(json.dumps(response) + "\n")
            out.flush()
