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
from src.factories.entity_factory import create_enemy_bullet, create_enemy_missile


SHOOTING_KINDS = {"lander", "mutant", "bomber", "baiter", "swarmer"}


class EnemyFireSystem:
    def __init__(self) -> None:
        self.enemies_cfg = ServiceLocator.config.get("enemies")
        self.audio_cfg = ServiceLocator.config.get("audio")
        self.world_cfg = ServiceLocator.config.get("world")
        self.cooldowns: dict[int, float] = {}
        self.rng = random.Random()
        self.enabled: bool = True
        self.mute_fire_sound: bool = False
        self.wave_fire_rate: float = 1.0
        self.wave_missile_chance: float = 0.0

    def set_wave_context(self, wave: dict | None) -> None:
        if not wave:
            self.wave_fire_rate = 1.0
            self.wave_missile_chance = 0.0
            return
        self.wave_fire_rate = max(0.2, float(wave.get("enemy_fire_rate", 1.0)))
        self.wave_missile_chance = max(0.0, float(wave.get("missile_chance", 0.0)))

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

            direction = pygame.Vector2(
                self._wrapped_dx(enemy_transform.position.x, player_position.x),
                player_position.y - enemy_transform.position.y,
            )
            if direction.length_squared() <= 0.01:
                direction = pygame.Vector2(1, 0)

            use_missile = enemy.kind in {"lander", "mutant"} and self.rng.random() < self._missile_chance()
            bullet_offset = self._bullet_spawn_offset(direction)
            if use_missile:
                missile_speed = float(self.enemies_cfg["missile"]["speed"])
                create_enemy_missile(
                    world,
                    enemy_transform.position + bullet_offset,
                    direction,
                    missile_speed,
                    enemy_velocity.value,
                    source_kind=enemy.kind,
                )
            else:
                bullet_speed = float(self.enemies_cfg["bullet"]["speed"])
                create_enemy_bullet(
                    world,
                    enemy_transform.position + bullet_offset,
                    direction,
                    bullet_speed,
                    enemy_velocity.value,
                )
            enemy_shoot_sound = self.audio_cfg["sounds"].get("enemy_shoot")
            if enemy_shoot_sound and not self.mute_fire_sound:
                ServiceLocator.sounds_service.play(enemy_shoot_sound)
            self.cooldowns[enemy_entity] = self._random_fire_cooldown(enemy.kind)

        self.cooldowns = {entity: remaining for entity, remaining in self.cooldowns.items() if entity in live_entities}

    def _random_fire_cooldown(self, enemy_kind: str) -> float:
        enemy_cfg = self.enemies_cfg[enemy_kind]
        minimum = float(enemy_cfg.get("fire_cooldown_min", 1.0))
        maximum = float(enemy_cfg.get("fire_cooldown_max", minimum))
        if maximum < minimum:
            maximum = minimum
        cooldown = self.rng.uniform(minimum, maximum)
        return cooldown / self.wave_fire_rate

    def _missile_chance(self) -> float:
        missile_cfg = self.enemies_cfg.get("missile", {})
        multiplier = float(missile_cfg.get("chance_multiplier", 0.35))
        return min(0.95, self.wave_missile_chance * multiplier)

    def _bullet_spawn_offset(self, direction: pygame.Vector2) -> pygame.Vector2:
        direction = direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(1, 0)
        return direction * 12

    def _wrapped_dx(self, source_x: float, target_x: float) -> float:
        world_width = float(self.world_cfg.get("width", 2048))
        return (target_x - source_x + world_width / 2) % world_width - world_width / 2

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
