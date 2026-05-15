from __future__ import annotations

import pygame

from src.components.camera import Camera
from src.components.laser import Laser
from src.components.parallax import Parallax
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator
from src.components.player import Player


class RenderSystem:
    def render(self, world, surface: pygame.Surface, camera: Camera) -> None:
        render_queue: list[tuple[int, int, Transform, Renderable, float, float | None, bool]] = []
        for entity, (transform, renderable) in world.get_components(Transform, Renderable):
            parallax = 1.0
            if world.has_component(entity, Parallax):
                parallax = world.component_for_entity(entity, Parallax).factor
            velocity_x = None
            if world.has_component(entity, Velocity):
                velocity_x = world.component_for_entity(entity, Velocity).value.x
            is_laser = world.has_component(entity, Laser)
            render_queue.append((renderable.layer, entity, transform, renderable, parallax, velocity_x, is_laser))
        for _, entity, transform, renderable, parallax, velocity_x, is_laser in sorted(render_queue, key=lambda item: item[0]):
            if not renderable.visible:
                continue
            screen_x = self._world_to_screen_x(transform.position.x, camera, parallax)
            screen_y = round(transform.position.y - camera.y)
            if renderable.shape == "rect":
                if is_laser and velocity_x is not None:
                    self._draw_laser(surface, round(screen_x), screen_y, renderable, velocity_x)
                else:
                    rect = pygame.Rect(
                        round(screen_x),
                        screen_y,
                        round(renderable.size.x),
                        round(renderable.size.y),
                    )
                    pygame.draw.rect(surface, renderable.color, rect)
            elif renderable.shape == "triangle":
                points = [
                    (screen_x + point[0], screen_y + point[1])
                    for point in renderable.points
                ]
                pygame.draw.polygon(surface, renderable.color, points)
            elif renderable.shape == "image":
                image = ServiceLocator.images_service.get(renderable.image_path)
                if renderable.flip_x:
                    image = pygame.transform.flip(image, True, False)
                rect = image.get_rect()
                if renderable.centered:
                    rect.center = (round(screen_x), screen_y)
                else:
                    rect.topleft = (round(screen_x), screen_y)

                if world.has_component(entity, Player):
                    player = world.component_for_entity(entity, Player)
                    if player.thrust_input.length_squared() > 0.0 or player.is_shooting:
                        try:
                            sheet = ServiceLocator.images_service.get("img/player_burner_moving.png")
                            frame_count = 3
                            frame_w = sheet.get_width() // frame_count if frame_count > 0 else sheet.get_width()
                            frame_h = sheet.get_height()
                            frame_index = player.thrust_anim_frame % frame_count
                            flame = sheet.subsurface(pygame.Rect(frame_w * frame_index, 0, frame_w, frame_h)).copy()
                        except Exception:
                            try:
                                flame = ServiceLocator.images_service.get("img/player_burner_idle.png")
                            except Exception:
                                flame = None
                        if flame is not None:
                            if renderable.flip_x:
                                flame = pygame.transform.flip(flame, True, False)
                            try:
                                scale_factor = 1
                                fw = max(1, int(flame.get_width() * scale_factor))
                                fh = max(1, int(flame.get_height() * scale_factor))
                                flame = pygame.transform.smoothscale(flame, (fw, fh))
                            except Exception:
                                pass
                            flame_rect = flame.get_rect()
                            offset_x = -int(rect.width * 0.45)
                            offset_y = int(rect.height * 0.15)
                            if renderable.flip_x:
                                offset_x = -offset_x
                            if renderable.centered:
                                flame_rect.center = (rect.centerx + offset_x, rect.centery + offset_y)
                            else:
                                flame_rect.topleft = (rect.left + offset_x, rect.top + offset_y)
                            surface.blit(flame, flame_rect)

                surface.blit(image, rect)

    def _draw_laser(self, surface: pygame.Surface, screen_x: int, screen_y: int, renderable: Renderable, velocity_x: float) -> None:
        beam_height = max(1, round(renderable.size.y))
        beam_width = max(1, round(renderable.size.x))
        tail_segments = [
            (3, 1, pygame.Color(255, 90, 28)),
            (4, 1, pygame.Color(255, 120, 45)),
            (5, 1, pygame.Color(255, 155, 70)),
            (6, 1, pygame.Color(255, 190, 105)),
            (8, 1, pygame.Color(255, 220, 150)),
            (10, 1, pygame.Color(255, 238, 190)),
        ]
        head_segment = (4, 1, pygame.Color(255, 255, 230))
        segments = tail_segments + [head_segment]

        total_width = sum(width for width, _, _ in segments)
        difference = beam_width - total_width
        if difference != 0:
            width, height, color = tail_segments[-1]
            tail_segments[-1] = (max(1, width + difference), height, color)
            segments = tail_segments + [head_segment]

        if velocity_x < 0:
            segments = list(reversed(segments))
            current_x = screen_x - beam_width
        else:
            current_x = screen_x

        for index, (width, height, color) in enumerate(segments):
            height = min(height, beam_height)
            y_offset = (beam_height - height) // 2
            rect = pygame.Rect(current_x, screen_y + y_offset, width, height)
            pygame.draw.rect(surface, color, rect)
            current_x += width

    def _world_to_screen_x(self, x: float, camera: Camera, parallax: float) -> float:
        world_width = camera.world_width
        relative = (x - camera.x * parallax + world_width / 2) % world_width - world_width / 2
        return relative
