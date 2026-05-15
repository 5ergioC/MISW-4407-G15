from __future__ import annotations

import random

import pygame

from src.components.audio_event import AudioEvent
from src.components.collider import Collider
from src.components.camera import CameraTarget
from src.components.input_command import InputCommand
from src.components.laser import Laser
from src.components.lifetime import Lifetime
from src.components.parallax import Parallax
from src.components.planet import Planet
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
            shape="image",
            size=pygame.Vector2(size["w"], size["h"]),
            color=pygame.Color(120, 255, 240),
            layer=10,
            image_path="img/player.png",
            centered=True,
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
            max_speed_x=player_cfg["max_speed_x"],
            max_speed_y=player_cfg["max_speed_y"],
            vertical_min=player_cfg["vertical_margin_top"],
            vertical_max=world_cfg["height"] - player_cfg["vertical_margin_bottom"],
        ),
    )
    world.add_component(entity, Wraparound(world_width=world_cfg["width"], margin=12))
    world.add_component(entity, CameraTarget(look_ahead_x=player_cfg["camera"]["look_ahead_x"]))
    return entity


def create_laser(world, position: pygame.Vector2, direction: float, owner_velocity_x: float = 0.0) -> int:
    player_cfg = ServiceLocator.config.get("player")
    entity = world.create_entity()
    velocity = pygame.Vector2(direction * player_cfg["laser_speed"] + owner_velocity_x, 0)
    laser_size = pygame.Vector2(40, 1)
    world.add_component(entity, Transform(position.copy()))
    world.add_component(entity, Velocity(velocity))
    world.add_component(
        entity,
        Renderable(
            shape="rect",
            size=laser_size,
            color=pygame.Color(255, 240, 150),
            layer=8,
        ),
    )
    world.add_component(entity, Collider(laser_size, pygame.Vector2()))
    world.add_component(
        entity,
        Projectile(owner="player", direction=pygame.Vector2(direction, 0), speed=abs(velocity.x), damage=1),
    )
    world.add_component(entity, Laser())
    world.add_component(entity, Lifetime(player_cfg["laser_lifetime"]))
    return entity


def create_starfield(world) -> list[int]:
    world_cfg = ServiceLocator.config.get("world")
    entities: list[int] = []
    star_layers = world_cfg.get("stars_config", {}).get("layers", [])
    if not star_layers:
        star_layers = [{"count": world_cfg["stars"], "brightness_min": 140, "brightness_max": 255}]
    star_colors = [
        pygame.Color(255, 85, 52),
        pygame.Color(255, 197, 67),
        pygame.Color(246, 245, 89),
        pygame.Color(78, 202, 74),
        pygame.Color(210, 210, 210),
    ]
    for layer_index, layer in enumerate(star_layers):
        parallax = 0.2 + layer_index * 0.18
        for _ in range(layer["count"]):
            entity = world.create_entity()
            x = random.uniform(0, world_cfg["width"])
            y = random.uniform(18, world_cfg["height"] - world_cfg["planet_height"] - 10)
            color = random.choice(star_colors)
            brightness = random.randint(layer["brightness_min"], layer["brightness_max"]) / 255
            world.add_component(entity, Transform(pygame.Vector2(x, y)))
            world.add_component(
                entity,
                Renderable(
                    shape="rect",
                    size=pygame.Vector2(1, 1),
                    color=pygame.Color(
                        int(color.r * brightness),
                        int(color.g * brightness),
                        int(color.b * brightness),
                    ),
                    layer=0,
                ),
            )
            world.add_component(entity, Parallax(parallax))
            entities.append(entity)
    return entities


def create_planet(world) -> int:
    world_cfg = ServiceLocator.config.get("world")
    planet_cfg = world_cfg["planet"]
    rng = random.Random(planet_cfg["seed"])
    width = world_cfg["width"]
    step = planet_cfg["segment_width"]
    points = _generate_planet_points(rng, width, step, planet_cfg["min_y"], planet_cfg["max_y"])
    entity = world.create_entity()
    world.add_component(entity, Planet(points=points, parallax=planet_cfg["parallax"]))
    return entity


def create_audio_event(world, sound_path: str) -> int:
    return world.create_entity(AudioEvent(sound_path))


def _generate_planet_points(
    rng: random.Random,
    width: int,
    step: int,
    min_y: int,
    max_y: int,
) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    x = 0
    y = rng.uniform(min_y + 12, max_y - 8)
    while x <= width:
        section_steps = rng.randint(8, 36)
        target_y = _choose_planet_target_y(rng, min_y, max_y)
        start_y = y
        for index in range(section_steps):
            if x > width:
                break
            t = index / max(1, section_steps - 1)
            eased = t * t * (3 - 2 * t)
            jitter = rng.choice((-2, -1, 0, 0, 1, 2))
            y = start_y + (target_y - start_y) * eased + jitter
            y = max(min_y, min(max_y, y))
            points.append((float(x), float(round(y))))
            x += step
        y = target_y
    if points[-1][0] < width:
        points.append((float(width), float(round(y))))
    return points


def _choose_planet_target_y(rng: random.Random, min_y: int, max_y: int) -> float:
    roll = rng.random()
    if roll < 0.18:
        return rng.uniform(min_y, min_y + 8)
    if roll < 0.42:
        return rng.uniform(max_y - 10, max_y)
    if roll < 0.66:
        return rng.uniform((min_y + max_y) / 2 - 5, (min_y + max_y) / 2 + 8)
    return rng.uniform(min_y + 8, max_y - 8)


def create_input_commands(world) -> None:
    input_map = {
        pygame.K_LEFT: "PLAYER_LEFT",
        pygame.K_a: "PLAYER_LEFT",
        pygame.K_RIGHT: "PLAYER_RIGHT",
        pygame.K_d: "PLAYER_RIGHT",
        pygame.K_UP: "PLAYER_UP",
        pygame.K_w: "PLAYER_UP",
        pygame.K_DOWN: "PLAYER_DOWN",
        pygame.K_s: "PLAYER_DOWN",
        pygame.K_SPACE: "PLAYER_FIRE",
        pygame.K_p: "PLAYER_PAUSE",
        pygame.K_v: "PLAYER_WIN",
        pygame.K_ESCAPE: "PLAYER_MENU",
    }
    
    for key, name in input_map.items():
        entity = world.create_entity()
        world.add_component(entity, InputCommand(name=name, key=key))
