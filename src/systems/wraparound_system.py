from src.components.transform import Transform
from src.components.wraparound import Wraparound


class WraparoundSystem:
    def update(self, world, dt: float) -> None:
        del dt
        for _, (transform, wraparound) in world.get_components(Transform, Wraparound):
            if wraparound.horizontal:
                if transform.position.x < -wraparound.margin:
                    transform.position.x = wraparound.world_width + wraparound.margin
                elif transform.position.x > wraparound.world_width + wraparound.margin:
                    transform.position.x = -wraparound.margin
            if wraparound.vertical and wraparound.world_height is not None:
                if transform.position.y < -wraparound.margin:
                    transform.position.y = wraparound.world_height + wraparound.margin
                elif transform.position.y > wraparound.world_height + wraparound.margin:
                    transform.position.y = -wraparound.margin
