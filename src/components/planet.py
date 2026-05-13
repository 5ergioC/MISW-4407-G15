from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Planet:
    points: list[tuple[float, float]] = field(default_factory=list)
    parallax: float = 0.75
    color: tuple[int, int, int] = (60, 210, 150)
