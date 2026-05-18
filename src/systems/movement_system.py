from src.components.player import Player
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.components.enemy import Enemy
from src.components.state import State


# Do not allow enemies to move above the HUD area (top HUD height in pixels)
# Raised to 56 to leave a safe margin under the HUD
HUD_BOTTOM_Y = 56


class MovementSystem:
    def update(self, world, dt: float) -> None:
        for entity, (transform, velocity) in world.get_components(Transform, Velocity):
            if world.has_component(entity, Player):
                continue
            transform.position += velocity.value * dt

            if world.has_component(entity, Enemy):
                if world.has_component(entity, State):
                    state = world.component_for_entity(entity, State)
                    if state.name in {"ascending", "transform_to_mutant"}:

                        continue
                if transform.position.y < HUD_BOTTOM_Y:
                    transform.position.y = HUD_BOTTOM_Y
