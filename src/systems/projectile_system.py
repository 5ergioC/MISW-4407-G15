from __future__ import annotations

import pygame

from src.components.player import Player
from src.components.projectile import Projectile
from src.components.transform import Transform
from src.components.velocity import Velocity


class ProjectileSystem:
    def update(self, world, dt: float) -> None:
        player_position = None
        world_width = None
        for _, (transform, _) in world.get_components(Transform, Player):
            player_position = transform.position.copy()
            break
        if player_position is not None:
            from src.engine.service_locator import ServiceLocator
            world_width = float(ServiceLocator.config.get("world")["width"])

        if player_position is None:
            return

        for _, (transform, velocity, projectile) in world.get_components(Transform, Velocity, Projectile):
            if projectile.owner != "enemy" or projectile.kind != "missile":
                continue

            offset = pygame.Vector2(
                self._wrapped_dx(transform.position.x, player_position.x, world_width),
                player_position.y - transform.position.y,
            )
            if offset.length_squared() <= 0.01:
                continue

            desired_velocity = offset.normalize() * projectile.speed
            velocity.value = velocity.value.lerp(desired_velocity, min(0.8, dt * 1.6))
            projectile.direction = velocity.value.normalize() if velocity.value.length_squared() > 0.01 else projectile.direction

    def _wrapped_dx(self, source_x: float, target_x: float, world_width: float) -> float:
        return (target_x - source_x + world_width / 2) % world_width - world_width / 2
