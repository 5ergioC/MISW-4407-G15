from __future__ import annotations

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.systems.input_command_system import InputCommandSystem


class WinScene(Scene):
    def enter(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.input_system = InputCommandSystem(
            {
                pygame.K_RETURN: SceneCommand(lambda: self.switch_to("menu")),
                pygame.K_ESCAPE: SceneCommand(lambda: self.switch_to("menu")),
            }
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        self.input_system.process_event(self.world, event)

    def update(self, dt: float) -> None:
        del dt

    def render(self) -> None:
        surface = self.virtual_screen
        font_path = self.interface_cfg["font"]["path"]
        high_score_color = self.interface_cfg["high_score_color"]
        normal_color = self.interface_cfg["normal_text_color"]
        title = ServiceLocator.texts_service.render(
            font_path, 12, "LEVEL COMPLETE", (high_score_color["r"], high_score_color["g"], high_score_color["b"])
        )
        prompt = ServiceLocator.texts_service.render(
            font_path, 8, "Press ENTER to return", (normal_color["r"], normal_color["g"], normal_color["b"])
        )
        surface.blit(title, title.get_rect(center=(160, 104)))
        surface.blit(prompt, prompt.get_rect(center=(160, 144)))
