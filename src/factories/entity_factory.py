from __future__ import annotations

import random

import pygame

from src.components.audio_event import AudioEvent
from src.components.animation import Animation
from src.components.astronaut import Astronaut
from src.components.collider import Collider
from src.components.camera import CameraTarget
from src.components.enemy import Enemy
from src.components.health import Health
from src.components.input_command import InputCommand
from src.components.laser import Laser
from src.components.lifetime import Lifetime
from src.components.parallax import Parallax
from src.components.planet import Planet
from src.components.player import Player
from src.components.projectile import Projectile
from src.components.particle import Particle
from src.components.renderable import Renderable
from src.components.score_value import ScoreValue
from src.components.state import State
from src.components.tag import Tag
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


def create_enemy_bullet(world, position: pygame.Vector2, direction: pygame.Vector2, speed: float, owner_velocity: pygame.Vector2 | None = None) -> int:
    enemies_cfg = ServiceLocator.config.get("enemies")
    bullet_cfg = enemies_cfg["bullet"]
    sheet = ServiceLocator.images_service.get("img/enemy_bullet.png")
    bullet_size = pygame.Vector2(max(1, sheet.get_width()), max(1, sheet.get_height()))
    travel_direction = direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(1, 0)
    velocity = travel_direction * speed
    if owner_velocity is not None:
        velocity += owner_velocity * 0.25

    entity = world.create_entity()
    world.add_component(entity, Transform(position.copy()))
    world.add_component(entity, Velocity(velocity))
    world.add_component(
        entity,
        Renderable(
            shape="image",
            size=bullet_size,
            color=pygame.Color(255, 255, 255),
            layer=8,
            image_path="img/enemy_bullet.png",
            centered=True,
        ),
    )
    world.add_component(entity, Collider(bullet_size, pygame.Vector2()))
    world.add_component(entity, Projectile(owner="enemy", direction=travel_direction, speed=speed, damage=1))
    world.add_component(entity, Lifetime(float(bullet_cfg["lifetime"])))
    world.add_component(entity, Tag("enemy_projectile"))
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


def _create_enemy_entity(
    world,
    *,
    kind: str,
    state: str,
    image_path: str,
    frame_count: int,
    layer: int,
    score: int,
    spawn_y_min: float,
    spawn_y_max: float,
    speed_x: float,
    speed_y: float,
    tag_labels: tuple[str, ...],
    frame_time: float,
    wrap_margin: int = 16,
) -> int:
    world_cfg = ServiceLocator.config.get("world")
    sheet = ServiceLocator.images_service.get(image_path)
    frame_width = max(1, sheet.get_width() // max(1, frame_count))
    frame_height = max(1, sheet.get_height())
    render_size = pygame.Vector2(frame_width, frame_height)
    spawn_x = random.uniform(0, world_cfg["width"])
    spawn_y = random.uniform(spawn_y_min, spawn_y_max)

    entity = world.create_entity()
    world.add_component(entity, Transform(pygame.Vector2(spawn_x, spawn_y)))
    world.add_component(entity, Velocity(pygame.Vector2(speed_x, speed_y)))
    world.add_component(
        entity,
        Renderable(
            shape="image",
            size=render_size,
            color=pygame.Color(255, 255, 255),
            layer=layer,
            image_path=image_path,
            centered=True,
        ),
    )
    world.add_component(entity, Collider(render_size, pygame.Vector2()))
    world.add_component(entity, Animation(frame_count=frame_count, frame_time=frame_time, loop=True))
    world.add_component(entity, Enemy(kind=kind, state=state))
    world.add_component(entity, State(name=state))
    world.add_component(entity, Health(current=1, maximum=1))
    world.add_component(entity, ScoreValue(amount=score))
    world.add_component(entity, Tag("enemy", *tag_labels))
    world.add_component(
        entity,
        Wraparound(
            world_width=world_cfg["width"],
            world_height=world_cfg["height"],
            margin=wrap_margin,
            horizontal=True,
            vertical=True,
        ),
    )
    return entity


def create_enemy_death_fx(world, position: pygame.Vector2) -> None:
    fragment_palette = [
        pygame.Color(255, 120, 45),
        pygame.Color(255, 165, 65),
        pygame.Color(255, 205, 90),
        pygame.Color(255, 95, 35),
    ]
    for index in range(6):
        angle = index * 60 + random.uniform(-12, 12)
        direction = pygame.Vector2(1, 0).rotate(angle)
        speed = random.uniform(40.0, 120.0)
        fragment = world.create_entity()
        offset = direction * random.uniform(0.0, 5.0)
        size = pygame.Vector2(random.uniform(2.0, 4.0), random.uniform(2.0, 4.0))
        world.add_component(fragment, Transform(position.copy() + offset - size / 2))
        world.add_component(fragment, Velocity(direction * speed))
        world.add_component(
            fragment,
            Renderable(
                shape="rect",
                size=size,
                color=random.choice(fragment_palette),
                layer=11,
                centered=True,
            ),
        )
        world.add_component(fragment, Particle(kind="enemy_death_fragment"))
        world.add_component(fragment, Lifetime(random.uniform(0.12, 0.28)))

    return None


def create_player_death_fx(world, position: pygame.Vector2) -> None:
    fragment_palette = [
        pygame.Color(120, 255, 240),
        pygame.Color(90, 220, 255),
        pygame.Color(170, 240, 255),
        pygame.Color(255, 255, 255),
    ]
    for index in range(7):
        angle = index * (360 / 7) + random.uniform(-10, 10)
        direction = pygame.Vector2(1, 0).rotate(angle)
        speed = random.uniform(55.0, 140.0)
        fragment = world.create_entity()
        offset = direction * random.uniform(0.0, 6.0)
        size = pygame.Vector2(random.uniform(2.5, 5.0), random.uniform(2.5, 5.0))
        world.add_component(fragment, Transform(position.copy() + offset - size / 2))
        world.add_component(fragment, Velocity(direction * speed))
        world.add_component(
            fragment,
            Renderable(
                shape="rect",
                size=size,
                color=random.choice(fragment_palette),
                layer=12,
                centered=True,
            ),
        )
        world.add_component(fragment, Particle(kind="player_death_fragment"))
        world.add_component(fragment, Lifetime(random.uniform(0.14, 0.34)))



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
        pygame.K_o: "PLAYER_LOSE_LIFE",
        pygame.K_v: "PLAYER_WIN",
        pygame.K_ESCAPE: "PLAYER_MENU",
        pygame.K_h: "TOGGLE_ENEMY_FIRE",
    }
    
    for key, name in input_map.items():
        entity = world.create_entity()
        world.add_component(entity, InputCommand(name=name, key=key))


