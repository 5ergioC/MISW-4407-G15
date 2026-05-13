from src.components.lifetime import Lifetime


class LifetimeSystem:
    def update(self, world, dt: float) -> None:
        dead_entities: list[int] = []
        for entity, (lifetime,) in world.get_components(Lifetime):
            lifetime.remaining -= dt
            if lifetime.remaining <= 0:
                dead_entities.append(entity)
        for entity in dead_entities:
            world.delete_entity(entity, immediate=True)
