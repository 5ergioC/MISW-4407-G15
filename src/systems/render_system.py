from __future__ import annotations

import pygame

from src.components.camera import Camera
from src.components.parallax import Parallax
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.engine.service_locator import ServiceLocator


class RenderSystem:
    def render(self, world, surface: pygame.Surface, camera: Camera) -> None:
        render_queue: list[tuple[int, int, Transform, Renderable, float]] = []
        for entity, (transform, renderable) in world.get_components(Transform, Renderable):
            parallax = 1.0
            if world.has_component(entity, Parallax):
                parallax = world.component_for_entity(entity, Parallax).factor
            render_queue.append((renderable.layer, entity, transform, renderable, parallax))
        for _, _, transform, renderable, parallax in sorted(render_queue, key=lambda item: item[0]):
            if not renderable.visible:
                continue
            screen_x = self._world_to_screen_x(transform.position.x, camera, parallax)
            screen_y = round(transform.position.y - camera.y)
            if renderable.trail_length > 0:
                self._draw_trail(surface, renderable, round(screen_x), screen_y)
            if renderable.shape == "rect":
                rect = pygame.Rect(0, 0, round(renderable.size.x), round(renderable.size.y))
                if renderable.centered:
                    rect.center = (round(screen_x), screen_y)
                else:
                    rect.topleft = (round(screen_x), screen_y)
                pygame.draw.rect(surface, renderable.color, rect)
            elif renderable.shape == "triangle":
                points = [
                    (screen_x + point[0], screen_y + point[1])
                    for point in renderable.points
                ]
                pygame.draw.polygon(surface, renderable.color, points)
            elif renderable.shape == "circle":
                pygame.draw.circle(
                    surface,
                    renderable.color,
                    (round(screen_x), screen_y),
                    max(1, round(renderable.size.x)),
                )
            elif renderable.shape == "image":
                image = ServiceLocator.images_service.get(renderable.image_path)
                if renderable.sprite_frame_width > 0:
                    frame_w = renderable.sprite_frame_width
                    frame_h = image.get_height()
                    src = pygame.Rect(renderable.sprite_frame * frame_w, 0, frame_w, frame_h)
                    image = image.subsurface(src)
                if renderable.flip_x:
                    image = pygame.transform.flip(image, True, False)
                rect = image.get_rect()
                if renderable.centered:
                    rect.center = (round(screen_x), screen_y)
                else:
                    rect.topleft = (round(screen_x), screen_y)
                surface.blit(image, rect)

    def _draw_trail(self, surface: pygame.Surface, renderable, sx: int, sy: int) -> None:
        c = renderable.color
        h = max(1, round(renderable.size.y))
        steps = renderable.trail_length
        dx = int(-renderable.trail_dir)
        for i in range(1, steps + 1):
            t = i / (steps + 1)
            if t < 0.4:
                ratio = t / 0.4
                r = int(255 + (c.r - 255) * ratio)
                g = int(255 + (c.g - 255) * ratio)
                b = int(255 + (c.b - 255) * ratio)
            else:
                ratio = (t - 0.4) / 0.6
                r = int(c.r * (1.0 - ratio))
                g = int(c.g * (1.0 - ratio))
                b = int(c.b * (1.0 - ratio))
            tx = sx + dx * i
            pygame.draw.rect(surface, pygame.Color(r, g, b), pygame.Rect(tx, sy, 2, h))

    def _world_to_screen_x(self, x: float, camera: Camera, parallax: float) -> float:
        world_width = camera.world_width
        relative = (x - camera.x * parallax + world_width / 2) % world_width - world_width / 2
        return relative