def create_lander(world, speed_multiplier: float = 1.0) -> int:
    enemies_cfg = ServiceLocator.config.get("enemies")
    lander_cfg = enemies_cfg["lander"]
    speed = float(lander_cfg["speed"]) * max(0.1, speed_multiplier)
    direction = random.choice((-1.0, 1.0))
    world_cfg = ServiceLocator.config.get("world")
    return _create_enemy_entity(
        world,
        kind="lander",
        state="patrol",
        image_path="img/enemy_lander.png",
        frame_count=5,
        layer=9,
        score=int(lander_cfg["score"]),
        spawn_y_min=56,
        spawn_y_max=max(58, world_cfg["height"] - world_cfg["planet_height"] - 26),
        speed_x=direction * speed,
        speed_y=0.0,
        tag_labels=("enemy_lander", "lander"),
        frame_time=0.09,
    )


def create_mutant(world, speed_multiplier: float = 1.0) -> int:
    enemies_cfg = ServiceLocator.config.get("enemies")
    mutant_cfg = enemies_cfg["mutant"]
    speed = float(mutant_cfg["speed"]) * max(0.1, speed_multiplier)
    direction_x = random.choice((-1.0, 1.0))
    direction_y = random.choice((-1.0, 1.0))
    world_cfg = ServiceLocator.config.get("world")
    return _create_enemy_entity(
        world,
        kind="mutant",
        state="chase",
        image_path="img/enemy_mutant.png",
        frame_count=5,
        layer=9,
        score=int(mutant_cfg["score"]),
        spawn_y_min=48,
        spawn_y_max=max(50, world_cfg["height"] - world_cfg["planet_height"] - 32),
        speed_x=direction_x * speed,
        speed_y=direction_y * speed * 0.35,
        tag_labels=("enemy_mutant", "mutant"),
        frame_time=0.08,
    )


def create_bomber(world, speed_multiplier: float = 1.0) -> int:
    enemies_cfg = ServiceLocator.config.get("enemies")
    bomber_cfg = enemies_cfg["bomber"]
    speed = float(bomber_cfg["speed"]) * max(0.1, speed_multiplier)
    direction_x = random.choice((-1.0, 1.0))
    return _create_enemy_entity(
        world,
        kind="bomber",
        state="bombing",
        image_path="img/enemy_bomber.png",
        frame_count=5,
        layer=9,
        score=int(bomber_cfg["score"]),
        spawn_y_min=42,
        spawn_y_max=140,
        speed_x=direction_x * speed,
        speed_y=speed * 0.24,
        tag_labels=("enemy_bomber", "bomber"),
        frame_time=0.08,
    )


