from __future__ import annotations

import math
import random

import pygame

from src.commands.scene_command import SceneCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.systems.input_command_system import InputCommandSystem


class WinScene(Scene):
    def enter(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.audio_cfg = ServiceLocator.config.get("audio")
        self.background = self.engine.virtual_screen.copy()
        self.elapsed = 0.0
        self.fireworks: list[dict[str, object]] = []
        self.spawn_timer = 0.0
        self.rng = random.Random(1337)
        ServiceLocator.sounds_service.play(self.audio_cfg["sounds"]["game_win"])
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
        self.spawn_timer -= dt
        if self.spawn_timer <= 0.0:
            self._spawn_firework()
            self.spawn_timer = self.rng.uniform(0.35, 0.8)

        active_fireworks: list[dict[str, object]] = []
        for firework in self.fireworks:
            firework["age"] = float(firework["age"]) + dt
            if float(firework["age"]) >= float(firework["lifetime"]):
                continue
            position = firework["position"]
            velocity = firework["velocity"]
            position.x += velocity.x * dt
            position.y += velocity.y * dt
            velocity.y += 140.0 * dt
            active_fireworks.append(firework)
        self.fireworks = active_fireworks

    def render(self) -> None:
        surface = self.virtual_screen
        surface.blit(self.background, (0, 0))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((6, 8, 18, 92))
        surface.blit(overlay, (0, 0))
        self._draw_fireworks(surface)
        font_path = self.interface_cfg["font"]["path"]
        high_score_color = self.interface_cfg["high_score_color"]
        normal_color = self.interface_cfg["normal_text_color"]
        title = ServiceLocator.texts_service.render(
            font_path, 12, "LEVEL COMPLETE", (high_score_color["r"], high_score_color["g"], high_score_color["b"])
        )
        prompt = ServiceLocator.texts_service.render(font_path, 8, "Press ENTER to return", (normal_color["r"], normal_color["g"], normal_color["b"]))
        surface.blit(title, title.get_rect(center=(160, 104)))
        if int(self.elapsed * 2.0) % 2 == 0:
            surface.blit(prompt, prompt.get_rect(center=(160, 144)))

    def _spawn_firework(self) -> None:
        x = self.rng.randint(30, 290)
        y = self.rng.randint(25, 110)
        palette = [
            pygame.Color(255, 90, 90),
            pygame.Color(255, 190, 70),
            pygame.Color(120, 220, 255),
            pygame.Color(180, 120, 255),
            pygame.Color(120, 255, 170),
        ]
        color = self.rng.choice(palette)
        particle_count = self.rng.randint(18, 28)
        for index in range(particle_count):
            angle = (math.tau * index / particle_count) + self.rng.uniform(-0.2, 0.2)
            speed = self.rng.uniform(60.0, 130.0)
            self.fireworks.append(
                {
                    "position": pygame.Vector2(x, y),
                    "velocity": pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed),
                    "age": 0.0,
                    "lifetime": self.rng.uniform(0.7, 1.1),
                    "color": color,
                    "size": self.rng.choice([1, 1, 2]),
                }
            )

    def _draw_fireworks(self, surface: pygame.Surface) -> None:
        for firework in self.fireworks:
            age = float(firework["age"])
            lifetime = float(firework["lifetime"])
            progress = min(1.0, age / lifetime)
            alpha = max(0, int(255 * (1.0 - progress)))
            color = firework["color"]
            size = int(firework["size"])
            position = firework["position"]
            radius = max(1, size)
            sparkle = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(sparkle, (*color[:3], alpha), (radius + 1, radius + 1), radius)
            surface.blit(sparkle, (round(position.x) - radius - 1, round(position.y) - radius - 1))
