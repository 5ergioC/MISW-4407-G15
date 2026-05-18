from src.components.transform import Transform
from src.components.wraparound import Wraparound


class WraparoundSystem:
    def update(self, world, dt: float) -> None:
        del dt
        for _, (transform, wraparound) in world.get_components(Transform, Wraparound):
            if wraparound.horizontal:
                world_width = float(wraparound.world_width)
                if world_width > 0:
                    transform.position.x %= world_width
            if wraparound.vertical and wraparound.world_height is not None:
                if transform.position.y < -wraparound.margin:
                    transform.position.y = wraparound.world_height + wraparound.margin
                elif transform.position.y > wraparound.world_height + wraparound.margin:
                    transform.position.y = -wraparound.margin
