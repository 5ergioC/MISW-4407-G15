from __future__ import annotations

import pygame

from src.components.player import Player
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.components.renderable import Renderable
from src.components.collider import Collider
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
        for ent, (transform, velocity, player) in world.get_components(Transform, Velocity, Player):
            laser_width = 40
            laser_height = 1
            spawn_pos = transform.position.copy()
            try:
                collider = world.component_for_entity(ent, Collider)
                renderable = world.component_for_entity(ent, Renderable)
                pw = float(renderable.size.x)

                center_offset = player.facing * (pw / 2.0 + laser_width / 2.0)
                spawn_pos = pygame.Vector2(transform.position.x + center_offset, transform.position.y)
            except Exception:

                offset = pygame.Vector2(6 * player.facing, 0)
                spawn_pos = transform.position + offset

            create_laser(world, spawn_pos, player.facing, velocity.value.x)
            ServiceLocator.sounds_service.play(self.audio_cfg["sounds"]["player_shoot"])

            player.is_shooting = True
            self.cooldown = self.player_cfg["fire_cooldown"]
            self.next_fire_time_ms = now + int(self.player_cfg["fire_cooldown"] * 1000)
            break
