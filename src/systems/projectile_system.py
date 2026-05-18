from __future__ import annotations

import pygame

from src.components.player import Player
from src.components.projectile import Projectile
from src.components.transform import Transform
from src.components.velocity import Velocity


class ProjectileSystem:
    def update(self, world, dt: float) -> None:
        player_position = None
        for _, (transform, _) in world.get_components(Transform, Player):
            player_position = transform.position.copy()
            break

        if player_position is None:
            return

        for _, (transform, velocity, projectile) in world.get_components(Transform, Velocity, Projectile):
            if projectile.owner != "enemy" or projectile.kind != "missile":
                continue

            offset = player_position - transform.position
            if offset.length_squared() <= 0.01:
                continue

            desired_velocity = offset.normalize() * projectile.speed
            velocity.value = velocity.value.lerp(desired_velocity, min(0.8, dt * 1.6))
            projectile.direction = velocity.value.normalize() if velocity.value.length_squared() > 0.01 else projectile.direction
