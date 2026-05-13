from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Transform:
    position: pygame.Vector2
