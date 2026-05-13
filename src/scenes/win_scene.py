from __future__ import annotations

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.systems.input_command_system import InputCommandSystem


class WinScene(Scene):
    def enter(self) -> None:
        self.title_font = pygame.font.Font(None, 36)
        self.body_font = pygame.font.Font(None, 18)
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
        title = self.title_font.render("LEVEL COMPLETE", True, pygame.Color(120, 255, 180))
        prompt = self.body_font.render("Press ENTER to return", True, pygame.Color("white"))
        surface.blit(title, title.get_rect(center=(160, 104)))
        surface.blit(prompt, prompt.get_rect(center=(160, 144)))