def create_baiter(world, speed_multiplier: float = 1.0) -> int:
    enemies_cfg = ServiceLocator.config.get("enemies")
    baiter_cfg = enemies_cfg["baiter"]
    speed = float(baiter_cfg["speed"]) * max(0.1, speed_multiplier)
    direction_x = random.choice((-1.0, 1.0))
    direction_y = random.choice((-1.0, 1.0))
    return _create_enemy_entity(
        world,
        kind="baiter",
        state="chasing",
        image_path="img/enemy_baiter.png",
        frame_count=5,
        layer=9,
        score=int(baiter_cfg["score"]),
        spawn_y_min=44,
        spawn_y_max=156,
        speed_x=direction_x * speed,
        speed_y=direction_y * speed * 0.18,
        tag_labels=("enemy_baiter", "baiter"),
        frame_time=0.07,
    )


def create_swarmer(world, speed_multiplier: float = 1.0) -> int:
    enemies_cfg = ServiceLocator.config.get("enemies")
    swarmer_cfg = enemies_cfg["swarmer"]
    speed = float(swarmer_cfg["speed"]) * max(0.1, speed_multiplier)
    direction_x = random.choice((-1.0, 1.0))
    direction_y = random.choice((-1.0, 1.0))
    return _create_enemy_entity(
        world,
        kind="swarmer",
        state="swarming",
        image_path="img/enemy_swarmer.png",
        frame_count=1,
        layer=9,
        score=int(swarmer_cfg["score"]),
        spawn_y_min=36,
        spawn_y_max=180,
        speed_x=direction_x * speed,
        speed_y=direction_y * speed * 0.14,
        tag_labels=("enemy_swarmer", "swarmer"),
        frame_time=0.1,
    )


def create_pod(world, speed_multiplier: float = 1.0) -> int:
    enemies_cfg = ServiceLocator.config.get("enemies")
    pod_cfg = enemies_cfg["pod"]
    speed = float(pod_cfg["speed"]) * max(0.1, speed_multiplier)
    direction_x = random.choice((-1.0, 1.0))
    return _create_enemy_entity(
        world,
        kind="pod",
        state="drifting",
        image_path="img/enemy_pod.png",
        frame_count=1,
        layer=9,
        score=int(pod_cfg["score"]),
        spawn_y_min=32,
        spawn_y_max=120,
        speed_x=direction_x * speed * 0.4,
        speed_y=speed * 0.16,
        tag_labels=("enemy_pod", "pod"),
        frame_time=0.1,
    )


def create_astronaut(world) -> int:
    world_cfg = ServiceLocator.config.get("world")
    astronaut_cfg = world_cfg.get("astronauts", {})
    ground_offset = int(astronaut_cfg.get("ground_offset", 6))
    astronaut_sheet = ServiceLocator.images_service.get("img/astronaut.png")
    astronaut_frame_w = max(1, astronaut_sheet.get_width() // 3)
    astronaut_frame_h = max(1, astronaut_sheet.get_height())
    render_size = pygame.Vector2(astronaut_frame_w, astronaut_frame_h)

    spawn_x = random.uniform(0, world_cfg["width"])
    spawn_y = world_cfg["height"] - world_cfg["planet_height"] - ground_offset

    entity = world.create_entity()
    world.add_component(entity, Transform(pygame.Vector2(spawn_x, spawn_y)))
    world.add_component(entity, Velocity(pygame.Vector2(0, 0)))
    world.add_component(
        entity,
        Renderable(
            shape="image",
            size=render_size,
            color=pygame.Color(255, 255, 255),
            layer=8,
            image_path="img/astronaut.png",
            centered=True,
        ),
    )
    world.add_component(entity, Collider(render_size, pygame.Vector2()))
    world.add_component(entity, Animation(frame_count=3, frame_time=0.12, loop=True))
    world.add_component(entity, Astronaut(state="walking"))
    world.add_component(entity, State(name="walking"))
    world.add_component(entity, Tag("astronaut", "friendly", "rescuable"))
    world.add_component(
        entity,
        Wraparound(
            world_width=world_cfg["width"],
            margin=12,
            horizontal=True,
            vertical=False,
        ),
    )
    return entity
