from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Wraparound:
    world_width: float
    world_height: float | None = None
    margin: float = 0.0
    horizontal: bool = True
    vertical: bool = False
