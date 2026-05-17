from src.components.animation import Animation
from src.components.renderable import Renderable


class AnimationSystem:
    def update(self, world, dt: float) -> None:
        for _, (animation, renderable) in world.get_components(Animation, Renderable):
            frame_count = animation.frame_count if animation.frame_count > 0 else len(animation.frames)
            if frame_count <= 1:
                continue
            animation.elapsed += dt
            if animation.elapsed < animation.frame_time:
                continue
            animation.elapsed = 0.0
            animation.frame_index += 1
            if animation.frame_index >= frame_count:
                animation.frame_index = 0 if animation.loop else frame_count - 1
            del renderable

