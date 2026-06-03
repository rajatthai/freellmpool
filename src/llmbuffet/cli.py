"""Command-line interface for llmbuffet.

llmbuffet ask "question"        one-shot completion (reads stdin too)
llmbuffet providers            list configured / available providers
llmbuffet quota                show today's per-provider usage
llmbuffet proxy                run the OpenAI-compatible proxy server
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .config import configured_providers, load_catalog
from .errors import AllProvidersExhausted, NoProvidersConfigured
from .quota import QuotaStore
from .router import Buffet


def _read_stdin() -> str:
    if sys.stdin is None or sys.stdin.isatty():
        return ""
    return sys.stdin.read()


def cmd_ask(args: argparse.Namespace) -> int:
    stdin = _read_stdin()
    prompt = args.prompt or ""
    if stdin:
        prompt = f"{stdin}\n\n{prompt}".strip() if prompt else stdin

    if not prompt.strip():
        print("llmbuffet: no prompt provided (pass text or pipe stdin)", file=sys.stderr)
        return 3

    buffet = Buffet.from_default_config()
    try:
        reply = buffet.ask(
            prompt,
            system=args.system,
            model=args.model,
            providers=args.providers.split(",") if args.providers else None,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
    except NoProvidersConfigured as exc:
        print(f"llmbuffet: {exc}", file=sys.stderr)
        return 3
    except AllProvidersExhausted as exc:
        print(f"llmbuffet: {exc}", file=sys.stderr)
        return 4

    print(reply.text)
    if args.verbose:
        print(f"\n[served by {reply.provider_id}/{reply.model}]", file=sys.stderr)
    return 0


def cmd_providers(args: argparse.Namespace) -> int:
    catalog = load_catalog()
    configured = {p.id for p in configured_providers(catalog)}
    n_models = sum(len(p.models) for p in catalog)
    print(f"llmbuffet catalog: {len(catalog)} providers, {n_models} models\n")
    for p in catalog:
        mark = "✓" if p.id in configured else "·"
        status = "configured" if p.id in configured else f"set {p.key_env}"
        print(f"  {mark} {p.id:<12} {p.label:<28} {len(p.models):>2} models   [{status}]")
    if not configured:
        print("\nNo providers configured yet. See .env.example for the env vars to set.")
    return 0


def cmd_quota(args: argparse.Namespace) -> int:
    store = QuotaStore()
    snap = store.snapshot()
    if not snap:
        print("No usage recorded today (UTC).")
        return 0
    print("Today's usage (UTC):")
    for key, count in sorted(snap.items(), key=lambda kv: -kv[1]):
        print(f"  {count:>6}  {key}")
    return 0


def cmd_proxy(args: argparse.Namespace) -> int:
    from .proxy import serve  # lazy: avoids http.server import on other paths

    buffet = Buffet.from_default_config()
    if not buffet.providers:
        print(
            "llmbuffet: no providers configured; set at least one API key "
            "(see .env.example) before starting the proxy.",
            file=sys.stderr,
        )
        return 3

    httpd = serve(buffet, host=args.host, port=args.port)
    n_models = sum(len(p.models) for p in buffet.providers)
    print(
        f"llmbuffet proxy on http://{args.host}:{args.port}/v1  "
        f"({len(buffet.providers)} providers, {n_models} models)\n"
        f"  point your OpenAI client at:  OPENAI_BASE_URL=http://{args.host}:{args.port}/v1\n"
        "  press Ctrl-C to stop",
        file=sys.stderr,
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nllmbuffet: shutting down", file=sys.stderr)
    finally:
        httpd.server_close()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llmbuffet",
        description="Pool free-tier LLM APIs behind one OpenAI-compatible endpoint.",
    )
    parser.add_argument("--version", action="version", version=f"llmbuffet {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ask = sub.add_parser("ask", help="one-shot completion")
    p_ask.add_argument("prompt", nargs="?", default="", help="prompt text (stdin is appended)")
    p_ask.add_argument("-s", "--system", help="system prompt")
    p_ask.add_argument("-m", "--model", help="restrict to a specific model name")
    p_ask.add_argument("-p", "--providers", help="comma-separated provider ids to allow")
    p_ask.add_argument("--max-tokens", type=int, default=1024)
    p_ask.add_argument("--temperature", type=float, default=0.0)
    p_ask.add_argument("-v", "--verbose", action="store_true", help="report which provider served")
    p_ask.set_defaults(func=cmd_ask)

    p_prov = sub.add_parser("providers", help="list providers and configuration status")
    p_prov.set_defaults(func=cmd_providers)

    p_quota = sub.add_parser("quota", help="show today's per-provider usage")
    p_quota.set_defaults(func=cmd_quota)

    p_proxy = sub.add_parser("proxy", help="run the OpenAI-compatible proxy server")
    p_proxy.add_argument("--host", default="127.0.0.1")
    p_proxy.add_argument("--port", type=int, default=8080)
    p_proxy.set_defaults(func=cmd_proxy)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
