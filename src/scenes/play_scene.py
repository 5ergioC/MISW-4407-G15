from __future__ import annotations

import pygame

from src.components.camera import Camera
from src.commands.bonus.smart_bomb_command import SmartBombCommand
from src.commands.move_command import MoveCommand
from src.commands.pause_command import PauseCommand
from src.commands.scene_command import SceneCommand
from src.commands.shoot_command import ShootCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import create_audio_event, create_planet, create_player, create_starfield
from src.systems.abduction_system import AbductionSystem
from src.systems.animation_system import AnimationSystem
from src.systems.astronaut_system import AstronautSystem
from src.systems.audio_system import AudioSystem
from src.systems.background_system import BackgroundSystem
from src.systems.camera_system import CameraSystem
from src.systems.collision_system import CollisionSystem
from src.systems.enemy_spawn_system import EnemySpawnSystem
from src.systems.gravity_system import GravitySystem
from src.systems.hud_system import HUDSystem
from src.systems.input_command_system import InputCommandSystem
from src.systems.lander_ai_system import LanderAISystem
from src.systems.lifetime_system import LifetimeSystem
from src.systems.movement_system import MovementSystem
from src.systems.mutant_ai_system import MutantAISystem
from src.systems.particle_system import ParticleSystem
from src.systems.pause_visibility_system import PauseVisibilitySystem
from src.systems.player_movement_system import PlayerMovementSystem
from src.systems.planet_system import PlanetSystem
from src.systems.projectile_system import ProjectileSystem
from src.systems.render_system import RenderSystem
from src.systems.bonus.smart_bomb_system import SmartBombSystem
from src.systems.scoring_system import ScoringSystem
from src.systems.shooting_system import ShootingSystem
from src.systems.wraparound_system import WraparoundSystem
from src.states.game_state import GameState


class PlayScene(Scene):
    def enter(self) -> None:
        self.world.clear_database()
        self.state = GameState.PLAYING
        world_cfg = ServiceLocator.config.get("world")
        window_cfg = ServiceLocator.config.get("window")
        player_cfg = ServiceLocator.config.get("player")
        virtual_size = window_cfg["virtual_size"]
        self.camera = Camera(
            width=virtual_size["w"],
            height=virtual_size["h"],
            world_width=world_cfg["width"],
            smoothness=player_cfg["camera"]["smoothness"],
            look_ahead_speed_threshold=player_cfg["camera"]["look_ahead_speed_threshold"],
        )
        self.background_system = BackgroundSystem()
        self.planet_system = PlanetSystem()
        self.render_system = RenderSystem()
        self.animation_system = AnimationSystem()
        self.hud_system = HUDSystem()
        self.audio_system = AudioSystem()
        self.camera_system = CameraSystem(self.camera)
        self.enemy_spawn_system = EnemySpawnSystem()
        self.lander_ai_system = LanderAISystem()
        self.mutant_ai_system = MutantAISystem()
        self.abduction_system = AbductionSystem()
        self.astronaut_system = AstronautSystem()
        self.gravity_system = GravitySystem()
        self.projectile_system = ProjectileSystem()
        self.collision_system = CollisionSystem()
        self.particle_system = ParticleSystem()
        self.smart_bomb_system = SmartBombSystem()
        self.scoring_system = ScoringSystem()
        self.pause_visibility_system = PauseVisibilitySystem()
        self.movement_system = PlayerMovementSystem()
        self.velocity_system = MovementSystem()
        self.wraparound_system = WraparoundSystem()
        self.lifetime_system = LifetimeSystem()
        self.shooting_system = ShootingSystem()
        self._create_world()
        self.input_system = InputCommandSystem(
            {
                pygame.K_LEFT: MoveCommand(pygame.Vector2(-1, 0)),
                pygame.K_a: MoveCommand(pygame.Vector2(-1, 0)),
                pygame.K_RIGHT: MoveCommand(pygame.Vector2(1, 0)),
                pygame.K_d: MoveCommand(pygame.Vector2(1, 0)),
                pygame.K_UP: MoveCommand(pygame.Vector2(0, -1)),
                pygame.K_w: MoveCommand(pygame.Vector2(0, -1)),
                pygame.K_DOWN: MoveCommand(pygame.Vector2(0, 1)),
                pygame.K_s: MoveCommand(pygame.Vector2(0, 1)),
                pygame.K_SPACE: ShootCommand(self.shooting_system.fire),
                pygame.K_b: SmartBombCommand(self._use_smart_bomb),
                pygame.K_p: PauseCommand(self._toggle_pause),
                pygame.K_ESCAPE: SceneCommand(lambda: self.switch_to("menu")),
            }
        )

    def _create_world(self) -> None:
        create_starfield(self.world)
        create_planet(self.world)
        create_player(self.world)
        create_audio_event(self.world, "snd/game_start.ogg")

    def _use_smart_bomb(self, world) -> None:
        self.smart_bomb_system.activate(world, self.camera, self.engine.shared_state)

    def _toggle_pause(self) -> None:
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
            self.pause_visibility_system.set_paused(self.world, True)
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            self.pause_visibility_system.set_paused(self.world, False)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.input_system.process_event(self.world, event)

    def update(self, dt: float) -> None:
        if self.state == GameState.PAUSED:
            return
        self.shooting_system.update(dt)
        self.enemy_spawn_system.update(self.world, dt)
        self.lander_ai_system.update(self.world, dt)
        self.mutant_ai_system.update(self.world, dt)
        self.abduction_system.update(self.world, dt)
        self.astronaut_system.update(self.world, dt)
        self.gravity_system.update(self.world, dt)
        self.movement_system.update(self.world, dt)
        self.velocity_system.update(self.world, dt)
        self.projectile_system.update(self.world, dt)
        self.wraparound_system.update(self.world, dt)
        self.collision_system.update(self.world, dt)
        self.particle_system.update(self.world, dt)
        self.animation_system.update(self.world, dt)
        self.planet_system.update(self.world, dt)
        self.camera_system.update(self.world, dt)
        self.scoring_system.update(self.world, self.engine.shared_state)
        self.lifetime_system.update(self.world, dt)
        self.audio_system.update(self.world, dt)

    def render(self) -> None:
        surface = self.virtual_screen
        self.background_system.render(surface)
        self.planet_system.render(self.world, surface, self.camera)
        self.render_system.render(self.world, surface, self.camera)
        self.hud_system.render(
            surface,
            self.engine.shared_state,
            self.state == GameState.PAUSED,
            self.camera,
            self.planet_system.points,
            self.world,
        )
