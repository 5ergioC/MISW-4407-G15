from __future__ import annotations

import math
import random

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.systems.input_command_system import InputCommandSystem


class MenuScene(Scene):
    def enter(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.window_cfg = ServiceLocator.config.get("window")
        self.logo_surface = ServiceLocator.images_service.get("img/game_logo.png")
        self.elapsed = 0.0
        self._rng = random.Random(1981)
        self._stars = self._create_menu_stars()
        self._terrain = self._create_menu_terrain()
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
        self.elapsed += dt

    def render(self) -> None:
        surface = self.virtual_screen
        surface.fill((0, 0, 0))
        self._render_stars(surface)
        self._render_terrain(surface)
        self._render_scanner_frame(surface)
        self._render_title(surface)
        self._render_prompts(surface)

    def _create_menu_stars(self) -> list[tuple[float, float, pygame.Color, float]]:
        colors = [
            pygame.Color(255, 85, 52),
            pygame.Color(255, 197, 67),
            pygame.Color(246, 245, 89),
            pygame.Color(78, 202, 74),
            pygame.Color(210, 210, 210),
        ]
        return [
            (
                self._rng.uniform(0, 320),
                self._rng.uniform(44, 210),
                self._rng.choice(colors),
                self._rng.uniform(3.0, 13.0),
            )
            for _ in range(34)
        ]

    def _create_menu_terrain(self) -> list[tuple[int, int]]:
        points: list[tuple[int, int]] = []
        y = 232
        for x in range(0, 324, 4):
            if x < 64:
                y -= self._rng.choice((0, 1, 2, 3))
            elif 64 <= x < 104:
                y += self._rng.choice((-2, -1, 0, 1, 2))
            elif 104 <= x < 204:
                y += self._rng.choice((0, 0, 1))
            elif 204 <= x < 268:
                y -= self._rng.choice((0, 1, 2))
            else:
                y += self._rng.choice((-1, 0, 1, 2))
            y = max(206, min(248, y))
            points.append((x, y))
        return points

    def _render_stars(self, surface: pygame.Surface) -> None:
        for x, y, color, speed in self._stars:
            screen_x = (x - self.elapsed * speed) % 320
            blink = 0.55 + 0.45 * math.sin(self.elapsed * 3.0 + x)
            star_color = (
                int(color.r * blink),
                int(color.g * blink),
                int(color.b * blink),
            )
            surface.fill(star_color, pygame.Rect(round(screen_x), round(y), 1, 1))

    def _render_terrain(self, surface: pygame.Surface) -> None:
        orange = pygame.Color(205, 106, 42)
        offset = -int(self.elapsed * 10) % 4
        shifted = [(x + offset, y) for x, y in self._terrain]
        for index in range(len(shifted) - 1):
            pygame.draw.line(surface, orange, shifted[index], shifted[index + 1], 1)

    def _render_scanner_frame(self, surface: pygame.Surface) -> None:
        green = pygame.Color(52, 174, 45)
        pygame.draw.line(surface, green, (0, 42), (320, 42), 2)
        pygame.draw.rect(surface, green, pygame.Rect(88, 1, 146, 40), 2)
        pygame.draw.rect(surface, green, pygame.Rect(234, 1, 86, 40), 2)
        mini_terrain = [(92 + index * 4, 34 + math.sin(index * 0.7) * 3) for index in range(34)]
        pygame.draw.lines(surface, pygame.Color(205, 106, 42), False, mini_terrain, 1)

    def _render_title(self, surface: pygame.Surface) -> None:
        font_path = self.interface_cfg["font"]["path"]
        title_phase = int(self.elapsed * 8) % 6
        title_color = [
            (255, 40, 40),
            (255, 197, 67),
            (246, 245, 89),
            (78, 202, 74),
            (80, 160, 255),
            (255, 80, 230),
        ][title_phase]
        logo_rect = self.logo_surface.get_rect(center=(160, 73))
        surface.blit(self.logo_surface, logo_rect)
        title = ServiceLocator.texts_service.render(
            font_path,
            18,
            "DEFENDER",
            title_color,
        )
        surface.blit(title, title.get_rect(center=(160, 112)))

    def _render_prompts(self, surface: pygame.Surface) -> None:
        font_path = self.interface_cfg["font"]["path"]
        yellow = (255, 244, 72)
        white = (245, 245, 245)
        cyan = (80, 210, 255)
        if int(self.elapsed * 2) % 2 == 0:
            start = ServiceLocator.texts_service.render(font_path, 9, "PRESS ENTER", yellow)
            surface.blit(start, start.get_rect(center=(160, 142)))
        controls = ServiceLocator.texts_service.render(
            font_path,
            7,
            "ARROWS/WASD   SPACE FIRE   P PAUSE",
            white,
        )
        goal = ServiceLocator.texts_service.render(font_path, 7, "RESCUE HUMANOIDS - DESTROY LANDERS", cyan)
        credit = ServiceLocator.texts_service.render(font_path, 7, "1 PLAYER   3 SHIPS", yellow)
        surface.blit(controls, controls.get_rect(center=(160, 168)))
        surface.blit(goal, goal.get_rect(center=(160, 184)))
        surface.blit(credit, credit.get_rect(center=(160, 202)))
