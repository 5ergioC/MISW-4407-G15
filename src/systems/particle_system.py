from __future__ import annotations

import pygame

from src.components.lifetime import Lifetime
from src.components.particle import Particle
from src.components.renderable import Renderable


class ParticleSystem:
    def update(self, world, dt: float) -> None:
        del dt
        rainbow = (
            pygame.Color(255, 231, 88),
            pygame.Color(96, 162, 255),
            pygame.Color(255, 97, 68),
        )
        for _, (particle, renderable, lifetime) in world.get_components(Particle, Renderable, Lifetime):
            if particle.kind != "score_popup":
                continue
            color_index = int((lifetime.remaining * 18) % len(rainbow))
            renderable.color = rainbow[color_index]
            renderable.visible = int(lifetime.remaining * 24) % 2 == 0
