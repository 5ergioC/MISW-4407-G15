from src.components.animation import Animation
from src.components.particle import Particle
from src.components.renderable import Renderable
import pygame


class AnimationSystem:
    def update(self, world, dt: float) -> None:
        for entity, (animation, renderable) in world.get_components(Animation, Renderable):
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
            if world.has_component(entity, Particle):
                particle = world.component_for_entity(entity, Particle)
                if particle.kind == "enemy_death":
                    scale = 1.0 + animation.frame_index * 0.6
                    renderable.size = pygame.Vector2(8 * scale, 8 * scale)
                    alpha = max(0, 255 - animation.frame_index * 70)
                    renderable.color = pygame.Color(255, max(90, 210 - animation.frame_index * 30), 90, alpha)

