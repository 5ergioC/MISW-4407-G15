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

    def update(self, world, dt: float) -> None:
        if dt <= 0:
            return

        players = list(world.get_components(Transform, Tag))
        player_pos = None
        for _, (t, tag) in players:
            if tag.has("player"):
                player_pos = t.position.copy()
                break

        astronauts = []
        for ent, (t, astro, tag) in world.get_components(Transform, Astronaut, Tag):
            if tag.has("astronaut") and astro.state == "walking":
                astronauts.append((ent, t))

        for ent, (t, v, enemy, state, tag) in world.get_components(Transform, Velocity, Enemy, State, Tag):
            if enemy.kind != "lander" or not tag.has("enemy"):
                continue

            cfg = self.enemies_cfg.get("lander", {})
            patrol_speed = float(cfg.get("speed", 40.0))
            abduction_speed = float(cfg.get("abduction_speed", 18.0))
            seek_radius = float(cfg.get("seek_radius", 90.0))

            # State machine: patrol, seek_astronaut, abducting, ascending, attack_player
            current = state.name if hasattr(state, "name") else getattr(state, "state", "patrol")


            player_visible = False
            if player_pos is not None:
                dx = abs(player_pos.x - t.position.x)
                if dx <= self.world_cfg.get("width", 4096) / 2:
                    player_visible = True

            if current in ("abducting", "ascending"):
                if current == "abducting":
                    v.value.y = -abduction_speed
                else:
                    v.value.y = -abduction_speed * 0.6
                v.value.x = max(-patrol_speed, min(patrol_speed, v.value.x))
                continue

            if player_visible:
                direction = 1.0 if player_pos.x > t.position.x else -1.0
                v.value.x = direction * patrol_speed
                state.name = "attack_player"
                continue

            target = None
            best_dist = 1e9
            for a_ent, a_t in astronauts:
                dist = abs(a_t.position.x - t.position.x)
                if dist < best_dist and dist <= seek_radius:
                    best_dist = dist
                    target = a_t

            if target is not None:
                direction = 1.0 if target.position.x > t.position.x else -1.0
                v.value.x = direction * (patrol_speed * 0.9)
                if best_dist <= max(8.0, target.position.y - t.position.y) or best_dist < 10.0:
                    state.name = "abducting"
                    v.value.y = -abduction_speed
                else:
                    state.name = "seek_astronaut"
                continue

            if abs(v.value.x) < 1.0:
                v.value.x = random.choice((-1.0, 1.0)) * patrol_speed
            if self.rng.random() < 0.01:
                v.value.x *= -1.0
            state.name = "patrol"
