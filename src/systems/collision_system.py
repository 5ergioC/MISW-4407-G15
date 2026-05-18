from __future__ import annotations

import pygame

from src.components.astronaut import Astronaut
from src.components.collider import Collider
from src.components.camera import Camera
from src.components.enemy import Enemy
from src.components.player import Player
from src.components.projectile import Projectile
from src.components.renderable import Renderable
from src.components.score_value import ScoreValue
from src.components.state import State
from src.components.tag import Tag
from src.components.transform import Transform
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_astronaut_death_fx, create_enemy_death_fx, create_score_event


class CollisionSystem:
    def update(self, world, dt: float, camera: Camera, on_player_enemy_collision=None) -> None:
        del dt

        players = list(world.get_components(Transform, Collider, Player, Renderable))
        projectiles = list(world.get_components(Transform, Collider, Projectile, Renderable))
        enemies = list(world.get_components(Transform, Collider, Renderable, Tag))
        enemy_projectiles = list(world.get_components(Transform, Collider, Projectile, Renderable))
        astronauts = list(world.get_components(Transform, Collider, Astronaut, Renderable, Tag))
        if enemies and projectiles:
            enemies_to_delete: set[int] = set()
            player_projectiles_to_delete: set[int] = set()
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
                    player_projectiles_to_delete.add(projectile_entity)
                    self._release_carried_astronaut(world, enemy_entity)
                    if world.has_component(enemy_entity, ScoreValue):
                        create_score_event(world, world.component_for_entity(enemy_entity, ScoreValue).amount)
                    create_enemy_death_fx(world, pygame.Vector2(enemy_rect.centerx, enemy_rect.centery))
                    if enemy_death_sound:
                        ServiceLocator.sounds_service.play(enemy_death_sound)

            for enemy_entity in enemies_to_delete:
                world.delete_entity(enemy_entity, immediate=True)
            for projectile_entity in player_projectiles_to_delete:
                world.delete_entity(projectile_entity, immediate=True)

        if enemy_projectiles and projectiles:
            enemy_projectiles_to_delete: set[int] = set()
            player_projectiles_to_delete: set[int] = set()
            for projectile_entity, (projectile_transform, projectile_collider, projectile_component, projectile_renderable) in projectiles:
                if projectile_component.owner != "player":
                    continue
                projectile_rect = self._build_rect(projectile_transform, projectile_collider, projectile_renderable)
                for enemy_projectile_entity, (enemy_projectile_transform, enemy_projectile_collider, enemy_projectile_component, enemy_projectile_renderable) in enemy_projectiles:
                    if enemy_projectile_component.owner != "enemy":
                        continue
                    enemy_projectile_rect = self._build_rect(enemy_projectile_transform, enemy_projectile_collider, enemy_projectile_renderable)
                    if not projectile_rect.colliderect(enemy_projectile_rect):
                        continue
                    enemy_projectiles_to_delete.add(enemy_projectile_entity)
                    player_projectiles_to_delete.add(projectile_entity)
                    score_cfg = ServiceLocator.config.get("scoring")
                    if enemy_projectile_component.kind == "missile":
                        create_score_event(world, int(score_cfg.get("enemy_missile_destroyed", 0)))
                    else:
                        create_score_event(world, int(score_cfg.get("enemy_bullet_destroyed", 0)))
            for entity in enemy_projectiles_to_delete:
                world.delete_entity(entity, immediate=True)
            for entity in player_projectiles_to_delete:
                world.delete_entity(entity, immediate=True)

        if astronauts and projectiles:
            astronauts_to_hide: set[int] = set()
            player_projectiles_to_delete: set[int] = set()
            for projectile_entity, (projectile_transform, projectile_collider, projectile_component, projectile_renderable) in projectiles:
                if projectile_component.owner != "player":
                    continue
                projectile_rect = self._build_rect(projectile_transform, projectile_collider, projectile_renderable)
                for astronaut_entity, (astronaut_transform, astronaut_collider, astronaut_component, astronaut_renderable, astronaut_tag) in astronauts:
                    if not astronaut_tag.has("astronaut") or astronaut_component.state == "dead":
                        continue
                    astronaut_rect = self._build_rect(astronaut_transform, astronaut_collider, astronaut_renderable)
                    if not projectile_rect.colliderect(astronaut_rect):
                        continue
                    self._clear_astronaut_bindings(world, astronaut_entity, astronaut_component)
                    astronaut_component.state = "dead"
                    astronaut_renderable.visible = False
                    create_astronaut_death_fx(world, astronaut_transform.position.copy())
                    astronauts_to_hide.add(astronaut_entity)
                    player_projectiles_to_delete.add(projectile_entity)
                    create_score_event(world, int(ServiceLocator.config.get("scoring").get("accidental_astronaut_kill", 0)))
            for astronaut_entity in astronauts_to_hide:
                if world.has_component(astronaut_entity, State):
                    world.component_for_entity(astronaut_entity, State).name = "dead"
            for projectile_entity in player_projectiles_to_delete:
                world.delete_entity(projectile_entity, immediate=True)

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
                self._release_carried_astronaut(world, enemy_entity)
                enemy_renderable.visible = False
                create_enemy_death_fx(world, pygame.Vector2(enemy_rect.centerx, enemy_rect.centery))
                if enemy_death_sound:
                    ServiceLocator.sounds_service.play(enemy_death_sound)
                world.delete_entity(enemy_entity, immediate=True)
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

    def _release_carried_astronaut(self, world, enemy_entity: int) -> None:
        if not world.has_component(enemy_entity, Enemy):
            return
        enemy = world.component_for_entity(enemy_entity, Enemy)
        astronaut_entity = enemy.carried_entity
        if astronaut_entity is None or not world.has_component(astronaut_entity, Astronaut):
            return

        astronaut = world.component_for_entity(astronaut_entity, Astronaut)
        astronaut.state = "falling"
        astronaut.carrier_entity = None
        astronaut.fall_start_y = world.component_for_entity(astronaut_entity, Transform).position.y
        if world.has_component(astronaut_entity, State):
            astronaut_state = world.component_for_entity(astronaut_entity, State)
            astronaut_state.name = "falling"
            astronaut_state.elapsed = 0.0
        if world.has_component(astronaut_entity, Renderable):
            world.component_for_entity(astronaut_entity, Renderable).visible = True

    def _clear_astronaut_bindings(self, world, astronaut_entity: int, astronaut: Astronaut) -> None:
        carrier_entity = astronaut.carrier_entity
        if carrier_entity is None:
            return

        if world.has_component(carrier_entity, Player):
            player = world.component_for_entity(carrier_entity, Player)
            if player.carried_astronaut == astronaut_entity:
                player.carried_astronaut = None

        if world.has_component(carrier_entity, Enemy):
            enemy = world.component_for_entity(carrier_entity, Enemy)
            if enemy.carried_entity == astronaut_entity:
                enemy.carried_entity = None
            if enemy.target_entity == astronaut_entity:
                enemy.target_entity = None
                enemy.alerting = False

        astronaut.carrier_entity = None
