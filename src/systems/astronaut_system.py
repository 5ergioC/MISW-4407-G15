from __future__ import annotations

import random

from src.components.astronaut import Astronaut
from src.components.state import State
from src.components.tag import Tag
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator


class AstronautSystem:
    def __init__(self) -> None:
        self.world_cfg = ServiceLocator.config.get("world")
        self.rng = random.Random()

    def update(self, world, dt: float) -> None:
        astronaut_cfg = self.world_cfg.get("astronauts", {})
        ground_y = self.world_cfg["height"] - self.world_cfg["planet_height"] - int(astronaut_cfg.get("ground_offset", 6))
        walk_speed = float(astronaut_cfg.get("walk_speed", 8.0))

        for _, (transform, velocity, astronaut, state, tag) in world.get_components(Transform, Velocity, Astronaut, State, Tag):
            if not tag.has("astronaut"):
                continue

            if astronaut.state == "walking":
                transform.position.y = ground_y
                velocity.value.y = 0.0
                if abs(velocity.value.x) < 0.1:
                    velocity.value.x = self.rng.choice((-1.0, 1.0)) * walk_speed
                if self.rng.random() < min(0.35 * dt, 0.05):
                    velocity.value.x *= -1.0
                state.name = "walking"
                state.elapsed += dt
                continue

            if astronaut.state in {"captured", "falling", "carried_by_player"}:
                state.name = astronaut.state
                state.elapsed += dt
                continue

            if astronaut.state == "deposited":
                astronaut.deposited = True
                astronaut.state = "walking"
                state.name = "walking"
                state.elapsed = 0.0
                velocity.value.y = 0.0
                if abs(velocity.value.x) < 0.1:
                    velocity.value.x = walk_speed
                continue

            if astronaut.state == "dead":
                velocity.value.update(0.0, 0.0)
                state.name = "dead"
