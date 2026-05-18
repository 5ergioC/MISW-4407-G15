from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Projectile:
    owner: str
    direction: pygame.Vector2
    speed: float
    damage: int
    kind: str = "bullet"
    source_kind: str = ""
