"""Token cost computation."""
from __future__ import annotations

from .config import Pricing


def cost_usd(
    input_tokens: int,
    output_tokens: int,
    pricing: Pricing,
    cache_read_tokens: int = 0,
) -> float | None:
    """Cost of one call in USD, or None if prices are not configured.

    `input_tokens` is the *uncached* input; cache reads are billed separately
    (at cache_read_per_mtok if set, otherwise at the normal input price).
    """
    if pricing.input_per_mtok is None or pricing.output_per_mtok is None:
        return None
    cache_price = (
        pricing.cache_read_per_mtok
        if pricing.cache_read_per_mtok is not None
        else pricing.input_per_mtok
    )
    return (
        input_tokens * pricing.input_per_mtok
        + cache_read_tokens * cache_price
        + output_tokens * pricing.output_per_mtok
    ) / 1_000_000
