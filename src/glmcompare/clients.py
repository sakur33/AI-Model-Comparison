"""Thin model clients that return normalised text + token usage."""
from __future__ import annotations

import inspect
import time
from dataclasses import dataclass

from .config import ModelConfig


@dataclass
class Completion:
    text: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    latency_s: float
    stop_reason: str | None = None


class AnthropicClient:
    def __init__(self, cfg: ModelConfig):
        import anthropic

        self.cfg = cfg
        self.client = anthropic.Anthropic(api_key=cfg.api_key())

    def complete(self, system: str, user: str, problem=None) -> Completion:
        t0 = time.perf_counter()
        resp = self.client.messages.create(
            model=self.cfg.model,
            system=system,
            messages=[{"role": "user", "content": user}],
            **self.cfg.params,
        )
        latency = time.perf_counter() - t0
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        u = resp.usage
        return Completion(
            text=text,
            input_tokens=u.input_tokens or 0,
            output_tokens=u.output_tokens or 0,
            cache_read_tokens=getattr(u, "cache_read_input_tokens", 0) or 0,
            latency_s=latency,
            stop_reason=resp.stop_reason,
        )


class OpenAICompatibleClient:
    """For CompactifAI (OpenAI-compatible chat completions endpoint)."""

    def __init__(self, cfg: ModelConfig):
        import openai

        base_url = cfg.resolved_base_url()
        if not base_url:
            raise RuntimeError(
                f"No base URL for '{cfg.key}'. Set {cfg.base_url_env} or base_url in the config."
            )
        self.cfg = cfg
        self.client = openai.OpenAI(api_key=cfg.api_key(), base_url=base_url)

    def complete(self, system: str, user: str, problem=None) -> Completion:
        t0 = time.perf_counter()
        # Streamed so the provider's request deadline is met by the first tokens.
        stream = self.client.chat.completions.create(
            model=self.cfg.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            stream=True,
            stream_options={"include_usage": True},
            **self.cfg.params,
        )
        parts: list[str] = []
        finish = None
        u = None
        for chunk in stream:
            if chunk.usage:
                u = chunk.usage
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            if choice.delta and choice.delta.content:
                parts.append(choice.delta.content)
            if choice.finish_reason:
                finish = choice.finish_reason
        latency = time.perf_counter() - t0
        if u is None:
            raise RuntimeError("stream ended without usage information")
        details = getattr(u, "prompt_tokens_details", None)
        cached = (getattr(details, "cached_tokens", 0) or 0) if details else 0
        return Completion(
            text="".join(parts),
            input_tokens=max((u.prompt_tokens or 0) - cached, 0),
            output_tokens=u.completion_tokens or 0,
            cache_read_tokens=cached,
            latency_s=latency,
            stop_reason=finish,
        )


class MockClient:
    """Answers with the problem's reference solution (offline pipeline test)."""

    def __init__(self, cfg: ModelConfig):
        self.cfg = cfg

    def complete(self, system: str, user: str, problem=None) -> Completion:
        code = inspect.getsource(problem.reference)
        text = f"```python\n{code}\n```"
        return Completion(
            text=text,
            input_tokens=(len(system) + len(user)) // 4,
            output_tokens=len(text) // 4,
            cache_read_tokens=0,
            latency_s=0.001,
            stop_reason="end_turn",
        )


def make_client(cfg: ModelConfig):
    if cfg.provider == "anthropic":
        return AnthropicClient(cfg)
    if cfg.provider == "openai_compatible":
        return OpenAICompatibleClient(cfg)
    if cfg.provider == "mock":
        return MockClient(cfg)
    raise ValueError(f"Unknown provider '{cfg.provider}' for model '{cfg.key}'")
