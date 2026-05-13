from __future__ import annotations

import pygame

from src.components.player import Player
from src.components.transform import Transform
from src.core.service_locator import ServiceLocator
from src.factories.entity_factory import create_laser


class ShootingSystem:
    def __init__(self) -> None:
        self.player_cfg = ServiceLocator.config.get("player")
        self.cooldown = 0.0

    def update(self, dt: float) -> None:
        self.cooldown = max(0.0, self.cooldown - dt)

    def fire(self, world) -> None:
        if self.cooldown > 0:
            return
        for _, (transform, player) in world.get_components(Transform, Player):
            offset = pygame.Vector2(8 * player.facing, 0)
            create_laser(world, transform.position + offset, player.facing)
            self.cooldown = self.player_cfg["fire_cooldown"]
            break
