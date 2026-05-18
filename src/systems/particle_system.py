import pygame

from src.components.lifetime import Lifetime
from src.components.particle import Particle
from src.components.renderable import Renderable


class ParticleSystem:
    def update(self, world, dt: float) -> None:
        for _, (particle, lifetime, renderable) in world.get_components(Particle, Lifetime, Renderable):
            ratio = 1.0 - (lifetime.remaining / particle.lifetime_max) if particle.lifetime_max > 0 else 1.0
            ratio = max(0.0, min(1.0, ratio))
            sc, ec = particle.start_color, particle.end_color
            renderable.color = pygame.Color(
                int(sc[0] + (ec[0] - sc[0]) * ratio),
                int(sc[1] + (ec[1] - sc[1]) * ratio),
                int(sc[2] + (ec[2] - sc[2]) * ratio),
            )
