from src.components.camera import Camera, CameraTarget
from src.components.player import Player
from src.components.transform import Transform
from src.components.velocity import Velocity


class CameraSystem:
    def __init__(self, camera: Camera) -> None:
        self.camera = camera

    def update(self, world, dt: float) -> None:
        for _, (transform, player, target, velocity) in world.get_components(Transform, Player, CameraTarget, Velocity):
            if abs(velocity.value.x) >= self.camera.look_ahead_speed_threshold:
                self.camera.look_direction = 1.0 if velocity.value.x > 0 else -1.0
            desired_x = transform.position.x - self.camera.width / 2 + target.look_ahead_x * self.camera.look_direction
            self.camera.x = self._lerp_wrapped(self.camera.x, desired_x, dt)
            self.camera.x %= self.camera.world_width
            self.camera.y = 0.0
            break

    def _lerp_wrapped(self, current: float, target: float, dt: float) -> float:
        half_world = self.camera.world_width / 2
        delta = (target - current + half_world) % self.camera.world_width - half_world
        factor = min(1.0, self.camera.smoothness * dt)
        return current + delta * factor
