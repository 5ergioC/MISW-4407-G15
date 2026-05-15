from __future__ import annotations

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.systems.input_command_system import InputCommandSystem


class GameOverScene(Scene):
    def enter(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.background = self.engine.virtual_screen.copy()
        self.elapsed = 0.0
        self.input_system = InputCommandSystem(
            {
                pygame.K_RETURN: SceneCommand(lambda: self.switch_to("menu")),
                pygame.K_ESCAPE: SceneCommand(lambda: self.switch_to("menu")),
            }
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        self.input_system.process_event(self.world, event)

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def render(self) -> None:
        surface = self.virtual_screen
        surface.blit(self.background, (0, 0))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((12, 6, 6, 104))
        surface.blit(overlay, (0, 0))
        font_path = self.interface_cfg["font"]["path"]
        pause_color = self.interface_cfg["pause_text_color"]
        normal_color = self.interface_cfg["normal_text_color"]
        title = ServiceLocator.texts_service.render(
            font_path, 16, "GAME OVER", (pause_color["r"], pause_color["g"], pause_color["b"])
        )
        reason = ServiceLocator.texts_service.render(
            font_path,
            8,
            str(self.engine.shared_state.get("game_over_reason", "Try again")),
            (normal_color["r"], normal_color["g"], normal_color["b"]),
        )
        prompt = ServiceLocator.texts_service.render(
            font_path, 8, "Press RETURN to return", (normal_color["r"], normal_color["g"], normal_color["b"])
        )
        surface.blit(title, title.get_rect(center=(160, 96)))
        surface.blit(reason, reason.get_rect(center=(160, 118)))
        if int(self.elapsed * 2.0) % 2 == 0:
            surface.blit(prompt, prompt.get_rect(center=(160, 154)))
