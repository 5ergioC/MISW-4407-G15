from __future__ import annotations

import math
import random

import pygame

from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator

_CYCLE_COLORS = [
    (255, 40,  40),
    (255, 197, 67),
    (246, 245, 89),
    (78,  202, 74),
    (80,  160, 255),
    (255, 80,  230),
]

_INSTRUCTIONS = [
    ("ARROWS / WASD", "MOVE SHIP"),
    ("SPACE",         "FIRE LASER"),
    ("B",             "SMART BOMB"),
    ("P",             "PAUSE"),
    ("RESCUE HUMANS", "BEFORE LANDERS REACH TOP"),
    ("LANDER -> TOP", "BECOMES MUTANT"),
]

_ENEMIES = [
    ("LANDER",  "img/enemy_lander.png",  15, "lander_destroyed"),
    ("MUTANT",  "img/enemy_mutant.png",  11, "mutant_destroyed"),
    ("BAITER",  "img/enemy_baiter.png",  16, "baiter_destroyed"),
    ("BOMBER",  "img/enemy_bomber.png",  13, "bomber_destroyed"),
    ("POD",     "img/enemy_pod.png",     15, "pod_destroyed"),
    ("SWARMER", "img/enemy_swarmer.png",  0, "swarmer_destroyed"),
]

_PAGE_SCORES    = 0
_PAGE_CONTROLS  = 1
_PAGE_DURATIONS = [7.0, 8.0]
_FADE_TIME      = 0.4


