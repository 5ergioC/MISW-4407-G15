from __future__ import annotations

import random
import pygame

from src.components.astronaut import Astronaut
from src.components.player import Player
from src.components.state import State
from src.components.tag import Tag
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_score_event, create_score_popup


class AstronautSystem:
    def __init__(self) -> None:
        self.world_cfg = ServiceLocator.config.get("world")
        self.rng = random.Random()

    def update(self, world, dt: float) -> None:
        astronaut_cfg = self.world_cfg.get("astronauts", {})
        ground_y = float(astronaut_cfg.get("ground_y", self.world_cfg["height"] - self.world_cfg["planet_height"] - int(astronaut_cfg.get("ground_offset", 6))))
        walk_speed = float(astronaut_cfg.get("walk_speed", 8.0))
        rescue_distance = 14.0
        carry_offset = 10.0
        score_cfg = ServiceLocator.config.get("scoring")

        player_data = list(world.get_components(Transform, Velocity, Player))
        player_entity = None
        player_transform = None
        player_velocity = None
        player_component = None
        if player_data:
            player_entity, (player_transform, player_velocity, player_component) = player_data[0]

        for astronaut_entity, (transform, velocity, astronaut, state, tag) in world.get_components(Transform, Velocity, Astronaut, State, Tag):
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

            if astronaut.state == "falling":
                if (
                    player_entity is not None
                    and player_component is not None
                    and player_component.carried_astronaut is None
                    and player_transform is not None
                    and player_transform.position.distance_to(transform.position) <= rescue_distance
                ):
                    astronaut.state = "carried_by_player"
                    astronaut.carrier_entity = player_entity
                    astronaut.rescued_from_fall = True
                    player_component.carried_astronaut = astronaut_entity
                    rescue_score = int(score_cfg.get("astronaut_rescued_falling", 0))
                    create_score_event(world, rescue_score)
                    create_score_popup(world, player_transform.position + pygame.Vector2(0, -12), rescue_score)
                    transform.position.x = player_transform.position.x
                    transform.position.y = player_transform.position.y + carry_offset
                    state.name = "carried_by_player"
                    state.elapsed = 0.0
                    velocity.value.update(0.0, 0.0)
                    continue

                state.name = "falling"
                state.elapsed += dt
                continue

            if astronaut.state == "captured":
                state.name = "captured"
                state.elapsed += dt
                continue

            if astronaut.state == "carried_by_player":
                if (
                    player_entity is None
                    or player_component is None
                    or player_transform is None
                    or player_component.carried_astronaut != astronaut_entity
                ):
                    astronaut.state = "falling"
                    astronaut.carrier_entity = None
                    astronaut.fall_start_y = transform.position.y
                    state.name = "falling"
                    state.elapsed = 0.0
                    continue

                transform.position.x = player_transform.position.x
                transform.position.y = player_transform.position.y + carry_offset
                velocity.value.update(0.0, 0.0)
                state.name = "carried_by_player"
                state.elapsed += dt
                if player_transform.position.y >= ground_y - 1:
                    astronaut.deposited = True
                    rescue_score = int(score_cfg.get("astronaut_rescued_falling", 0)) if astronaut.rescued_from_fall else int(score_cfg.get("astronaut_deposited", 0))
                    create_score_event(world, rescue_score)
                    create_score_popup(world, pygame.Vector2(player_transform.position.x, ground_y - 14), rescue_score)
                    astronaut.rescued_from_fall = False
                    astronaut.state = "deposited"
                    astronaut.carrier_entity = None
                    player_component.carried_astronaut = None
                    transform.position.y = ground_y
                    velocity.value.update(0.0, 0.0)
                    state.name = "deposited"
                    state.elapsed = 0.0
                continue

            if astronaut.state == "deposited":
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
