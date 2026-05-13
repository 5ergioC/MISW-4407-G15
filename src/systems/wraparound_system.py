from src.components.transform import Transform
from src.components.wraparound import Wraparound


class WraparoundSystem:
    def update(self, world, dt: float) -> None:
        del dt
        for _, (transform, wraparound) in world.get_components(Transform, Wraparound):
            if transform.position.x < -wraparound.margin:
                transform.position.x = wraparound.world_width + wraparound.margin
            elif transform.position.x > wraparound.world_width + wraparound.margin:
                transform.position.x = -wraparound.margin
