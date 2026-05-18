from __future__ import annotations

import json
from pathlib import Path


class HighScoreSystem:
    def __init__(self, config_path: Path) -> None:
        self._path = config_path / "highscore.json"
        self._data: dict = self._load()

    def _load(self) -> dict:
        with open(self._path, encoding="utf-8") as f:
            return json.load(f)

    def save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    @property
    def scores(self) -> list[dict]:
        return self._data["scores"]

    @property
    def max_entries(self) -> int:
        return self._data.get("max_entries", 5)

    def qualifies(self, score: int) -> bool:
        if len(self.scores) < self.max_entries:
            return score > 0
        return score > self.scores[-1]["score"]

    def insert(self, name: str, score: int) -> int:
        entry = {"name": name[:3].upper(), "score": score}
        self.scores.append(entry)
        self.scores.sort(key=lambda e: e["score"], reverse=True)
        del self.scores[self.max_entries:]
        self.save()
        return next(i for i, e in enumerate(self.scores) if e is entry or (e["name"] == entry["name"] and e["score"] == entry["score"]))
