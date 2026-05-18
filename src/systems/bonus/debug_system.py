from __future__ import annotations

import pygame

from src.components.astronaut import Astronaut
from src.components.camera import Camera
from src.components.collider import Collider
from src.components.enemy import Enemy
from src.components.player import Player
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.engine.service_locator import ServiceLocator

_GREEN  = pygame.Color(0, 255, 0)
_RED    = pygame.Color(255, 50, 50)
_YELLOW = pygame.Color(255, 255, 0)
_CYAN   = pygame.Color(0, 220, 255)
_WHITE  = pygame.Color(255, 255, 255)


class DebugSystem:
    def __init__(self) -> None:
        self.enabled = False
        cfg = ServiceLocator.config.get("debug")
        self._show_colliders   = cfg.get("show_colliders", True)
        self._show_entity_ids  = cfg.get("show_entity_ids", False)
        self._show_ai_states   = cfg.get("show_ai_states", True)
        self._show_camera      = cfg.get("show_camera_bounds", True)
        self._font_path        = ServiceLocator.config.get("interface")["font"]["path"]

    def toggle(self) -> None:
        self.enabled = not self.enabled

    def update(self, world, dt: float) -> None:
        del world, dt

    def render(self, world, surface: pygame.Surface, camera: Camera) -> None:
        if not self.enabled:
            return

        world_width = camera.world_width

        # FPS (clock ticks approximation via caption)
        fps_surf = ServiceLocator.texts_service.render_dynamic(
            self._font_path, 7, f"DBG  CAM X:{int(camera.x)}  Y:{int(camera.y)}", _YELLOW
        )
        surface.blit(fps_surf, (4, 44))

        for entity, (transform, renderable) in world.get_components(Transform, Renderable):
            sx = self._world_to_screen(transform.position.x, camera, world_width)
            sy = int(transform.position.y - camera.y)

            if self._show_colliders and world.has_component(entity, Collider):
                col = world.component_for_entity(entity, Collider)
                color = _RED if world.has_component(entity, Player) else _GREEN
                rect = pygame.Rect(
                    round(sx + col.offset.x - col.size.x / 2),
                    round(sy + col.offset.y - col.size.y / 2),
                    round(col.size.x),
                    round(col.size.y),
                )
                pygame.draw.rect(surface, color, rect, 1)

            if self._show_entity_ids:
                id_surf = ServiceLocator.texts_service.render_dynamic(
                    self._font_path, 6, str(entity), _WHITE
                )
                surface.blit(id_surf, (round(sx), sy - 8))

            if self._show_ai_states:
                state_text = None
                if world.has_component(entity, Enemy):
                    e = world.component_for_entity(entity, Enemy)
                    state_text = f"{e.kind[:3].upper()} {e.state}"
                elif world.has_component(entity, Astronaut):
                    a = world.component_for_entity(entity, Astronaut)
                    state_text = f"AST {a.state}"
                if state_text:
                    st = ServiceLocator.texts_service.render_dynamic(
                        self._font_path, 6, state_text, _CYAN
                    )
                    surface.blit(st, (round(sx), sy + 10))

        if self._show_camera:
            cam_rect = pygame.Rect(0, int(-camera.y), int(camera.width), int(camera.height))
            pygame.draw.rect(surface, _YELLOW, cam_rect, 1)

    def _world_to_screen(self, x: float, camera: Camera, world_width: float) -> float:
        return (x - camera.x + world_width / 2) % world_width - world_width / 2
