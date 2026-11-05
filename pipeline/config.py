"""Loads config/*.yaml. Model IDs, effort levels and budgets live there, never in code."""

from functools import cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"


@cache
def load(name: str) -> dict[str, Any]:
    with open(CONFIG_DIR / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def models() -> dict[str, Any]:
    return load("models")


def task(name: str) -> dict[str, Any]:
    """Routing for one AI task: {mode, effort}."""
    tasks = models()["tasks"]
    if name not in tasks:
        raise KeyError(f"task {name!r} missing from config/models.yaml")
    return tasks[name]
