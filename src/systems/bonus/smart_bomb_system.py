from __future__ import annotations

import pygame

from src.components.astronaut import Astronaut
from src.components.camera import Camera
from src.components.enemy import Enemy
from src.components.state import State
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.factories.entity_factory import create_audio_event, create_explosion


class SmartBombSystem:
    def activate(self, world, camera: Camera, shared_state: dict) -> None:
        if shared_state.get("smart_bombs", 0) <= 0:
            return

        world_width = camera.world_width
        margin = 16

        to_kill: list[tuple[int, str, pygame.Vector2]] = []
        for entity, (enemy, transform) in world.get_components(Enemy, Transform):
            screen_x = (transform.position.x - camera.x + world_width / 2) % world_width - world_width / 2
            if -margin <= screen_x <= camera.width + margin:
                to_kill.append((entity, enemy.kind, transform.position.copy()))

        if not to_kill:
            return

        shared_state["smart_bombs"] -= 1

        killed_ids = {e for e, _, _ in to_kill}

        # Release any astronauts being carried by killed enemies
        for _, (astronaut, state) in world.get_components(Astronaut, State):
            if astronaut.carrier_entity in killed_ids or astronaut.state in ("captured", "carried"):
                if astronaut.carrier_entity in killed_ids or astronaut.carrier_entity is None:
                    astronaut.state = "falling"
                    astronaut.carrier_entity = None
                    state.name = "falling"
                    state.elapsed = 0.0

        for entity, kind, position in to_kill:
            if world.entity_exists(entity):
                # Clear carried reference on enemy before deleting
                if world.has_component(entity, Enemy):
                    e = world.component_for_entity(entity, Enemy)
                    if e:
                        e.carried_entity = None
                        e.target_entity = None
                world.delete_entity(entity, immediate=True)
            create_explosion(world, position, kind=kind, count=16)

        create_audio_event(world, "snd/enemy_die.ogg")
