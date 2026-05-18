from __future__ import annotations

import random

from src.components.tag import Tag
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import (
    create_astronaut,
    create_baiter,
    create_bomber,
    create_lander,
    create_mutant,
    create_pod,
    create_swarmer,
)


SPAWN_TYPES = (
    ("landers", "initial_landers", create_lander, "lander_speed_multiplier"),
    ("mutants", "initial_mutants", create_mutant, "mutant_speed_multiplier"),
    ("bombers", "initial_bombers", create_bomber, "bomber_speed_multiplier"),
    ("baiters", "initial_baiters", create_baiter, "baiter_speed_multiplier"),
    ("swarmers", "initial_swarmers", create_swarmer, "swarmer_speed_multiplier"),
    ("pods", "initial_pods", create_pod, "pod_speed_multiplier"),
)


class EnemySpawnSystem:
    def __init__(self) -> None:
        waves_cfg = ServiceLocator.config.get("waves")
        self.enemies_cfg = ServiceLocator.config.get("enemies")
        self.waves: list[dict] = list(waves_cfg.get("waves", []))
        self.loop_after_last_wave = bool(waves_cfg.get("loop_after_last_wave", False))

        self.wave_index = 0
        self.wave_started = False
        self.remaining_counts: dict[str, int] = {count_key: 0 for count_key, *_ in SPAWN_TYPES}
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
        while self.spawn_timer <= 0.0 and any(count > 0 for count in self.remaining_counts.values()):
            self._spawn_enemy(world, wave)
            self.spawn_timer += spawn_interval

        if self._can_advance_wave(world):
            self.wave_index += 1
            self.wave_started = False

    def reset(self) -> None:
        self.wave_index = 0
        self.wave_started = False
        self.remaining_counts = {count_key: 0 for count_key, *_ in SPAWN_TYPES}
        self.spawn_timer = 0.0

    def _start_wave(self, world, wave: dict) -> None:
        for count_key, initial_key, _, _ in SPAWN_TYPES:
            initial_count = int(self.enemies_cfg.get(initial_key, 0)) if self.wave_index == 0 else 0
            self.remaining_counts[count_key] = max(0, int(wave.get(count_key, 0)) + initial_count)
        self.spawn_timer = 0.0
        self.wave_started = True

        target_astronauts = max(0, int(wave.get("astronauts", 0)))
        current_astronauts = self._count_by_tag(world, "astronaut")
        missing_astronauts = max(0, target_astronauts - current_astronauts)
        if missing_astronauts > 0:
            world_cfg = ServiceLocator.config.get("world")
            spacing = world_cfg["width"] / (target_astronauts + 1)
            for index in range(missing_astronauts):
                create_astronaut(world, spacing * (current_astronauts + index + 1))

    def _spawn_enemy(self, world, wave: dict) -> None:
        available_types = [(count_key, spawn_fn, speed_multiplier_key) for count_key, _, spawn_fn, speed_multiplier_key in SPAWN_TYPES if self.remaining_counts[count_key] > 0]
        if not available_types:
            return

        total = sum(self.remaining_counts[count_key] for count_key, _, _ in available_types)
        roll = self.rng.uniform(0, total)
        accumulator = 0.0
        selected_count_key = available_types[-1][0]
        selected_spawn_fn = available_types[-1][1]
        selected_speed_key = available_types[-1][2]

        for count_key, spawn_fn, speed_multiplier_key in available_types:
            accumulator += self.remaining_counts[count_key]
            if roll <= accumulator:
                selected_count_key = count_key
                selected_spawn_fn = spawn_fn
                selected_speed_key = speed_multiplier_key
                break

        selected_spawn_fn(world, speed_multiplier=float(wave.get(selected_speed_key, 1.0)))
        self.remaining_counts[selected_count_key] -= 1

    def _can_advance_wave(self, world) -> bool:
        if any(count > 0 for count in self.remaining_counts.values()):
            return False
        return self._count_by_tag(world, "enemy") == 0

    def _count_by_tag(self, world, label: str) -> int:
        count = 0
        for _, (tag,) in world.get_components(Tag):
            if tag.has(label):
                count += 1
        return count
