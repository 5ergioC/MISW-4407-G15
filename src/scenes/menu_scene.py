from __future__ import annotations

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.systems.input_command_system import InputCommandSystem


class MenuScene(Scene):
    def enter(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.logo_surface = ServiceLocator.images_service.get("img/game_logo.png")
        self.input_system = InputCommandSystem(
            {
                pygame.K_RETURN: SceneCommand(self._start_game),
                pygame.K_SPACE: SceneCommand(self._start_game),
            }
        )

    def _start_game(self) -> None:
        self.engine.reset_run_state()
        self.switch_to("play")

    def handle_event(self, event: pygame.event.Event) -> None:
        self.input_system.process_event(self.world, event)

    def update(self, dt: float) -> None:
        del dt

    def render(self) -> None:
        surface = self.virtual_screen
        title_color = self.interface_cfg["title_text_color"]
        normal_color = self.interface_cfg["normal_text_color"]
        font_path = self.interface_cfg["font"]["path"]
        title = ServiceLocator.texts_service.render(
            font_path, 20, "DEFENDER CLONE", (title_color["r"], title_color["g"], title_color["b"])
        )
        subtitle = ServiceLocator.texts_service.render(
            font_path, 10, "Press ENTER to start", (normal_color["r"], normal_color["g"], normal_color["b"])
        )
        help_one = ServiceLocator.texts_service.render(
            font_path, 8, "Arrows move, SPACE fires, P pauses", (normal_color["r"], normal_color["g"], normal_color["b"])
        )
        help_two = ServiceLocator.texts_service.render(
            font_path, 8, "ECS architecture with engine services", (normal_color["r"], normal_color["g"], normal_color["b"])
        )
        logo_rect = self.logo_surface.get_rect(center=(160, 72))
        surface.blit(self.logo_surface, logo_rect)
        surface.blit(title, title.get_rect(center=(160, 128)))
        surface.blit(subtitle, subtitle.get_rect(center=(160, 154)))
        surface.blit(help_one, help_one.get_rect(center=(160, 184)))
        surface.blit(help_two, help_two.get_rect(center=(160, 204)))
