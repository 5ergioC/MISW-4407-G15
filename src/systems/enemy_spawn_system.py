from __future__ import annotations

import random

from src.components.tag import Tag
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_astronaut, create_lander, create_mutant


class EnemySpawnSystem:
    def __init__(self) -> None:
        waves_cfg = ServiceLocator.config.get("waves")
        self.enemies_cfg = ServiceLocator.config.get("enemies")
        self.waves: list[dict] = list(waves_cfg.get("waves", []))
        self.loop_after_last_wave = bool(waves_cfg.get("loop_after_last_wave", False))

        self.wave_index = 0
        self.wave_started = False
        self.remaining_landers = 0
        self.remaining_mutants = 0
        self.spawn_timer = 0.0
        self.rng = random.Random()

    def update(self, world, dt: float) -> None:
        if not self.waves:
            return

        if self.wave_index >= len(self.waves):
            if not self.loop_after_last_wave:
                return
            self.wave_index = 0

        wave = self.waves[self.wave_index]
        if not self.wave_started:
            self._start_wave(world, wave)

        self.spawn_timer -= dt
        spawn_interval = max(0.1, float(wave.get("spawn_interval", 2.0)))
        while self.spawn_timer <= 0.0 and (self.remaining_landers > 0 or self.remaining_mutants > 0):
            self._spawn_enemy(world, wave)
            self.spawn_timer += spawn_interval

        if self._can_advance_wave(world):
            self.wave_index += 1
            self.wave_started = False

    def _start_wave(self, world, wave: dict) -> None:
        initial_landers = int(self.enemies_cfg.get("initial_landers", 0)) if self.wave_index == 0 else 0
        initial_mutants = int(self.enemies_cfg.get("initial_mutants", 0)) if self.wave_index == 0 else 0

        self.remaining_landers = int(wave.get("landers", 0)) + initial_landers
        self.remaining_mutants = int(wave.get("mutants", 0)) + initial_mutants
        self.spawn_timer = 0.0
        self.wave_started = True

        target_astronauts = max(0, int(wave.get("astronauts", 0)))
        current_astronauts = self._count_by_tag(world, "astronaut")
        for _ in range(max(0, target_astronauts - current_astronauts)):
            create_astronaut(world)

    def _spawn_enemy(self, world, wave: dict) -> None:
        can_spawn_lander = self.remaining_landers > 0
        can_spawn_mutant = self.remaining_mutants > 0
        if not can_spawn_lander and not can_spawn_mutant:
            return

        if can_spawn_lander and can_spawn_mutant:
            total = self.remaining_landers + self.remaining_mutants
            spawn_lander = self.rng.random() < (self.remaining_landers / total)
        else:
            spawn_lander = can_spawn_lander

        if spawn_lander:
            create_lander(world, speed_multiplier=float(wave.get("lander_speed_multiplier", 1.0)))
            self.remaining_landers -= 1
        else:
            create_mutant(world, speed_multiplier=float(wave.get("mutant_speed_multiplier", 1.0)))
            self.remaining_mutants -= 1

    def _can_advance_wave(self, world) -> bool:
        if self.remaining_landers > 0 or self.remaining_mutants > 0:
            return False
        return self._count_by_tag(world, "enemy") == 0

    def _count_by_tag(self, world, label: str) -> int:
        count = 0
        for _, (tag,) in world.get_components(Tag):
            if tag.has(label):
                count += 1
        return count
