from __future__ import annotations

import pygame

from src.components.astronaut import Astronaut
from src.components.enemy import Enemy
from src.components.state import State
from src.components.tag import Tag
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_audio_event, create_mutant


class AbductionSystem:
    def __init__(self) -> None:
        self.enemies_cfg = ServiceLocator.config.get("enemies")
        self.audio_cfg = ServiceLocator.config.get("audio")

    def update(self, world, dt: float) -> None:
        capture_sound = self.audio_cfg["sounds"].get("lander_capture_astronaut")
        mutate_sound = self.audio_cfg["sounds"].get("lander_mutate_astronaut")
        carry_offset = pygame.Vector2(0, 12)

        for enemy_entity, (enemy_transform, enemy_velocity, enemy, enemy_state, enemy_tag) in world.get_components(
            Transform, Velocity, Enemy, State, Tag
        ):
            if enemy.kind != "lander" or not enemy_tag.has("enemy"):
                continue
            if enemy_state.name not in {"abducting", "ascending"}:
                continue

            astronaut_entity = enemy.carried_entity or enemy.target_entity
            if astronaut_entity is None or not world.has_component(astronaut_entity, Astronaut):
                enemy.target_entity = None
                enemy.carried_entity = None
                enemy.alerting = False
                enemy_state.name = "patrol"
                enemy.state = "patrol"
                continue

            astronaut = world.component_for_entity(astronaut_entity, Astronaut)
            astronaut_state = world.component_for_entity(astronaut_entity, State)
            astronaut_transform = world.component_for_entity(astronaut_entity, Transform)
            astronaut_velocity = world.component_for_entity(astronaut_entity, Velocity)
            lander_cfg = self.enemies_cfg["lander"]
            abduction_speed = float(lander_cfg.get("abduction_speed", 18.0))
            top_escape_y = float(lander_cfg.get("top_escape_y", 20.0))

            if astronaut.state == "walking" and enemy_state.name == "abducting":
                astronaut.state = "captured"
                astronaut_state.name = "captured"
                astronaut_state.elapsed = 0.0
                astronaut.carrier_entity = enemy_entity
                enemy.carried_entity = astronaut_entity
                enemy.alerting = True
                if capture_sound:
                    create_audio_event(world, capture_sound)
                enemy_state.name = "ascending"
                enemy.state = "ascending"

            if astronaut.state == "captured":
                enemy_velocity.value.x *= 0.98
                enemy_velocity.value.y = -abduction_speed
                astronaut_transform.position = enemy_transform.position + carry_offset
                astronaut_velocity.value.update(0.0, 0.0)
                if enemy_transform.position.y <= top_escape_y:
                    if mutate_sound:
                        create_audio_event(world, mutate_sound)
                    create_mutant(world)
                    world.delete_entity(astronaut_entity, immediate=True)
                    world.delete_entity(enemy_entity, immediate=True)
