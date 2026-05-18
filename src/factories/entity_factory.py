from __future__ import annotations

import math
import random

import pygame

from src.components.animation import Animation
from src.components.audio_event import AudioEvent
from src.components.collider import Collider
from src.components.camera import CameraTarget
from src.components.laser import Laser
from src.components.lifetime import Lifetime
from src.components.parallax import Parallax
from src.components.particle import Particle
from src.components.planet import Planet
from src.components.player import Player
from src.components.projectile import Projectile
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.components.wraparound import Wraparound
from src.engine.service_locator import ServiceLocator

_EXPLOSION_COLORS: dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]] = {
    "lander":  ((255, 234, 125), (199,  55,   0)),
    "mutant":  ((255, 200, 255), ( 80,   0, 100)),
    "player":  ((255, 255, 255), (255, 105,  15)),
    "generic": ((255, 234, 125), (199,  55,   0)),
    "baiter":  ((255, 200,  80), (180,  60,   0)),
    "bomber":  ((255, 234, 125), (199,  55,   0)),
}

_FLASH_FRAME_W = 12
_FLASH_LIFETIME = 0.12


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

    burner = world.create_entity()
    world.add_component(burner, Transform(pygame.Vector2(spawn["x"] - 8, spawn["y"])))
    world.add_component(
        burner,
        Renderable(
            shape="image",
            size=pygame.Vector2(8, 8),
            color=pygame.Color(255, 140, 0),
            layer=9,
            image_path="img/player_burner_idle.png",
            centered=True,
            visible=False,
        ),
    )
    player_component = world.component_for_entity(entity, Player)
    player_component.burner_entity = burner
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
            size=pygame.Vector2(5, 1),
            color=pygame.Color(255, 240, 150),
            layer=8,
            trail_length=30,
            trail_dir=direction,
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


LANDER_FRAME_W = 15
LANDER_FRAME_H = 12
LANDER_FRAME_COUNT = 5

ASTRONAUT_FRAME_W = 10
ASTRONAUT_FRAME_H = 10
ASTRONAUT_FRAME_COUNT = 3


def make_lander_animation() -> Animation:
    return Animation(frame_count=LANDER_FRAME_COUNT, frame_time=0.12, loop=True)


def make_astronaut_animation() -> Animation:
    return Animation(frame_count=ASTRONAUT_FRAME_COUNT, frame_time=0.18, loop=True)


def create_audio_event(world, sound_path: str) -> int:
    return world.create_entity(AudioEvent(sound_path))


def create_explosion(
    world,
    position: pygame.Vector2,
    kind: str = "generic",
    count: int = 14,
    speed_min: float = 20.0,
    speed_max: float = 60.0,
    lifetime_min: float = 0.3,
    lifetime_max: float = 0.7,
) -> list[int]:
    start_color, end_color = _EXPLOSION_COLORS.get(kind, _EXPLOSION_COLORS["generic"])
    entities: list[int] = []
    flash = world.create_entity()
    world.add_component(flash, Transform(position.copy()))
    world.add_component(
        flash,
        Renderable(
            shape="image",
            size=pygame.Vector2(_FLASH_FRAME_W, _FLASH_FRAME_W),
            color=pygame.Color(255, 255, 255),
            layer=25,
            image_path="img/explosion_flash.png",
            centered=True,
            sprite_frame_width=_FLASH_FRAME_W,
            sprite_frame=0,
        ),
    )
    world.add_component(flash, Animation(frame_count=3, frame_time=0.04, loop=False))
    world.add_component(flash, Lifetime(_FLASH_LIFETIME))

    for i in range(count):
        angle = (i / count) * math.tau + random.uniform(-0.3, 0.3)
        speed = random.uniform(speed_min, speed_max)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        lifetime = random.uniform(lifetime_min, lifetime_max)
        radius = random.uniform(0.8, 2.0)

        if kind == "player":
            end = (
                random.randint(180, 255),
                random.randint(50, 200),
                random.randint(0, 80),
            )
        else:
            end = end_color

        entity = world.create_entity()
        world.add_component(entity, Transform(position.copy()))
        world.add_component(entity, Velocity(pygame.Vector2(vx, vy)))
        world.add_component(
            entity,
            Renderable(
                shape="circle",
                size=pygame.Vector2(radius, radius),
                color=pygame.Color(*start_color),
                layer=20,
            ),
        )
        world.add_component(entity, Particle(kind=kind, start_color=start_color, end_color=end, lifetime_max=lifetime))
        world.add_component(entity, Lifetime(lifetime))
        entities.append(entity)
    return entities


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
    # blend last 15% toward start y for seamless wrap
    if len(points) > 20:
        blend_count = max(8, len(points) // 7)
        start_y = points[0][1]
        for i in range(blend_count):
            idx = len(points) - blend_count + i
            if 0 <= idx < len(points):
                t = i / blend_count
                x_coord, y_coord = points[idx]
                points[idx] = (x_coord, y_coord + (start_y - y_coord) * t)
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