class AttractScene(Scene):
    def enter(self) -> None:
        self.interface_cfg  = ServiceLocator.config.get("interface")
        self.scoring_cfg    = ServiceLocator.config.get("scoring")
        self.font_path      = self.interface_cfg["font"]["path"]
        self.elapsed        = 0.0
        self.page_timer     = 0.0
        self.page           = _PAGE_SCORES
        self._rng           = random.Random(42)
        self._stars         = self._make_stars()
        self._terrain       = self._make_terrain()
        self._instr_idx     = 0
        self._instr_timer   = 0.0
        self._instr_interval = 2.8

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.switch_to("menu")

    def update(self, dt: float) -> None:
        self.elapsed    += dt
        self.page_timer += dt
        if self.page_timer >= _PAGE_DURATIONS[self.page]:
            self.page_timer = 0.0
            self.page = _PAGE_CONTROLS if self.page == _PAGE_SCORES else _PAGE_SCORES
        self._instr_timer += dt
        if self._instr_timer >= self._instr_interval:
            self._instr_timer = 0.0
            self._instr_idx = (self._instr_idx + 1) % len(_INSTRUCTIONS)
        if self.elapsed > 40.0:
            self.switch_to("menu")

    def render(self) -> None:
        surface = self.virtual_screen
        surface.fill((0, 0, 0))
        self._render_stars(surface)
        self._render_terrain(surface)
        self._render_scanner_frame(surface)
        fade_in  = min(1.0, self.page_timer / _FADE_TIME)
        fade_out = min(1.0, (_PAGE_DURATIONS[self.page] - self.page_timer) / _FADE_TIME)
        alpha    = int(255 * min(fade_in, fade_out))
        page_surf = pygame.Surface((320, 256), pygame.SRCALPHA)
        if self.page == _PAGE_SCORES:
            self._render_enemy_table(page_surf)
        else:
            self._render_controls_page(page_surf)
        page_surf.set_alpha(alpha)
        surface.blit(page_surf, (0, 0))
        self._render_footer(surface)

    # ------------------------------------------------------------------ pages

    def _render_enemy_table(self, surface: pygame.Surface) -> None:
        green  = (52, 174, 45)
        yellow = (255, 244, 72)

        scanner_lbl = ServiceLocator.texts_service.render(self.font_path, 8, "SCANNER", green)
        surface.blit(scanner_lbl, scanner_lbl.get_rect(center=(160, 52)))

        cols = [82, 160, 238]
        rows = [90, 155]
        for idx, (name, img_path, frame_w, score_key) in enumerate(_ENEMIES):
            col = idx % 3
            row = idx // 3
            cx  = cols[col]
            cy  = rows[row]

            try:
                img = ServiceLocator.images_service.get(img_path)
                if frame_w > 0:
                    src = pygame.Rect(0, 0, frame_w, img.get_height())
                    img = img.subsurface(src)
                surface.blit(img, img.get_rect(center=(cx, cy)))
            except Exception:
                pass

            phase = int(self.elapsed * 6) % len(_CYCLE_COLORS)
            name_surf  = ServiceLocator.texts_service.render_dynamic(
                self.font_path, 7, name, _CYCLE_COLORS[phase]
            )
            pts        = self.scoring_cfg.get(score_key, 150)
            score_surf = ServiceLocator.texts_service.render(
                self.font_path, 8, str(pts), yellow
            )
            surface.blit(name_surf,  name_surf.get_rect(center=(cx, cy + 14)))
            surface.blit(score_surf, score_surf.get_rect(center=(cx, cy + 24)))

    def _render_controls_page(self, surface: pygame.Surface) -> None:
        logo  = ServiceLocator.images_service.get("img/game_logo.png")
        phase = int(self.elapsed * 8) % len(_CYCLE_COLORS)
        color = _CYCLE_COLORS[phase]
        surface.blit(logo, logo.get_rect(center=(160, 68)))
        title = ServiceLocator.texts_service.render_dynamic(self.font_path, 10, "DEFENDER", color)
        surface.blit(title, title.get_rect(center=(160, 96)))

        key, action = _INSTRUCTIONS[self._instr_idx]
        fade_in  = min(1.0, self._instr_timer / 0.3)
        fade_out = 1.0 - max(0.0, (self._instr_timer - (self._instr_interval - 0.3)) / 0.3)
        alpha    = int(255 * min(fade_in, fade_out))
        phase2   = int(self.elapsed * 6) % len(_CYCLE_COLORS)
        key_s    = ServiceLocator.texts_service.render_dynamic(
            self.font_path, 9, f"[ {key} ]", _CYCLE_COLORS[phase2]
        )
        act_s    = ServiceLocator.texts_service.render_dynamic(
            self.font_path, 7, action, (220, 220, 220)
        )
        key_s.set_alpha(alpha)
        act_s.set_alpha(alpha)
        surface.blit(key_s, key_s.get_rect(center=(160, 148)))
        surface.blit(act_s, act_s.get_rect(center=(160, 162)))

    # ---------------------------------------------------------------- shared

    def _render_footer(self, surface: pygame.Surface) -> None:
        yellow = (255, 244, 72)
        white  = (245, 245, 245)
        if int(self.elapsed * 2) % 2 == 0:
            prompt = ServiceLocator.texts_service.render(self.font_path, 8, "PRESS ANY KEY", yellow)
            surface.blit(prompt, prompt.get_rect(center=(160, 200)))
        credit = ServiceLocator.texts_service.render(self.font_path, 6, "WILLIAMS ELECTRONICS  1981", white)
        surface.blit(credit, credit.get_rect(center=(160, 214)))

    def _make_stars(self) -> list:
        colors = [
            pygame.Color(255, 85, 52), pygame.Color(255, 197, 67),
            pygame.Color(246, 245, 89), pygame.Color(78, 202, 74),
            pygame.Color(210, 210, 210),
        ]
        return [
            (self._rng.uniform(0, 320), self._rng.uniform(44, 185),
             self._rng.choice(colors), self._rng.uniform(4.0, 14.0))
            for _ in range(40)
        ]

    def _make_terrain(self) -> list:
        points: list[tuple[int, int]] = []
        y = 230
        for x in range(0, 324, 4):
            y += self._rng.choice((-2, -1, 0, 0, 1, 2))
            y  = max(210, min(248, y))
            points.append((x, y))
        return points

    def _render_stars(self, surface: pygame.Surface) -> None:
        for x, y, color, speed in self._stars:
            sx    = (x - self.elapsed * speed) % 320
            blink = 0.55 + 0.45 * math.sin(self.elapsed * 3.0 + x)
            surface.fill(
                (int(color.r * blink), int(color.g * blink), int(color.b * blink)),
                pygame.Rect(round(sx), round(y), 1, 1),
            )

    def _render_terrain(self, surface: pygame.Surface) -> None:
        orange  = pygame.Color(205, 106, 42)
        offset  = -int(self.elapsed * 12) % 4
        shifted = [(x + offset, y) for x, y in self._terrain]
        for i in range(len(shifted) - 1):
            pygame.draw.line(surface, orange, shifted[i], shifted[i + 1], 1)

    def _render_scanner_frame(self, surface: pygame.Surface) -> None:
        phase = int(self.elapsed * 8) % len(_CYCLE_COLORS)
        border = pygame.Color(*_CYCLE_COLORS[phase])
        pygame.draw.line(surface, border, (0, 42), (320, 42), 2)
        pygame.draw.rect(surface, border, pygame.Rect(91, 4, 142, 32), 2)
