from __future__ import annotations

import json
from pathlib import Path


class ConfigService:
    def __init__(self, root_path: Path) -> None:
        self._config_path = root_path / "config"
        self._cache: dict[str, dict] = {}

    def get(self, name: str) -> dict:
        if name not in self._cache:
            with open(self._config_path / f"{name}.json", encoding="utf-8") as handle:
                self._cache[name] = json.load(handle)
        return self._cache[name]
