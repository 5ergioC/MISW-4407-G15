from __future__ import annotations

import math

from src.components.player import Player
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.components.velocity import Velocity

_BURNER_IDLE_OFFSET_X = 6
_BURNER_MOVE_OFFSET_X = 9
_BURNER_IDLE_FRAME_W = 8
_BURNER_MOVE_FRAME_W = 13
_BURNER_FRAME_TIME = 0.08


import pygame


class PlayerMovementSystem:
    def _sync_burner(self, world, player, player_transform, dt: float, velocity=None) -> None:
        bid = player.burner_entity
        if bid < 0:
            return
        if not world.has_component(bid, Transform) or not world.has_component(bid, Renderable):
            return
        burner_r = world.component_for_entity(bid, Renderable)
        burner_t = world.component_for_entity(bid, Transform)

        offset = _BURNER_IDLE_OFFSET_X if not player.is_thrusting else _BURNER_MOVE_OFFSET_X
        offset_x = -offset * player.facing
        burner_t.position = pygame.Vector2(
            player_transform.position.x + offset_x,
            player_transform.position.y,
        )
        burner_r.flip_x = player.facing < 0

        # hide burner if player is dead/invisible
        if world.has_component(player.burner_entity, Renderable):
            pass  # already got burner_r above
        player_entity_renderable = None
        for ent, (pl,) in world.get_components(Player):
            if pl is player and world.has_component(ent, Renderable):
                player_entity_renderable = world.component_for_entity(ent, Renderable)
                break
        if player_entity_renderable is not None and not player_entity_renderable.visible:
            burner_r.visible = False
            return

        speed_sq = velocity.length_squared() if velocity is not None else 0.0
        moving = speed_sq > 4.0 or player.is_thrusting

        if not moving:
            burner_r.visible = False
            return

        burner_r.visible = True
        if player.is_thrusting:
            burner_r.image_path = "img/player_burner_moving.png"
            burner_r.sprite_frame_width = _BURNER_MOVE_FRAME_W
        else:
            burner_r.image_path = "img/player_burner_idle.png"
            burner_r.sprite_frame_width = _BURNER_IDLE_FRAME_W

        player.burner_timer += dt
        if player.burner_timer >= _BURNER_FRAME_TIME:
            player.burner_timer = 0.0
            player.burner_frame = (player.burner_frame + 1) % 3
        burner_r.sprite_frame = player.burner_frame

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
            thrusting = player.thrust_input.length_squared() > 0.01
            player.is_thrusting = thrusting
            if math.fabs(velocity.value.x) > 0.01:
                player.facing = 1.0 if velocity.value.x >= 0 else -1.0
            if world.has_component(entity, Renderable):
                world.component_for_entity(entity, Renderable).flip_x = player.facing < 0
            self._sync_burner(world, player, transform, dt, velocity.value)
