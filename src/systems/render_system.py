from __future__ import annotations

import pygame

from src.components.renderable import Renderable
from src.components.transform import Transform


class RenderSystem:
    def render(self, world, surface: pygame.Surface) -> None:
        render_queue: list[tuple[int, Transform, Renderable]] = []
        for _, (transform, renderable) in world.get_components(Transform, Renderable):
            render_queue.append((renderable.layer, transform, renderable))
        for _, transform, renderable in sorted(render_queue, key=lambda item: item[0]):
            if not renderable.visible:
                continue
            if renderable.shape == "rect":
                rect = pygame.Rect(
                    round(transform.position.x),
                    round(transform.position.y),
                    round(renderable.size.x),
                    round(renderable.size.y),
                )
                pygame.draw.rect(surface, renderable.color, rect)
            elif renderable.shape == "triangle":
                points = [
                    (transform.position.x + point[0], transform.position.y + point[1])
                    for point in renderable.points
                ]
                pygame.draw.polygon(surface, renderable.color, points)
