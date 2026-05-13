from __future__ import annotations

from dataclasses import dataclass, field

import pygame


@dataclass
class Renderable:
    shape: str
    size: pygame.Vector2
    color: pygame.Color
    layer: int = 0
    visible: bool = True
    text: str = ""
    points: list[tuple[float, float]] = field(default_factory=list)
