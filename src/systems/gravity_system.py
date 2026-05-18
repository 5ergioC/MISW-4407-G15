from __future__ import annotations

from src.components.astronaut import Astronaut
from src.components.renderable import Renderable
from src.components.state import State
from src.components.tag import Tag
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_audio_event


class GravitySystem:
    def __init__(self) -> None:
        self.world_cfg = ServiceLocator.config.get("world")
        self.audio_cfg = ServiceLocator.config.get("audio")

    def update(self, world, dt: float) -> None:
        astronaut_cfg = self.world_cfg.get("astronauts", {})
        gravity = float(astronaut_cfg.get("gravity", 65.0))
        ground_y = float(astronaut_cfg.get("ground_y", self.world_cfg["height"] - self.world_cfg["planet_height"] - int(astronaut_cfg.get("ground_offset", 6))))
        safe_fall_height = float(astronaut_cfg.get("safe_fall_height", 36.0))

        for _, (transform, velocity, astronaut, state, renderable, tag) in world.get_components(
            Transform, Velocity, Astronaut, State, Renderable, Tag
        ):
            if not tag.has("astronaut") or astronaut.state != "falling":
                continue

            if astronaut.fall_start_y is None:
                astronaut.fall_start_y = transform.position.y

            velocity.value.y += gravity * dt

            if transform.position.y < ground_y:
                continue

            transform.position.y = ground_y
            velocity.value.y = 0.0
            fall_distance = ground_y - float(astronaut.fall_start_y)
            astronaut.carrier_entity = None

            if fall_distance > safe_fall_height:
                astronaut.state = "dead"
                state.name = "dead"
                renderable.visible = False
                fall_sound = self.audio_cfg["sounds"].get("astronaut_fall")
                if fall_sound:
                    create_audio_event(world, fall_sound)
            else:
                astronaut.state = "walking"
                state.name = "walking"

            astronaut.fall_start_y = None
