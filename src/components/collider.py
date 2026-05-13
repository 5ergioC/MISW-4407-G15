from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Collider:
    size: pygame.Vector2
    offset: pygame.Vector2
