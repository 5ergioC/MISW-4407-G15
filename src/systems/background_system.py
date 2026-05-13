from __future__ import annotations

import pygame

from src.engine.service_locator import ServiceLocator


class BackgroundSystem:
    def __init__(self) -> None:
        self.world_cfg = ServiceLocator.config.get("world")

    def update(self, world, dt: float) -> None:
        del dt
        del world

    def render(self, surface: pygame.Surface) -> None:
        del surface
        # Background color is filled by the engine. Stars and planet are ECS/system rendered.
