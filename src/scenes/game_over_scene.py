from __future__ import annotations

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.systems.bonus.high_score_system import HighScoreSystem
from src.systems.input_command_system import InputCommandSystem


class GameOverScene(Scene):
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
        # play game over sound if configured
        audio_cfg = ServiceLocator.config.get("audio")
        game_over_sound = audio_cfg.get("sounds", {}).get("game_over")
        if game_over_sound:
            ServiceLocator.sounds_service.play(game_over_sound)

    def _on_confirm(self) -> None:
        score = int(self.engine.shared_state.get("score", 0))
        if self.hs_system.qualifies(score):
            self.switch_to("high_score")
        else:
            self.switch_to("menu")

    def handle_event(self, event: pygame.event.Event) -> None:
        self.input_system.process_event(self.world, event)

    def update(self, dt: float) -> None:
        del dt

    def update(self, dt: float) -> None:
        self.elapsed = getattr(self, "elapsed", 0.0) + dt

    def render(self) -> None:
        surface = self.virtual_screen
        surface.fill((0, 0, 0))
        font_path = self.interface_cfg["font"]["path"]
        pause_color = self.interface_cfg["pause_text_color"]
        normal_color = self.interface_cfg["normal_text_color"]
        yellow = (255, 244, 72)
        white = (245, 245, 245)

        elapsed = getattr(self, "elapsed", 0.0)
        phase = int(elapsed * 4) % 6
        colors = [(255,40,40),(255,197,67),(246,245,89),(78,202,74),(80,160,255),(255,80,230)]

        title = ServiceLocator.texts_service.render_dynamic(font_path, 16, "GAME OVER", colors[phase])
        reason = ServiceLocator.texts_service.render(
            font_path, 7,
            str(self.engine.shared_state.get("game_over_reason", "")),
            (normal_color["r"], normal_color["g"], normal_color["b"]),
        )
        score = int(self.engine.shared_state.get("score", 0))
        score_label = ServiceLocator.texts_service.render(font_path, 7, "SCORE", white)
        score_val = ServiceLocator.texts_service.render_dynamic(font_path, 14, f"{score:06}", yellow)

        hs = self.hs_system.scores[0]["score"] if self.hs_system.scores else 0
        hs_label = ServiceLocator.texts_service.render(font_path, 7, "BEST", white)
        hs_val = ServiceLocator.texts_service.render(font_path, 8, f"{hs:06}", (80, 160, 255))

        prompt = ServiceLocator.texts_service.render(font_path, 7, "PRESS ENTER", white)

        surface.blit(title,      title.get_rect(center=(160, 80)))
        if reason.get_width() > 0:
            surface.blit(reason, reason.get_rect(center=(160, 104)))
        surface.blit(score_label, score_label.get_rect(center=(160, 124)))
        surface.blit(score_val,   score_val.get_rect(center=(160, 140)))
        surface.blit(hs_label,    hs_label.get_rect(center=(160, 162)))
        surface.blit(hs_val,      hs_val.get_rect(center=(160, 176)))
        if int(elapsed * 2) % 2 == 0:
            surface.blit(prompt,  prompt.get_rect(center=(160, 204)))
