from __future__ import annotations

import pygame

from src.components.camera import Camera
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

_SCANNER_RECT = pygame.Rect(91, 0, 142, 44)
_HUD_BOTTOM   = 42
_SCAN_WINDOW  = 2500

_PLAYER_COLOR = pygame.Color(245, 245, 245)
_ASTRO_COLOR  = pygame.Color(255, 220, 50)
_PLANET_COLOR = pygame.Color(205, 106, 42)

_ENEMY_DOT_COLORS: dict[str, pygame.Color] = {
    "lander":  pygame.Color(52, 220, 52),
    "mutant":  pygame.Color(255, 80, 255),
    "baiter":  pygame.Color(255, 140, 0),
    "bomber":  pygame.Color(200, 200, 60),
    "pod":     pygame.Color(180, 100, 255),
    "swarmer": pygame.Color(255, 60, 60),
}


class HUDSystem:
    def __init__(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.world_cfg = ServiceLocator.config.get("world")
        self.hud_bottom = _HUD_BOTTOM

        raw_lives = ServiceLocator.images_service.get("img/interface_lives.png")
        lw = max(1, round(raw_lives.get_width() * 1.2))
        lh = max(1, round(raw_lives.get_height() * 1.2))
        self.lives_icon = pygame.transform.smoothscale(raw_lives, (lw, lh))

        raw_bomb = ServiceLocator.images_service.get("img/interface_smart_bomb.png")
        bw = max(1, round(raw_bomb.get_width() * 0.7))
        bh = max(1, round(raw_bomb.get_height() * 0.7))
        self.smart_bomb_icon = pygame.transform.smoothscale(raw_bomb, (bw, bh))

        self.astronaut_icon = self._build_counter_icon("img/astronaut.png", frame_count=3, scale=0.82)

    def render(
        self,
        surface: pygame.Surface,
        shared_state: dict[str, object],
        paused: bool,
        camera: Camera | None = None,
        planet_points: list[tuple[float, float]] | None = None,
        world=None,
        enemy_count: int = 0,
        astronaut_count: int = 0,
        enemy_fire_disabled: bool = False,
        abduction_world_x: float | None = None,
    ) -> None:
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, 320, _HUD_BOTTOM))

        wave = int(shared_state.get("wave", 0))
        self._render_scanner(surface, camera, planet_points or [], world, wave)

        font_path = self.interface_cfg["font"]["path"]
        pause_color = self.interface_cfg["pause_text_color"]

        score_phase = int(pygame.time.get_ticks() / 120) % len(_SCORE_COLORS)
        score_color = _SCORE_COLORS[score_phase]
        score_text = ServiceLocator.texts_service.render_dynamic(
            font_path, 8, f"{shared_state['score']:06}", score_color
        )

        # left panel
        self._render_lives(surface, int(shared_state.get("lives", 0)))
        surface.blit(score_text, (4, 16))
        self._render_smart_bombs(surface, int(shared_state.get("smart_bombs", 0)))

        # right panel — enemy/astronaut counters
        self._render_counts(surface, font_path, enemy_count, astronaut_count)

        # abduction arrow
        if abduction_world_x is not None and camera is not None:
            self._render_abduction_arrow(surface, camera, abduction_world_x)

        # paused overlay
        if paused and pygame.time.get_ticks() // 250 % 2 == 0:
            paused_text = ServiceLocator.texts_service.render(
                font_path, 10, "PAUSED",
                (pause_color["r"], pause_color["g"], pause_color["b"]),
            )
            surface.blit(paused_text, paused_text.get_rect(center=(160, 118)))

        # debug: enemy fire disabled indicator
        if enemy_fire_disabled and pygame.time.get_ticks() // 400 % 2 == 0:
            disabled_text = ServiceLocator.texts_service.render(font_path, 8, "ENEMY FIRE OFF", (220, 60, 60))
            surface.blit(disabled_text, disabled_text.get_rect(center=(160, 12)))

    # ── Lives ──────────────────────────────────────────────────────────────

    def _render_lives(self, surface: pygame.Surface, lives: int) -> None:
        icon = self.lives_icon
        spacing = icon.get_width() + 2
        for i in range(max(0, lives)):
            surface.blit(icon, (4 + i * spacing, 5))

    # ── Smart bombs ────────────────────────────────────────────────────────

    def _render_smart_bombs(self, surface: pygame.Surface, count: int) -> None:
        icon = self.smart_bomb_icon
        base_x = 236
        for i in range(max(0, count)):
            surface.blit(icon, (base_x + i * (icon.get_width() + 1), 28))

    # ── Enemy / astronaut counters (right panel) ───────────────────────────

    def _render_counts(
        self,
        surface: pygame.Surface,
        font_path: str,
        enemy_count: int,
        astronaut_count: int,
    ) -> None:
        yellow = (255, 244, 72)
        white  = (255, 255, 255)
        enemies_label = ServiceLocator.texts_service.render(font_path, 7, "ENEMIES", white)
        enemies_val   = ServiceLocator.texts_service.render_dynamic(font_path, 8, f"{enemy_count:02}", yellow)
        astro_val     = ServiceLocator.texts_service.render(font_path, 7, f"{astronaut_count:02}", yellow)
        surface.blit(enemies_label, enemies_label.get_rect(topright=(314, 6)))
        surface.blit(enemies_val,   enemies_val.get_rect(topright=(314, 16)))
        icon_x, icon_y = 274, 28
        surface.blit(self.astronaut_icon, (icon_x, icon_y))
        surface.blit(astro_val, astro_val.get_rect(topleft=(icon_x + 14, icon_y + 1)))

    # ── Abduction arrow ────────────────────────────────────────────────────

    def _render_abduction_arrow(
        self,
        surface: pygame.Surface,
        camera: Camera,
        target_world_x: float,
    ) -> None:
        dx = (target_world_x - camera.x + camera.world_width / 2) % camera.world_width - camera.world_width / 2
        screen_x = round(dx)
        cy = 56
        color = pygame.Color(255, 92, 64)
        if 0 <= screen_x <= camera.width:
            pygame.draw.polygon(surface, color, [
                (screen_x, cy - 6), (screen_x - 5, cy + 4), (screen_x + 5, cy + 4),
            ])
        elif screen_x < 0:
            pygame.draw.polygon(surface, color, [(8, cy), (20, cy - 6), (20, cy + 6)])
        else:
            pygame.draw.polygon(surface, color, [(312, cy), (300, cy - 6), (300, cy + 6)])

    # ── Scanner / minimap ──────────────────────────────────────────────────

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

        world_width  = camera.world_width
        world_height = float(self.world_cfg.get("height", 256))
        inner = scanner.inflate(-4, -4)
        cx    = scanner.centerx

        # find player position
        player_wx: float = camera.x + camera.width / 2
        player_wy: float = world_height / 2
        if world is not None:
            for _, (_, pt) in world.get_components(Player, Transform):
                player_wx = pt.position.x
                player_wy = pt.position.y
                break

        def world_to_scan(wx: float) -> int:
            ddx = (wx - player_wx + world_width / 2) % world_width - world_width / 2
            return int(cx + ddx * (inner.width / _SCAN_WINDOW))

        # planet terrain
        if planet_points:
            half_w = inner.width // 2 + 2
            clip   = pygame.Rect(scanner.left + 3, scanner.top + 2, scanner.width - 6, scanner.height - 4)
            surface.set_clip(clip)
            prev_pt = None
            for wx, wy in planet_points:
                sx  = world_to_scan(wx)
                sy  = scanner.top + int(wy / world_height * scanner.height)
                cur = (sx, sy)
                if prev_pt is not None:
                    px = prev_pt[0]
                    if abs(sx - cx) <= half_w or abs(px - cx) <= half_w:
                        pygame.draw.line(surface, _PLANET_COLOR, prev_pt, cur, 1)
                prev_pt = cur
            surface.set_clip(None)

        # viewport brackets (┌──┐ top, └──┘ bottom)
        sw    = max(3, int(camera.width * (inner.width / _SCAN_WINDOW) / 2))
        vl, vr = cx - sw, cx + sw
        wc, tk = pygame.Color(245, 245, 245), 3
        pygame.draw.line(surface, wc, (vl, scanner.top),     (vr, scanner.top),     2)
        pygame.draw.line(surface, wc, (vl, scanner.top),     (vl, scanner.top + tk), 2)
        pygame.draw.line(surface, wc, (vr, scanner.top),     (vr, scanner.top + tk), 2)
        pygame.draw.line(surface, wc, (vl, scanner.bottom - 1), (vr, scanner.bottom - 1), 2)
        pygame.draw.line(surface, wc, (vl, scanner.bottom - 1), (vl, scanner.bottom - 1 - tk), 2)
        pygame.draw.line(surface, wc, (vr, scanner.bottom - 1), (vr, scanner.bottom - 1 - tk), 2)

        if world is None:
            return

        blink_on = pygame.time.get_ticks() // 200 % 2 == 0

        def dot_sy(wy: float) -> int:
            sy = scanner.top + int(wy / world_height * scanner.height)
            return max(scanner.top + 1, min(scanner.bottom - 1, sy))

        # astronaut dots
        from src.components.astronaut import Astronaut
        for _, (astronaut, transform) in world.get_components(Astronaut, Transform):
            captured = astronaut.state in ("captured", "abducted", "carried")
            if captured and not blink_on:
                continue
            color = pygame.Color(255, 50, 50) if captured else _ASTRO_COLOR
            sx = world_to_scan(transform.position.x)
            if inner.left <= sx <= inner.right:
                pygame.draw.rect(surface, color, pygame.Rect(sx - 1, dot_sy(transform.position.y), 2, 2))

        # enemy dots
        from src.components.enemy import Enemy
        for _, (enemy, transform) in world.get_components(Enemy, Transform):
            color = _ENEMY_DOT_COLORS.get(enemy.kind, pygame.Color(200, 200, 200))
            sx = world_to_scan(transform.position.x)
            if inner.left <= sx <= inner.right:
                pygame.draw.rect(surface, color, pygame.Rect(sx - 1, dot_sy(transform.position.y), 2, 2))

        # player cross (always centered, Y mapped)
        scan_y = scanner.top + int(player_wy / world_height * scanner.height)
        scan_y = max(scanner.top + 1, min(scanner.bottom - 1, scan_y))
        for ddx, ddy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            surface.set_at((cx + ddx, scan_y + ddy), _PLAYER_COLOR)

    # ── Helpers ────────────────────────────────────────────────────────────

    def _build_counter_icon(self, image_path: str, frame_count: int, scale: float) -> pygame.Surface:
        sheet = ServiceLocator.images_service.get(image_path)
        fw    = max(1, sheet.get_width() // max(1, frame_count))
        frame = sheet.subsurface(pygame.Rect(0, 0, fw, sheet.get_height())).copy()
        tw    = max(1, round(frame.get_width()  * scale))
        th    = max(1, round(frame.get_height() * scale))
        if frame.get_size() != (tw, th):
            frame = pygame.transform.smoothscale(frame, (tw, th))
        return frame
