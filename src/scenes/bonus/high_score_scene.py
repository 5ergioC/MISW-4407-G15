from __future__ import annotations

import pygame

from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.systems.bonus.high_score_system import HighScoreSystem

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
_CYCLE_COLORS = [
    (255, 40,  40),
    (255, 197, 67),
    (246, 245, 89),
    (78,  202, 74),
    (80,  160, 255),
    (255, 80,  230),
]


class HighScoreScene(Scene):
    def enter(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.font_path = self.interface_cfg["font"]["path"]
        root = ServiceLocator.config._config_path
        self.hs_system = HighScoreSystem(root)
        self.score = int(self.engine.shared_state.get("score", 0))
        self.qualifies = self.hs_system.qualifies(self.score)
        self.name_chars = [0, 0, 0]
        self.cursor = 0
        self.done = False
        self.new_rank: int | None = None
        self.elapsed = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.done or not self.qualifies:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.switch_to("menu")
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.name_chars[self.cursor] = (self.name_chars[self.cursor] - 1) % len(_ALPHABET)
        elif event.key == pygame.K_DOWN:
            self.name_chars[self.cursor] = (self.name_chars[self.cursor] + 1) % len(_ALPHABET)
        elif event.key == pygame.K_LEFT and self.cursor > 0:
            self.cursor -= 1
        elif event.key in (pygame.K_RIGHT, pygame.K_SPACE) and self.cursor < 2:
            self.cursor += 1
        elif event.key == pygame.K_RETURN:
            name = "".join(_ALPHABET[i] for i in self.name_chars).strip() or "AAA"
            self.new_rank = self.hs_system.insert(name, self.score)
            self.done = True
        elif event.key == pygame.K_ESCAPE:
            self.switch_to("menu")

    def update(self, dt: float) -> None:
        self.elapsed += dt
        if not self.qualifies:
            self.switch_to("menu")

    def render(self) -> None:
        surface = self.virtual_screen
        surface.fill((0, 0, 0))
        phase = int(self.elapsed * 8) % len(_CYCLE_COLORS)
        color = _CYCLE_COLORS[phase]
        yellow = (255, 244, 72)
        white = (245, 245, 245)
        cyan = (80, 210, 255)

        title = ServiceLocator.texts_service.render_dynamic(self.font_path, 12, "HIGH SCORES", color)
        surface.blit(title, title.get_rect(center=(160, 20)))

        scores = self.hs_system.scores
        for rank, entry in enumerate(scores):
            y = 44 + rank * 22
            rank_color = color if (self.done and rank == self.new_rank) else yellow
            rank_txt = ServiceLocator.texts_service.render_dynamic(self.font_path, 8, f"{rank + 1}.", rank_color)
            name_txt = ServiceLocator.texts_service.render_dynamic(self.font_path, 8, entry["name"], rank_color)
            score_txt = ServiceLocator.texts_service.render_dynamic(self.font_path, 8, f"{entry['score']:06}", rank_color)
            surface.blit(rank_txt,  (60,  y))
            surface.blit(name_txt,  (86,  y))
            surface.blit(score_txt, (148, y))

        if not self.done and self.qualifies:
            self._render_name_entry(surface, cyan)
        else:
            prompt = ServiceLocator.texts_service.render(self.font_path, 7, "PRESS ENTER", white)
            surface.blit(prompt, prompt.get_rect(center=(160, 210)))

    def _render_name_entry(self, surface: pygame.Surface, color: tuple) -> None:
        white = (245, 245, 245)
        yellow = (255, 244, 72)
        score_txt = ServiceLocator.texts_service.render(self.font_path, 8, f"YOUR SCORE: {self.score:06}", white)
        surface.blit(score_txt, score_txt.get_rect(center=(160, 164)))

        prompt = ServiceLocator.texts_service.render(self.font_path, 7, "ENTER YOUR NAME", white)
        surface.blit(prompt, prompt.get_rect(center=(160, 182)))

        for i, char_idx in enumerate(self.name_chars):
            char = _ALPHABET[char_idx]
            char_color = color if i == self.cursor else yellow
            blink = i == self.cursor and int(pygame.time.get_ticks() / 250) % 2 == 0
            char_surf = ServiceLocator.texts_service.render_dynamic(self.font_path, 14, "_" if blink else char, char_color)
            surface.blit(char_surf, char_surf.get_rect(center=(148 + i * 20, 200)))

        hint = ServiceLocator.texts_service.render(self.font_path, 6, "UP/DOWN LETTER   LEFT/RIGHT MOVE   ENTER OK", (150, 150, 150))
        surface.blit(hint, hint.get_rect(center=(160, 222)))
