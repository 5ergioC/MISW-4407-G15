from src.components.enemy import Enemy
from src.components.player import Player
from src.components.projectile import Projectile
from src.components.renderable import Renderable


class PauseVisibilitySystem:
    def set_paused(self, world, paused: bool) -> None:
        # TODO(P1): Keep background visible and hide player, enemies, and projectiles while paused.
        for entity, (renderable,) in world.get_components(Renderable):
            if (
                world.has_component(entity, Player)
                or world.has_component(entity, Enemy)
                or world.has_component(entity, Projectile)
            ):
                renderable.visible = not paused

