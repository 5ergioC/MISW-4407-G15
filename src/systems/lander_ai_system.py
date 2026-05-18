from __future__ import annotations

import random

import pygame

from src.components.astronaut import Astronaut
from src.components.enemy import Enemy
from src.components.state import State
from src.components.tag import Tag
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator


class LanderAISystem:
    def __init__(self) -> None:
        self.enemies_cfg = ServiceLocator.config.get("enemies")
        self.world_cfg = ServiceLocator.config.get("world")
        self.rng = random.Random()
        self.last_positions: dict[int, pygame.Vector2] = {}
        self.stuck_timers: dict[int, float] = {}

    def update(self, world, dt: float) -> None:
        if dt <= 0:
            return

        players = list(world.get_components(Transform, Tag))
        player_pos = None
        for _, (t, tag) in players:
            if tag.has("player"):
                player_pos = t.position.copy()
                break

        astronauts: dict[int, pygame.Vector2] = {}
        for ent, (t, astro, tag) in world.get_components(Transform, Astronaut, Tag):
            if tag.has("astronaut") and astro.state == "walking":
                astronauts[ent] = t.position.copy()

        live_entities: set[int] = set()
        for ent, (t, v, enemy, state, tag) in world.get_components(Transform, Velocity, Enemy, State, Tag):
            if enemy.kind != "lander" or not tag.has("enemy"):
                continue
            live_entities.add(ent)

            cfg = self.enemies_cfg.get("lander", {})
            patrol_speed = float(cfg.get("speed", 40.0))
            vertical_speed = float(cfg.get("vertical_speed", 30.0))
            seek_radius = float(cfg.get("seek_radius", 90.0))
            capture_distance = float(cfg.get("capture_distance", 18.0))
            state.elapsed += dt

            current = state.name
            player_visible = False
            if player_pos is not None:
                dx = abs(self._wrapped_dx(t.position.x, player_pos.x))
                if dx <= self.world_cfg.get("width", 2048) / 2:
                    player_visible = True

            if current in ("abducting", "ascending"):
                self.last_positions[ent] = t.position.copy()
                self.stuck_timers[ent] = 0.0
                continue

            target_position = astronauts.get(enemy.target_entity) if enemy.target_entity is not None else None
            if target_position is None:
                enemy.target_entity = self._choose_target_entity(t.position, astronauts, seek_radius * 1.6)
                if enemy.target_entity is not None:
                    target_position = astronauts[enemy.target_entity]
                    self._change_state(state, enemy, "seek_astronaut")

            if target_position is not None:
                offset = self._wrapped_offset(t.position, target_position)
                if offset.length() <= capture_distance:
                    v.value.update(0.0, 0.0)
                    self._change_state(state, enemy, "abducting")
                    enemy.alerting = True
                    continue

                v.value.x = self._signed_speed(offset.x, patrol_speed)
                if abs(offset.y) > 4.0:
                    v.value.y = self._signed_speed(offset.y, vertical_speed)
                else:
                    v.value.y = 0.0
                self._change_state(state, enemy, "seek_astronaut")
                continue

            if player_visible and self.rng.random() < min(0.45 * dt, 0.08):
                self._change_state(state, enemy, "attack_player")
                v.value.x = self._signed_speed(self._wrapped_dx(t.position.x, player_pos.x), patrol_speed)
                v.value.y = 0.0
                continue

            if state.name == "attack_player" and player_visible:
                v.value.x = self._signed_speed(self._wrapped_dx(t.position.x, player_pos.x), patrol_speed)
                v.value.y = 0.0
                if state.elapsed < 0.8:
                    continue

            if abs(v.value.x) < 1.0 or state.elapsed > 1.8:
                v.value.x = self.rng.choice((-1.0, 1.0)) * patrol_speed
                if self.rng.random() < 0.4:
                    v.value.y = self.rng.choice((-1.0, 1.0)) * vertical_speed * 0.4
                else:
                    v.value.y = 0.0
                self._change_state(state, enemy, "patrol")

            self._recover_if_stuck(ent, t.position, v, enemy, state, patrol_speed, vertical_speed, dt)

        self.last_positions = {entity: position for entity, position in self.last_positions.items() if entity in live_entities}
        self.stuck_timers = {entity: timer for entity, timer in self.stuck_timers.items() if entity in live_entities}

    def _choose_target_entity(
        self,
        lander_position: pygame.Vector2,
        astronauts: dict[int, pygame.Vector2],
        max_distance: float,
    ) -> int | None:
        target_entity: int | None = None
        best_distance = max_distance
        for astronaut_entity, astronaut_position in astronauts.items():
            distance = self._wrapped_offset(lander_position, astronaut_position).length()
            if distance < best_distance:
                best_distance = distance
                target_entity = astronaut_entity
        return target_entity

    def _wrapped_dx(self, source_x: float, target_x: float) -> float:
        world_width = float(self.world_cfg.get("width", 2048))
        return (target_x - source_x + world_width / 2) % world_width - world_width / 2

    def _wrapped_offset(self, source: pygame.Vector2, target: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2(self._wrapped_dx(source.x, target.x), target.y - source.y)

    def _recover_if_stuck(
        self,
        entity: int,
        position: pygame.Vector2,
        velocity: Velocity,
        enemy: Enemy,
        state: State,
        patrol_speed: float,
        vertical_speed: float,
        dt: float,
    ) -> None:
        previous = self.last_positions.get(entity)
        self.last_positions[entity] = position.copy()
        if previous is None or state.name in {"abducting", "ascending"}:
            self.stuck_timers[entity] = 0.0
            return

        moved = position.distance_to(previous)
        if moved <= 0.35:
            self.stuck_timers[entity] = self.stuck_timers.get(entity, 0.0) + dt
        else:
            self.stuck_timers[entity] = 0.0

        if self.stuck_timers[entity] < 1.1:
            return

        enemy.target_entity = None
        enemy.alerting = False
        velocity.value.x = self.rng.choice((-1.0, 1.0)) * patrol_speed
        velocity.value.y = self.rng.choice((-1.0, 0.0, 1.0)) * vertical_speed * 0.35
        self._change_state(state, enemy, "patrol")
        self.stuck_timers[entity] = 0.0

    def _change_state(self, state: State, enemy: Enemy, new_state: str) -> None:
        if state.name != new_state:
            state.name = new_state
            state.elapsed = 0.0
        enemy.state = state.name

    def _signed_speed(self, distance: float, speed: float) -> float:
        if abs(distance) < 0.5:
            return 0.0
        return speed if distance > 0 else -speed
