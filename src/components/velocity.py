from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Velocity:
    value: pygame.Vector2
