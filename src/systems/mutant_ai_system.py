from __future__ import annotations

import pygame

from src.components.enemy import Enemy
from src.components.player import Player
from src.components.state import State
from src.components.tag import Tag
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator


class MutantAISystem:
    def __init__(self) -> None:
        self.enemies_cfg = ServiceLocator.config.get("enemies")

    def update(self, world, dt: float) -> None:
        player_position = None
        for _, (transform, _) in world.get_components(Transform, Player):
            player_position = transform.position.copy()
            break

        if player_position is None:
            return

        mutant_cfg = self.enemies_cfg["mutant"]
        base_speed = float(mutant_cfg.get("speed", 70.0))
        chase_acceleration = float(mutant_cfg.get("chase_acceleration", 100.0))
        vertical_factor = float(mutant_cfg.get("vertical_chase_factor", 0.35))

        for _, (transform, velocity, enemy, state, tag) in world.get_components(Transform, Velocity, Enemy, State, Tag):
            if enemy.kind != "mutant" or not tag.has("enemy"):
                continue

            offset = player_position - transform.position
            if offset.length_squared() <= 1.0:
                continue

            direction = offset.normalize()
            velocity.value.x += direction.x * chase_acceleration * dt
            velocity.value.y += direction.y * chase_acceleration * vertical_factor * dt

            velocity.value.x = max(-base_speed, min(base_speed, velocity.value.x))
            velocity.value.y = max(-base_speed * vertical_factor, min(base_speed * vertical_factor, velocity.value.y))

            state.name = "chase" if abs(offset.x) > 24.0 else "attack_player"
            state.elapsed += dt
            enemy.state = state.name
