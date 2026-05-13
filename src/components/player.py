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
    max_speed_x: float
    max_speed_y: float
    vertical_min: float
    vertical_max: float
    facing: float = 1.0
