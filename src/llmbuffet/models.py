"""Core data types: Provider, Model, Reply."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Model:
    """A single model offered by a provider."""

    name: str
    rpd: int = 0  # free-tier requests-per-day hint; 0 = unknown/unmetered

    @property
    def key(self) -> str:
        """Unused-namespace-safe identifier, filled in by Provider."""
        return self.name


@dataclass(frozen=True)
class Provider:
    """A free-tier LLM endpoint and the models it serves."""

    id: str
    label: str
    adapter: str  # "openai" | "gemini" | "cloudflare"
    base_url: str
    key_env: str
    models: tuple[Model, ...]
    extra_env: tuple[str, ...] = field(default_factory=tuple)

    def is_configured(self, env: dict[str, str] | None = None) -> bool:
        """True if the API key and any extra required env vars are present."""
        env = env if env is not None else dict(os.environ)
        if not env.get(self.key_env):
            return False
        return all(env.get(name) for name in self.extra_env)

    def api_key(self, env: dict[str, str] | None = None) -> str | None:
        env = env if env is not None else dict(os.environ)
        return env.get(self.key_env) or None

    def model(self, name: str) -> Model | None:
        for m in self.models:
            if m.name == name:
                return m
        return None


@dataclass
class Reply:
    """A normalized successful completion from some provider."""

    text: str
    provider_id: str
    model: str
    raw: dict
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    def __str__(self) -> str:  # pragma: no cover - convenience
        return self.text
