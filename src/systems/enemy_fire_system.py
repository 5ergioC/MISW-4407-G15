from __future__ import annotations

import random

import pygame

from src.components.camera import Camera
from src.components.enemy import Enemy
from src.components.player import Player
from src.components.renderable import Renderable
from src.components.tag import Tag
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_enemy_bullet


SHOOTING_KINDS = {"lander", "mutant", "bomber", "baiter", "swarmer"}


class EnemyFireSystem:
    def __init__(self) -> None:
        self.enemies_cfg = ServiceLocator.config.get("enemies")
        self.audio_cfg = ServiceLocator.config.get("audio")
        self.cooldowns: dict[int, float] = {}
        self.rng = random.Random()
        self.enabled: bool = True

    def update(self, world, dt: float, camera: Camera) -> None:
        if not self.enabled:
            return

        player_data = list(world.get_components(Transform, Player))
        if not player_data:
            self.cooldowns.clear()
            return

        _, (player_transform, _) = player_data[0]
        player_position = player_transform.position.copy()

        live_entities: set[int] = set()
        for enemy_entity, (enemy_transform, enemy_velocity, enemy, enemy_renderable, enemy_tag) in world.get_components(Transform, Velocity, Enemy, Renderable, Tag):
            if not enemy_tag.has("enemy") or enemy.kind not in SHOOTING_KINDS:
                continue
            live_entities.add(enemy_entity)

            cooldown = self.cooldowns.get(enemy_entity, self._random_fire_cooldown(enemy.kind))
            cooldown = max(0.0, cooldown - dt)
            self.cooldowns[enemy_entity] = cooldown
            if cooldown > 0.0:
                continue
            if not self._is_on_screen(enemy_transform, enemy_renderable, camera):
                continue

            direction = player_position - enemy_transform.position
            if direction.length_squared() <= 0.01:
                direction = pygame.Vector2(1, 0)

            bullet_speed = float(self.enemies_cfg["bullet"]["speed"])
            bullet_offset = self._bullet_spawn_offset(direction)
            create_enemy_bullet(
                world,
                enemy_transform.position + bullet_offset,
                direction,
                bullet_speed,
                enemy_velocity.value,
            )
            enemy_shoot_sound = self.audio_cfg["sounds"].get("enemy_shoot")
            if enemy_shoot_sound:
                ServiceLocator.sounds_service.play(enemy_shoot_sound)
            self.cooldowns[enemy_entity] = self._random_fire_cooldown(enemy.kind)

        self.cooldowns = {entity: remaining for entity, remaining in self.cooldowns.items() if entity in live_entities}

    def _random_fire_cooldown(self, enemy_kind: str) -> float:
        enemy_cfg = self.enemies_cfg[enemy_kind]
        minimum = float(enemy_cfg.get("fire_cooldown_min", 1.0))
        maximum = float(enemy_cfg.get("fire_cooldown_max", minimum))
        if maximum < minimum:
            maximum = minimum
        return self.rng.uniform(minimum, maximum)

    def _bullet_spawn_offset(self, direction: pygame.Vector2) -> pygame.Vector2:
        direction = direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(1, 0)
        return direction * 12

    def _is_on_screen(self, transform: Transform, renderable: Renderable, camera: Camera) -> bool:
        rect = pygame.Rect(
            round(transform.position.x),
            round(transform.position.y),
            round(renderable.size.x),
            round(renderable.size.y),
        )
        if renderable.centered:
            rect.center = (round(transform.position.x), round(transform.position.y))
        screen_x = (rect.x - camera.x + camera.world_width / 2) % camera.world_width - camera.world_width / 2
        screen_rect = pygame.Rect(round(screen_x), rect.y - round(camera.y), rect.width, rect.height)
        viewport = pygame.Rect(0, 0, round(camera.width), round(camera.height))
        return screen_rect.colliderect(viewport)