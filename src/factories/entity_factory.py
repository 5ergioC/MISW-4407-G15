from __future__ import annotations

import random

import pygame

from src.components.collider import Collider
from src.components.laser import Laser
from src.components.lifetime import Lifetime
from src.components.player import Player
from src.components.projectile import Projectile
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.components.wraparound import Wraparound
from src.engine.service_locator import ServiceLocator


def create_player(world) -> int:
    player_cfg = ServiceLocator.config.get("player")
    world_cfg = ServiceLocator.config.get("world")
    entity = world.create_entity()
    spawn = player_cfg["spawn"]
    size = player_cfg["size"]
    world.add_component(entity, Transform(pygame.Vector2(spawn["x"], spawn["y"])))
    world.add_component(entity, Velocity(pygame.Vector2()))
    world.add_component(
        entity,
        Renderable(
            shape="triangle",
            size=pygame.Vector2(size["w"], size["h"]),
            color=pygame.Color(120, 255, 240),
            layer=10,
            points=[(-6, 0), (5, -4), (5, 4)],
        ),
    )
    world.add_component(entity, Collider(pygame.Vector2(size["w"], size["h"]), pygame.Vector2()))
    world.add_component(
        entity,
        Player(
            thrust_input=pygame.Vector2(),
            thrust=player_cfg["thrust"],
            drag=player_cfg["drag"],
            max_speed=player_cfg["max_speed"],
            lives=player_cfg["lives"],
        ),
    )
    world.add_component(entity, Wraparound(world_width=world_cfg["width"], margin=12))
    return entity


def create_laser(world, position: pygame.Vector2, direction: float) -> int:
    player_cfg = ServiceLocator.config.get("player")
    entity = world.create_entity()
    velocity = pygame.Vector2(direction, 0) * player_cfg["laser_speed"]
    world.add_component(entity, Transform(position.copy()))
    world.add_component(entity, Velocity(velocity))
    world.add_component(
        entity,
        Renderable(
            shape="rect",
            size=pygame.Vector2(8, 2),
            color=pygame.Color(255, 240, 150),
            layer=8,
        ),
    )
    world.add_component(entity, Collider(pygame.Vector2(8, 2), pygame.Vector2()))
    world.add_component(
        entity,
        Projectile(owner="player", direction=pygame.Vector2(direction, 0), speed=velocity.length(), damage=1),
    )
    world.add_component(entity, Laser())
    world.add_component(entity, Lifetime(0.9))
    return entity


def create_starfield(world) -> list[int]:
    world_cfg = ServiceLocator.config.get("world")
    entities: list[int] = []
    for _ in range(world_cfg["stars"]):
        entity = world.create_entity()
        x = random.uniform(0, world_cfg["width"])
        y = random.uniform(0, world_cfg["height"] - world_cfg["planet_height"] - 8)
        speed = random.uniform(-12, -4)
        tone = random.randint(140, 255)
        world.add_component(entity, Transform(pygame.Vector2(x, y)))
        world.add_component(entity, Velocity(pygame.Vector2(speed, 0)))
        world.add_component(
            entity,
            Renderable(
                shape="rect",
                size=pygame.Vector2(1, 1),
                color=pygame.Color(tone, tone, tone),
                layer=0,
            ),
        )
        world.add_component(entity, Wraparound(world_width=world_cfg["width"], margin=1))
        entities.append(entity)
    return entities
