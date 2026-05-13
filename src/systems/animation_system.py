from src.components.animation import Animation
from src.components.renderable import Renderable


class AnimationSystem:
    def update(self, world, dt: float) -> None:
        # TODO(P4): Advance sprite frames and update Renderable when spritesheets/frames are wired.
        for _, (animation, renderable) in world.get_components(Animation, Renderable):
            if not animation.frames:
                continue
            animation.elapsed += dt
            if animation.elapsed < animation.frame_time:
                continue
            animation.elapsed = 0.0
            animation.frame_index += 1
            if animation.frame_index >= len(animation.frames):
                animation.frame_index = 0 if animation.loop else len(animation.frames) - 1
            del renderable

