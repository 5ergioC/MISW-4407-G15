from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Player:
    thrust_input: pygame.Vector2
    thrust: float
    drag: float
    max_speed: float
    lives: int
    facing: float = 1.0
