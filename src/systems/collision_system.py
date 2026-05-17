from __future__ import annotations

import pygame

from src.components.collider import Collider
from src.components.player import Player
from src.components.renderable import Renderable
from src.components.tag import Tag
from src.components.transform import Transform


class CollisionSystem:
    def update(self, world, dt: float, on_player_enemy_collision=None) -> None:
        del dt

        players = list(world.get_components(Transform, Collider, Player, Renderable))
        enemies = list(world.get_components(Transform, Collider, Renderable, Tag))
        if not players or not enemies:
            return

        for player_entity, (player_transform, player_collider, player_component, player_renderable) in players:
            player_rect = self._build_rect(player_transform, player_collider, player_renderable)
            for enemy_entity, (enemy_transform, enemy_collider, enemy_renderable, enemy_tag) in enemies:
                if not enemy_tag.has("enemy"):
                    continue
                enemy_rect = self._build_rect(enemy_transform, enemy_collider, enemy_renderable)
                if not player_rect.colliderect(enemy_rect):
                    continue
                del player_entity
                del enemy_entity
                if on_player_enemy_collision is not None:
                    on_player_enemy_collision()
                return

    def _build_rect(self, transform: Transform, collider: Collider, renderable: Renderable) -> pygame.Rect:
        rect = pygame.Rect(
            round(transform.position.x + collider.offset.x),
            round(transform.position.y + collider.offset.y),
            max(1, round(collider.size.x)),
            max(1, round(collider.size.y)),
        )
        if renderable.centered:
            rect.center = (
                round(transform.position.x + collider.offset.x),
                round(transform.position.y + collider.offset.y),
            )
        return rect
