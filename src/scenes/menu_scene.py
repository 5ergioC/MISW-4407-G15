from __future__ import annotations

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.systems.input_command_system import InputCommandSystem


class MenuScene(Scene):
    def enter(self) -> None:
        self.title_font = pygame.font.Font(None, 36)
        self.body_font = pygame.font.Font(None, 18)
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
        title = self.title_font.render("DEFENDER CLONE", True, pygame.Color(120, 255, 240))
        subtitle = self.body_font.render("Press ENTER to start", True, pygame.Color("white"))
        help_one = self.body_font.render("Arrows move, SPACE fires, P pauses", True, pygame.Color("white"))
        help_two = self.body_font.render("This base is ready for ECS gameplay systems", True, pygame.Color(180, 190, 220))
        surface.blit(title, title.get_rect(center=(160, 92)))
        surface.blit(subtitle, subtitle.get_rect(center=(160, 128)))
        surface.blit(help_one, help_one.get_rect(center=(160, 156)))
        surface.blit(help_two, help_two.get_rect(center=(160, 182)))
