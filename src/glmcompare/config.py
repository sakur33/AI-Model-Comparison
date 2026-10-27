"""Load model configuration (models.yaml)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "config" / "models.yaml"
DEFAULT_RESULTS = REPO_ROOT / "results"


@dataclass
class Pricing:
    input_per_mtok: float | None = None
    output_per_mtok: float | None = None
    cache_read_per_mtok: float | None = None


@dataclass
class ModelConfig:
    key: str
    label: str
    provider: str
    model: str
    api_key_env: str | None = None
    base_url_env: str | None = None
    base_url: str | None = None
    params: dict = field(default_factory=dict)
    pricing: Pricing = field(default_factory=Pricing)

    def api_key(self) -> str | None:
        return os.environ.get(self.api_key_env) if self.api_key_env else None

    def resolved_base_url(self) -> str | None:
        if self.base_url_env and os.environ.get(self.base_url_env):
            return os.environ[self.base_url_env]
        return self.base_url


def load_models(path: str | Path | None = None) -> dict[str, ModelConfig]:
    path = Path(path or os.environ.get("GLMCOMPARE_CONFIG") or DEFAULT_CONFIG)
    data = yaml.safe_load(path.read_text())
    models: dict[str, ModelConfig] = {}
    for key, raw in (data.get("models") or {}).items():
        raw = dict(raw)
        pricing = Pricing(**(raw.pop("pricing", None) or {}))
        models[key] = ModelConfig(
            key=key,
            label=raw.pop("label", key),
            pricing=pricing,
            params=raw.pop("params", None) or {},
            **raw,
        )
    return models
