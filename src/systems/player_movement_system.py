from __future__ import annotations

import math

from src.components.player import Player
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.components.velocity import Velocity


class PlayerMovementSystem:
    def update(self, world, dt: float) -> None:
        for entity, (transform, velocity, player) in world.get_components(Transform, Velocity, Player):
            velocity.value += player.thrust_input * player.thrust * dt
            velocity.value *= player.drag ** (dt * 60.0)
            velocity.value.x = max(-player.max_speed_x, min(player.max_speed_x, velocity.value.x))
            velocity.value.y = max(-player.max_speed_y, min(player.max_speed_y, velocity.value.y))
            if velocity.value.length_squared() > player.max_speed * player.max_speed:
                velocity.value.scale_to_length(player.max_speed)
            transform.position += velocity.value * dt
            if transform.position.y < player.vertical_min:
                transform.position.y = player.vertical_min
                velocity.value.y = max(0.0, velocity.value.y)
            elif transform.position.y > player.vertical_max:
                transform.position.y = player.vertical_max
                velocity.value.y = min(0.0, velocity.value.y)
            if math.fabs(velocity.value.x) > 0.01:
                player.facing = 1.0 if velocity.value.x >= 0 else -1.0
            if world.has_component(entity, Renderable):
                world.component_for_entity(entity, Renderable).flip_x = player.facing < 0
