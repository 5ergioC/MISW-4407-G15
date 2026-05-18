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

_SCANNER_RECT  = pygame.Rect(91, 0, 142, 44)
_HUD_BOTTOM    = 42
_SCAN_WINDOW   = 2500
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
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, 320, _HUD_BOTTOM))
        wave = int(shared_state.get("wave", 0))
        self._render_scanner(surface, camera, planet_points or [], world, wave)
        font_path = self.interface_cfg["font"]["path"]
        pause_color = self.interface_cfg["pause_text_color"]
        yellow = (255, 244, 72)

        score_phase = int(pygame.time.get_ticks() / 120) % len(_SCORE_COLORS)
        score_color = _SCORE_COLORS[score_phase]
        score_str = f"{shared_state['score']:06}"
        score_text = ServiceLocator.texts_service.render_dynamic(font_path, 8, score_str, score_color)
        enemy_count = sum(1 for _ in world.get_components(Enemy)) if world is not None else 0
        enemies_text = ServiceLocator.texts_service.render_dynamic(font_path, 7, f"ENEMIES {enemy_count}", yellow)

        # left panel: lives icons top, score below
        self._render_lives(surface, shared_state)
        surface.blit(score_text, (4, 16))
        # right panel (x 234-320): enemies top, smart bombs below
        surface.blit(enemies_text, (236, 4))
        self._render_smart_bombs(surface, font_path, shared_state)
        if world is not None and camera is not None:
            self._render_capture_arrows(surface, world, camera)
        if paused and pygame.time.get_ticks() // 250 % 2 == 0:
            paused_text = ServiceLocator.texts_service.render(
                font_path, 10, "PAUSED", (pause_color["r"], pause_color["g"], pause_color["b"])
            )
            rect = paused_text.get_rect(center=(160, 118))
            surface.blit(paused_text, rect)

    def _render_lives(self, surface: pygame.Surface, shared_state: dict) -> None:
        lives = int(shared_state.get("lives", 0))
        icon = ServiceLocator.images_service.get("img/interface_lives.png")
        icon_w = icon.get_width() + 1
        for i in range(lives):
            surface.blit(icon, (4 + i * icon_w, 5))

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

    def _render_capture_arrows(
        self,
        surface: pygame.Surface,
        world,
        camera: Camera,
    ) -> None:
        if pygame.time.get_ticks() // 150 % 2 == 0:
            return

        player_x: float | None = None
        for _, (_, transform) in world.get_components(Player, Transform):
            player_x = transform.position.x
            break
        if player_x is None:
            return

        world_width = camera.world_width
        captured_states = ("captured", "abducted", "carried")
        arrow_left = False
        arrow_right = False

        for _, (astronaut, transform) in world.get_components(Astronaut, Transform):
            if astronaut.state not in captured_states:
                continue
            dx = (transform.position.x - player_x + world_width / 2) % world_width - world_width / 2
            if dx < -camera.width / 2:
                arrow_left = True
            elif dx > camera.width / 2:
                arrow_right = True

        color = _CAPTURE_COLOR
        size = 7
        mid_y = 140

        if arrow_left:
            pts = [(8, mid_y), (8 + size, mid_y - size), (8 + size, mid_y + size)]
            pygame.draw.polygon(surface, color, pts)

        if arrow_right:
            pts = [(312, mid_y), (312 - size, mid_y - size), (312 - size, mid_y + size)]
            pygame.draw.polygon(surface, color, pts)

    def _render_scanner(
        self,
        surface: pygame.Surface,
        camera: Camera | None,
        planet_points: list[tuple[float, float]],
        world=None,
        wave: int = 0,
    ) -> None:
        scanner = _SCANNER_RECT
        border_color = pygame.Color(*_SCORE_COLORS[wave % len(_SCORE_COLORS)])
        pygame.draw.line(surface, border_color, (0, _HUD_BOTTOM), (320, _HUD_BOTTOM), 2)
        pygame.draw.rect(surface, border_color, scanner, 2)

        if camera is None:
            return

        world_width = camera.world_width
        inner = scanner.inflate(-4, -4)

        world_cfg = ServiceLocator.config.get("world")
        world_height: float = world_cfg.get("height", 256)

        # find player world position for centering
        player_wx: float = camera.x + camera.width / 2
        player_wy: float = world_height / 2
        if world is not None:
            for _, (_, pt) in world.get_components(Player, Transform):
                player_wx = pt.position.x
                player_wy = pt.position.y
                break

        half_win = _SCAN_WINDOW / 2
        cx = scanner.centerx

        def world_to_scan(wx: float) -> int:
            dx = (wx - player_wx + world_width / 2) % world_width - world_width / 2
            return int(cx + dx * (inner.width / _SCAN_WINDOW))

        # planet terrain — same Y mapping as player for accuracy
        if planet_points:
            half_w = inner.width // 2 + 2
            surface.set_clip(pygame.Rect(scanner.left + 3, scanner.top + 2, scanner.width - 6, scanner.height - 4))
            prev_pt = None
            for wx, wy in planet_points:
                sx = world_to_scan(wx)
                sy = scanner.top + int(wy / world_height * scanner.height)
                cur_pt = (sx, sy)
                if prev_pt is not None:
                    px = prev_pt[0]
                    if abs(sx - cx) <= half_w or abs(px - cx) <= half_w:
                        pygame.draw.line(surface, _PLANET_COLOR, prev_pt, cur_pt, 1)
                prev_pt = cur_pt
            surface.set_clip(None)

        # camera viewport — corner brackets: ┌──┐ top, └──┘ bottom, narrow
        screen_half_w = max(3, int(camera.width * (inner.width / _SCAN_WINDOW) / 2))
        vl = cx - screen_half_w
        vr = cx + screen_half_w
        wc = pygame.Color(245, 245, 245)
        tk = 3  # tick height px
        # top bar + downward ticks (┌──┐)
        pygame.draw.line(surface, wc, (vl, scanner.top), (vr, scanner.top), 2)
        pygame.draw.line(surface, wc, (vl, scanner.top), (vl, scanner.top + tk), 2)
        pygame.draw.line(surface, wc, (vr, scanner.top), (vr, scanner.top + tk), 2)
        # bottom bar + upward ticks (└──┘)
        pygame.draw.line(surface, wc, (vl, scanner.bottom - 2), (vr, scanner.bottom - 2), 2)
        pygame.draw.line(surface, wc, (vl, scanner.bottom - 2), (vl, scanner.bottom - 2 - tk), 2)
        pygame.draw.line(surface, wc, (vr, scanner.bottom - 2), (vr, scanner.bottom - 2 - tk), 2)

        if world is None:
            return

        blink_on = pygame.time.get_ticks() // 200 % 2 == 0

        # astronaut dots
        for _, (astronaut, transform) in world.get_components(Astronaut, Transform):
            captured = astronaut.state in ("captured", "abducted", "carried")
            if captured and not blink_on:
                continue
            color = _CAPTURE_COLOR if captured else _ASTRO_COLOR
            sx = world_to_scan(transform.position.x)
            if inner.left <= sx <= inner.right:
                pygame.draw.rect(surface, color, pygame.Rect(sx - 1, scanner.centery + 1, 2, 2))

        # enemy dots
        for _, (enemy, transform) in world.get_components(Enemy, Transform):
            color = _ENEMY_DOT_COLORS.get(enemy.kind, pygame.Color(200, 200, 200))
            sx = world_to_scan(transform.position.x)
            if inner.left <= sx <= inner.right:
                pygame.draw.rect(surface, color, pygame.Rect(sx - 1, scanner.centery - 2, 2, 2))

        # player cross — X always centered, Y mapped from world height
        scan_y = scanner.top + int((player_wy / world_height) * scanner.height)
        scan_y = max(scanner.top + 1, min(scanner.bottom - 1, scan_y))
        for ddx, ddy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            surface.set_at((cx + ddx, scan_y + ddy), _PLAYER_COLOR)
