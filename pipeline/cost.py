"""Token and dollar accounting per stage, written to cost.json in the run folder."""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from . import config


@dataclass
class StageUsage:
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_5m_tokens: int = 0
    cache_write_1h_tokens: int = 0
    usd: float = 0.0


@dataclass
class CostTracker:
    stages: dict[str, StageUsage] = field(default_factory=dict)

    def record(self, stage: str, usage: Any, model: str, batch: bool = False) -> StageUsage:
        """Add one response's `usage` to a stage and return that call's own usage."""
        price = config.models()["pricing"][model]
        cc = getattr(usage, "cache_creation", None)
        if cc is not None:
            w5 = cc.ephemeral_5m_input_tokens or 0
            w1h = cc.ephemeral_1h_input_tokens or 0
        else:  # no per-TTL breakdown: attribute the total to the configured TTL
            total_w = usage.cache_creation_input_tokens or 0
            w1h, w5 = (total_w, 0) if config.models()["caching"]["ttl"] == "1h" else (0, total_w)
        call = StageUsage(
            calls=1,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cache_read_tokens=usage.cache_read_input_tokens or 0,
            cache_write_5m_tokens=w5,
            cache_write_1h_tokens=w1h,
        )
        usd = (
            call.input_tokens * price["input"]
            + call.output_tokens * price["output"]
            + call.cache_read_tokens * price["cache_read"]
            + call.cache_write_5m_tokens * price["cache_write_5m"]
            + call.cache_write_1h_tokens * price["cache_write_1h"]
        ) / 1_000_000
        if batch:
            usd *= price["batch_discount"]
        call.usd = round(usd, 6)

        s = self.stages.setdefault(stage, StageUsage())
        for k, v in asdict(call).items():
            setattr(s, k, getattr(s, k) + v)
        s.usd = round(s.usd, 6)
        return call

    @property
    def total_usd(self) -> float:
        return round(sum(s.usd for s in self.stages.values()), 4)

    def write(self, path: Path) -> None:
        data = {"total_usd": self.total_usd, "stages": {k: asdict(v) for k, v in self.stages.items()}}
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
