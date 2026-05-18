from __future__ import annotations

import pygame

import math

from src.components.astronaut import Astronaut
from src.components.camera import Camera
from src.components.enemy import Enemy
from src.components.player import Player
from src.components.transform import Transform
from src.engine.service_locator import ServiceLocator

_SCORE_COLORS: list[tuple[int, int, int]] = [
    (255, 40,  40),
    (255, 197, 67),
    (246, 245, 89),
    (78,  202, 74),
    (80,  160, 255),
    (255, 80,  230),
]

_SCANNER_RECT = pygame.Rect(90, 1, 144, 40)
_ENEMY_DOT_COLORS: dict[str, pygame.Color] = {
    "lander":  pygame.Color(52, 220, 52),
    "mutant":  pygame.Color(255, 80, 255),
    "baiter":  pygame.Color(255, 140, 0),
    "bomber":  pygame.Color(200, 200, 60),
    "pod":     pygame.Color(180, 100, 255),
    "swarmer": pygame.Color(255, 60, 60),
}
_PLAYER_COLOR    = pygame.Color(245, 245, 245)
_ASTRO_COLOR     = pygame.Color(255, 220, 50)
_CAPTURE_COLOR   = pygame.Color(255, 50, 50)
_PLANET_COLOR    = pygame.Color(205, 106, 42)
_BORDER_COLOR    = pygame.Color(52, 174, 45)


class HUDSystem:
    def __init__(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")

    def render(
        self,
        surface: pygame.Surface,
        shared_state: dict[str, object],
        paused: bool,
        camera: Camera | None = None,
        planet_points: list[tuple[float, float]] | None = None,
        world=None,
    ) -> None:
        self._render_scanner(surface, camera, planet_points or [], world)
        font_path = self.interface_cfg["font"]["path"]
        pause_color = self.interface_cfg["pause_text_color"]
        yellow = (255, 244, 72)

        score_phase = int(pygame.time.get_ticks() / 120) % len(_SCORE_COLORS)
        score_color = _SCORE_COLORS[score_phase]
        score_str = f"{shared_state['score']:06}"
        score_text = ServiceLocator.texts_service.render_dynamic(font_path, 8, score_str, score_color)
        lives_text = ServiceLocator.texts_service.render(font_path, 7, f"LIVES {shared_state['lives']}", yellow)

        enemy_count = sum(1 for _ in world.get_components(Enemy)) if world is not None else 0
        enemies_text = ServiceLocator.texts_service.render_dynamic(font_path, 7, f"ENEMIES {enemy_count}", yellow)

        # left panel (x 0-88): lives top, score below
        surface.blit(lives_text, (4, 4))
        surface.blit(score_text, (4, 16))
        # right panel (x 234-320): enemies top, smart bombs below
        surface.blit(enemies_text, (236, 4))
        self._render_smart_bombs(surface, font_path, shared_state)
        if paused and pygame.time.get_ticks() // 250 % 2 == 0:
            paused_text = ServiceLocator.texts_service.render(
                font_path, 10, "PAUSED", (pause_color["r"], pause_color["g"], pause_color["b"])
            )
            rect = paused_text.get_rect(center=(160, 118))
            surface.blit(paused_text, rect)

    def _render_smart_bombs(
        self,
        surface: pygame.Surface,
        font_path: str,
        shared_state: dict,
    ) -> None:
        count = int(shared_state.get("smart_bombs", 0))
        icon = ServiceLocator.images_service.get("img/interface_smart_bomb.png")
        icon_w = icon.get_width()
        for i in range(count):
            surface.blit(icon, (236 + i * (icon_w + 1), 16))

    def _render_scanner(
        self,
        surface: pygame.Surface,
        camera: Camera | None,
        planet_points: list[tuple[float, float]],
        world=None,
    ) -> None:
        scanner = _SCANNER_RECT
        hud_bottom = scanner.bottom + 2
        pygame.draw.line(surface, _BORDER_COLOR, (0, hud_bottom), (320, hud_bottom), 2)
        pygame.draw.rect(surface, _BORDER_COLOR, scanner, 2)
        pygame.draw.rect(surface, _BORDER_COLOR, pygame.Rect(234, 1, 86, hud_bottom - 2), 2)

        if camera is None:
            return

        world_width = camera.world_width
        scale_x = scanner.width / world_width

        # planet terrain line
        if planet_points:
            min_y = min(y for _, y in planet_points)
            max_y = max(y for _, y in planet_points)
            height = max(1.0, max_y - min_y)
            scaled = []
            for wx, wy in planet_points:
                x = scanner.left + wx * scale_x
                y = scanner.bottom - 4 - ((max_y - wy) / height) * (scanner.height - 10)
                if scanner.left <= x <= scanner.right:
                    scaled.append((x, y))
            if len(scaled) > 1:
                pygame.draw.lines(surface, _PLANET_COLOR, False, scaled, 1)

        # camera viewport indicator
        view_x = scanner.left + (camera.x % world_width) * scale_x
        view_w = max(6, camera.width * scale_x)
        pygame.draw.line(surface, pygame.Color(245, 245, 245), (view_x, scanner.top), (view_x + view_w, scanner.top), 2)
        pygame.draw.line(surface, pygame.Color(245, 245, 245), (view_x, scanner.bottom), (view_x + view_w, scanner.bottom), 2)

        if world is None:
            return

        blink_on = pygame.time.get_ticks() // 200 % 2 == 0

        # astronaut dots
        for _, (astronaut, transform) in world.get_components(Astronaut, Transform):
            captured = astronaut.state in ("captured", "abducted", "carried")
            if captured and not blink_on:
                continue
            color = _CAPTURE_COLOR if captured else _ASTRO_COLOR
            sx = int(scanner.left + (transform.position.x % world_width) * scale_x)
            if scanner.left <= sx <= scanner.right:
                pygame.draw.rect(surface, color, pygame.Rect(sx - 1, scanner.centery, 2, 2))

        # enemy dots
        for _, (enemy, transform) in world.get_components(Enemy, Transform):
            color = _ENEMY_DOT_COLORS.get(enemy.kind, pygame.Color(200, 200, 200))
            sx = int(scanner.left + (transform.position.x % world_width) * scale_x)
            if scanner.left <= sx <= scanner.right:
                pygame.draw.rect(surface, color, pygame.Rect(sx - 1, scanner.centery - 3, 2, 2))

        # player dot — drawn last so it's always on top
        for _, (_, transform) in world.get_components(Player, Transform):
            sx = int(scanner.left + (transform.position.x % world_width) * scale_x)
            sx = max(scanner.left, min(scanner.right, sx))
            pygame.draw.rect(surface, _PLAYER_COLOR, pygame.Rect(sx - 1, scanner.centery - 1, 3, 3))
