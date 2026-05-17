from __future__ import annotations

import pygame

from src.components.collider import Collider
from src.components.camera import Camera
from src.components.player import Player
from src.components.projectile import Projectile
from src.components.renderable import Renderable
from src.components.tag import Tag
from src.components.transform import Transform
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_enemy_death_fx


class CollisionSystem:
    def update(self, world, dt: float, camera: Camera, on_player_enemy_collision=None) -> None:
        del dt

        players = list(world.get_components(Transform, Collider, Player, Renderable))
        projectiles = list(world.get_components(Transform, Collider, Projectile, Renderable))
        enemies = list(world.get_components(Transform, Collider, Renderable, Tag))
        enemy_projectiles = list(world.get_components(Transform, Collider, Projectile, Renderable))
        if enemies and projectiles:
            enemies_to_delete: set[int] = set()
            enemy_death_sound = ServiceLocator.config.get("audio")["sounds"].get("enemy_die")
            for projectile_entity, (projectile_transform, projectile_collider, projectile_component, projectile_renderable) in projectiles:
                if projectile_component.owner != "player":
                    continue
                projectile_rect = self._build_rect(projectile_transform, projectile_collider, projectile_renderable)
                for enemy_entity, (enemy_transform, enemy_collider, enemy_renderable, enemy_tag) in enemies:
                    if enemy_entity in enemies_to_delete or not enemy_tag.has("enemy"):
                        continue
                    if not self._is_on_screen(enemy_transform, enemy_collider, enemy_renderable, camera):
                        continue
                    enemy_rect = self._build_rect(enemy_transform, enemy_collider, enemy_renderable)
                    if not projectile_rect.colliderect(enemy_rect):
                        continue
                    enemies_to_delete.add(enemy_entity)
                    create_enemy_death_fx(world, pygame.Vector2(enemy_rect.centerx, enemy_rect.centery))
                    if enemy_death_sound:
                        ServiceLocator.sounds_service.play(enemy_death_sound)

            for enemy_entity in enemies_to_delete:
                world.delete_entity(enemy_entity, immediate=True)

        if players and enemy_projectiles:
            enemy_projectiles_to_delete: set[int] = set()
            for projectile_entity, (projectile_transform, projectile_collider, projectile_component, projectile_renderable) in enemy_projectiles:
                if projectile_component.owner != "enemy":
                    continue
                projectile_rect = self._build_rect(projectile_transform, projectile_collider, projectile_renderable)
                for player_entity, (player_transform, player_collider, player_component, player_renderable) in players:
                    player_rect = self._build_rect(player_transform, player_collider, player_renderable)
                    if not projectile_rect.colliderect(player_rect):
                        continue
                    enemy_projectiles_to_delete.add(projectile_entity)
                    del player_entity
                    if on_player_enemy_collision is not None:
                        on_player_enemy_collision(player_transform.position.copy())
                    for projectile_entity in enemy_projectiles_to_delete:
                        world.delete_entity(projectile_entity, immediate=True)
                    return

        if not players or not enemies:
            return

        enemy_death_sound = ServiceLocator.config.get("audio")["sounds"].get("enemy_die")
        for player_entity, (player_transform, player_collider, player_component, player_renderable) in players:
            player_rect = self._build_rect(player_transform, player_collider, player_renderable)
            for enemy_entity, (enemy_transform, enemy_collider, enemy_renderable, enemy_tag) in enemies:
                if not enemy_tag.has("enemy"):
                    continue
                if not self._is_on_screen(enemy_transform, enemy_collider, enemy_renderable, camera):
                    continue
                enemy_rect = self._build_rect(enemy_transform, enemy_collider, enemy_renderable)
                if not player_rect.colliderect(enemy_rect):
                    continue
                enemy_renderable.visible = False
                create_enemy_death_fx(world, pygame.Vector2(enemy_rect.centerx, enemy_rect.centery))
                if enemy_death_sound:
                    ServiceLocator.sounds_service.play(enemy_death_sound)
                del player_entity
                del enemy_entity
                if on_player_enemy_collision is not None:
                    on_player_enemy_collision(player_transform.position.copy())
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

    def _is_on_screen(self, transform: Transform, collider: Collider, renderable: Renderable, camera: Camera) -> bool:
        enemy_rect = self._build_rect(transform, collider, renderable)
        screen_x = self._world_to_screen_x(enemy_rect.x, camera)
        screen_rect = pygame.Rect(round(screen_x), enemy_rect.y - round(camera.y), enemy_rect.width, enemy_rect.height)
        viewport = pygame.Rect(0, 0, round(camera.width), round(camera.height))
        return screen_rect.colliderect(viewport)

    def _world_to_screen_x(self, x: float, camera: Camera) -> float:
        world_width = camera.world_width
        return (x - camera.x + world_width / 2) % world_width - world_width / 2
