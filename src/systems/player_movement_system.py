from __future__ import annotations

import math

from src.components.player import Player
from src.engine.service_locator import ServiceLocator
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.components.velocity import Velocity


class PlayerMovementSystem:
    def update(self, world, dt: float) -> None:
        for entity, (transform, velocity, player) in world.get_components(Transform, Velocity, Player):

            thrust_vec = player.thrust_input
            if thrust_vec.length_squared() > 0.0:
                dot = velocity.value.x * thrust_vec.x + velocity.value.y * thrust_vec.y
                if dot < 0.0:
                    accel_factor = 0.3
                else:
                    accel_factor = 1.0
                velocity.value += thrust_vec * player.thrust * dt * accel_factor

            if player.thrust_input.length_squared() > 0.0:
                effective_drag = player.drag
            else:
                effective_drag = min(player.drag + 0.03, 0.99)

            velocity.value *= effective_drag ** (dt * 60.0)
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
                renderable = world.component_for_entity(entity, Renderable)
                renderable.flip_x = player.facing < 0
                
                if player.thrust_input.length_squared() > 0.0:
                    player.thrust_anim_timer += dt
                    frame_time = 0.08
                    if player.thrust_anim_timer >= frame_time:
                        player.thrust_anim_timer -= frame_time
                        player.thrust_anim_frame = (player.thrust_anim_frame + 1) % 3
                else:
                    player.thrust_anim_timer = 0.0
                    player.thrust_anim_frame = 0
