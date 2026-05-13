from src.components.player import Player
from src.components.transform import Transform
from src.components.velocity import Velocity


class MovementSystem:
    def update(self, world, dt: float) -> None:
        for entity, (transform, velocity) in world.get_components(Transform, Velocity):
            if world.has_component(entity, Player):
                continue
            transform.position += velocity.value * dt
