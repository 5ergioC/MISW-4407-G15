from __future__ import annotations

import pygame

from src.commands.move_command import MoveCommand
from src.components.camera import Camera
from src.components.input_command import InputCommand
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import (
    create_audio_event,
    create_input_commands,
    create_planet,
    create_player,
    create_starfield,
)
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
from src.systems.input_command_system import system_input_command
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
        self.scoring_system = ScoringSystem()
        self.pause_visibility_system = PauseVisibilitySystem()
        self.movement_system = PlayerMovementSystem()
        self.velocity_system = MovementSystem()
        self.wraparound_system = WraparoundSystem()
        self.lifetime_system = LifetimeSystem()
        self.shooting_system = ShootingSystem()
        self._create_world()

    def _create_world(self) -> None:
        create_starfield(self.world)
        create_planet(self.world)
        create_player(self.world)
        create_input_commands(self.world)
        create_audio_event(self.world, "snd/game_start.ogg")

    def _toggle_pause(self) -> None:
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
            self.pause_visibility_system.set_paused(self.world, True)
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            self.pause_visibility_system.set_paused(self.world, False)

    def _do_action(self, c_input: InputCommand) -> None:
        move_commands = {
            "PLAYER_LEFT": MoveCommand(pygame.Vector2(-1, 0)),
            "PLAYER_RIGHT": MoveCommand(pygame.Vector2(1, 0)),
            "PLAYER_UP": MoveCommand(pygame.Vector2(0, -1)),
            "PLAYER_DOWN": MoveCommand(pygame.Vector2(0, 1)),
        }

        if c_input.name in move_commands:
            move_commands[c_input.name].execute_with_phase(self.world, c_input)

        elif c_input.name == "PLAYER_FIRE":
            if hasattr(c_input, 'phase'):
                from src.components.input_command import CommandPhase
                if c_input.phase == CommandPhase.START:
                    self.shooting_system.fire(self.world)

        elif c_input.name == "PLAYER_PAUSE":
            from src.components.input_command import CommandPhase
            if c_input.phase == CommandPhase.START:
                self._toggle_pause()

        elif c_input.name == "PLAYER_WIN":
            from src.components.input_command import CommandPhase
            if c_input.phase == CommandPhase.START:
                self.engine.reset_run_state()
                self.switch_to("win")

        elif c_input.name == "PLAYER_MENU":
            from src.components.input_command import CommandPhase
            if c_input.phase == CommandPhase.START:
                self.switch_to("menu")

    def handle_event(self, event: pygame.event.Event) -> None:
        system_input_command(self.world, event, self._do_action)

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
        )
