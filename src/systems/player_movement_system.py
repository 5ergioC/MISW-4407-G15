from __future__ import annotations

import math

from src.components.player import Player
from src.components.transform import Transform
from src.components.velocity import Velocity


class PlayerMovementSystem:
    def update(self, world, dt: float) -> None:
        for _, (transform, velocity, player) in world.get_components(Transform, Velocity, Player):
            velocity.value += player.thrust_input * player.thrust * dt
            velocity.value *= player.drag
            if velocity.value.length_squared() > player.max_speed * player.max_speed:
                velocity.value.scale_to_length(player.max_speed)
            transform.position += velocity.value * dt
            if math.fabs(velocity.value.x) > 0.01:
                player.facing = 1.0 if velocity.value.x >= 0 else -1.0
