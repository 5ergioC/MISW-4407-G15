from __future__ import annotations

import pygame

from src.core.service_locator import ServiceLocator


class BackgroundSystem:
    def __init__(self) -> None:
        self.world_cfg = ServiceLocator.config.get("world")

    def update(self, world, dt: float) -> None:
        del dt
        del world

    def render(self, surface: pygame.Surface) -> None:
        width = self.world_cfg["width"]
        height = self.world_cfg["height"]
        planet_height = self.world_cfg["planet_height"]
        ground_rect = pygame.Rect(0, height - planet_height, width, planet_height)
        pygame.draw.rect(surface, pygame.Color(18, 28, 42), ground_rect)
        step = 12
        for x in range(0, width + step, step):
            y = ground_rect.top + ((x // step) % 3) * 2
            pygame.draw.line(
                surface,
                pygame.Color(60, 210, 150),
                (x, y),
                (min(width, x + step), y + 2),
                1,
            )
