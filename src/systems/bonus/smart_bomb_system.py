from __future__ import annotations

import pygame

from src.components.camera import Camera
from src.components.enemy import Enemy
from src.components.transform import Transform
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

        for entity, kind, position in to_kill:
            if world.entity_exists(entity):
                world.delete_entity(entity, immediate=True)
            create_explosion(world, position, kind=kind, count=16)

        create_audio_event(world, "snd/enemy_die.ogg")
