from __future__ import annotations

import pygame

from src.components.player import Player
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_laser


class ShootingSystem:
    def __init__(self) -> None:
        self.player_cfg = ServiceLocator.config.get("player")
        self.audio_cfg = ServiceLocator.config.get("audio")
        self.cooldown = 0.0
        self.next_fire_time_ms = 0

    def update(self, dt: float) -> None:
        self.cooldown = max(0.0, self.cooldown - dt)

    def fire(self, world) -> None:
        now = pygame.time.get_ticks()
        if self.cooldown > 0 or now < self.next_fire_time_ms:
            return
        for _, (transform, velocity, player) in world.get_components(Transform, Velocity, Player):
            offset = pygame.Vector2(6 * player.facing, 0)
            create_laser(world, transform.position + offset, player.facing, velocity.value.x)
            ServiceLocator.sounds_service.play(self.audio_cfg["sounds"]["player_shoot"])

            player.is_shooting = True
            self.cooldown = self.player_cfg["fire_cooldown"]
            self.next_fire_time_ms = now + int(self.player_cfg["fire_cooldown"] * 1000)
            break
