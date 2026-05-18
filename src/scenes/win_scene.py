from __future__ import annotations

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.systems.bonus.high_score_system import HighScoreSystem
from src.systems.input_command_system import InputCommandSystem


class WinScene(Scene):
    def enter(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.hs_system = HighScoreSystem(ServiceLocator.config._config_path)
        self.elapsed = 0.0
        self.input_system = InputCommandSystem(
            {
                pygame.K_RETURN: SceneCommand(self._on_confirm),
                pygame.K_ESCAPE: SceneCommand(lambda: self.switch_to("menu")),
            }
        )

    def _on_confirm(self) -> None:
        score = int(self.engine.shared_state.get("score", 0))
        if self.hs_system.qualifies(score):
            self.switch_to("high_score")
        else:
            self.switch_to("menu")

    def handle_event(self, event: pygame.event.Event) -> None:
        self.input_system.process_event(self.world, event)

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def render(self) -> None:
        surface = self.virtual_screen
        surface.fill((0, 0, 0))
        font_path = self.interface_cfg["font"]["path"]
        white = (245, 245, 245)
        yellow = (255, 244, 72)
        cyan = (80, 210, 255)

        phase = int(self.elapsed * 6) % 6
        colors = [(255,40,40),(255,197,67),(246,245,89),(78,202,74),(80,160,255),(255,80,230)]

        title = ServiceLocator.texts_service.render_dynamic(font_path, 10, "LEVEL COMPLETE", colors[phase])
        score = int(self.engine.shared_state.get("score", 0))
        score_label = ServiceLocator.texts_service.render(font_path, 7, "SCORE", white)
        score_val = ServiceLocator.texts_service.render_dynamic(font_path, 14, f"{score:06}", yellow)

        hs = self.hs_system.scores[0]["score"] if self.hs_system.scores else 0
        is_record = score >= hs
        hs_label = ServiceLocator.texts_service.render_dynamic(
            font_path, 7, "NEW RECORD!" if is_record else "BEST", colors[phase] if is_record else white
        )
        hs_val = ServiceLocator.texts_service.render(font_path, 8, f"{hs:06}", cyan)

        prompt = ServiceLocator.texts_service.render(font_path, 7, "PRESS ENTER", white)

        surface.blit(title,       title.get_rect(center=(160, 72)))
        surface.blit(score_label, score_label.get_rect(center=(160, 100)))
        surface.blit(score_val,   score_val.get_rect(center=(160, 116)))
        surface.blit(hs_label,    hs_label.get_rect(center=(160, 142)))
        surface.blit(hs_val,      hs_val.get_rect(center=(160, 156)))
        if int(self.elapsed * 2) % 2 == 0:
            surface.blit(prompt,  prompt.get_rect(center=(160, 190)))
