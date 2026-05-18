from src.components.animation import Animation
from src.components.renderable import Renderable


class AnimationSystem:
    def update(self, world, dt: float) -> None:
        for _, (animation, renderable) in world.get_components(Animation, Renderable):
            animation.elapsed += dt
            if animation.elapsed < animation.frame_time:
                continue
            animation.elapsed = 0.0
            if animation.frame_count > 0:
                # spritesheet mode — advance frame_index, sync to renderable
                animation.frame_index += 1
                if animation.frame_index >= animation.frame_count:
                    animation.frame_index = 0 if animation.loop else animation.frame_count - 1
                renderable.sprite_frame = animation.frame_index
            elif animation.frames:
                # path-list mode
                animation.frame_index += 1
                if animation.frame_index >= len(animation.frames):
                    animation.frame_index = 0 if animation.loop else len(animation.frames) - 1
                renderable.image_path = animation.frames[animation.frame_index]

