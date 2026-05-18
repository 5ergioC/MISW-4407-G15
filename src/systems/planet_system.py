from __future__ import annotations

import pygame

from src.components.camera import Camera
from src.components.planet import Planet
from src.engine.service_locator import ServiceLocator


class PlanetSystem:
    def __init__(self) -> None:
        self.world_cfg = ServiceLocator.config.get("world")
        color_cfg = self.world_cfg["planet"].get("color", {"r": 205, "g": 106, "b": 42})
        self.color = pygame.Color(color_cfg["r"], color_cfg["g"], color_cfg["b"])
        self._points: list[tuple[float, float]] = []

    def update(self, world, dt: float) -> None:
        del dt
        for _, (planet,) in world.get_components(Planet):
            self._points = planet.points
            break

    @property
    def points(self) -> list[tuple[float, float]]:
        return self._points

    def render(self, world, surface: pygame.Surface, camera: Camera) -> None:
        for _, (planet,) in world.get_components(Planet):
            if len(planet.points) < 2:
                return
            repeated_points: list[tuple[float, float]] = []
            for world_offset in (-camera.world_width, 0.0, camera.world_width):
                for world_x, world_y in planet.points:
                    repeated_points.append((world_x + world_offset - camera.x * planet.parallax, world_y - camera.y))
            for index in range(1, len(repeated_points)):
                previous = repeated_points[index - 1]
                current = repeated_points[index]
                if self._segment_visible(previous[0], current[0], camera.width):
                    pygame.draw.line(surface, self.color, previous, current, 1)
            break

    def _segment_visible(self, x1: float, x2: float, screen_width: float) -> bool:
        return max(x1, x2) >= -16 and min(x1, x2) <= screen_width + 16
