from __future__ import annotations

import pygame

from src.commands.move_command import MoveCommand
from src.commands.pause_command import PauseCommand
from src.commands.scene_command import SceneCommand
from src.commands.shoot_command import ShootCommand
from src.core.scene import Scene
from src.factories.entity_factory import create_player, create_starfield
from src.systems.audio_system import AudioSystem
from src.systems.background_system import BackgroundSystem
from src.systems.hud_system import HUDSystem
from src.systems.input_command_system import InputCommandSystem
from src.systems.lifetime_system import LifetimeSystem
from src.systems.movement_system import MovementSystem
from src.systems.player_movement_system import PlayerMovementSystem
from src.systems.render_system import RenderSystem
from src.systems.shooting_system import ShootingSystem
from src.systems.wraparound_system import WraparoundSystem
from src.states.game_state import GameState


class PlayScene(Scene):
    def enter(self) -> None:
        self.world.clear_database()
        self.state = GameState.PLAYING
        self.background_system = BackgroundSystem()
        self.render_system = RenderSystem()
        self.hud_system = HUDSystem()
        self.audio_system = AudioSystem()
        self.movement_system = PlayerMovementSystem()
        self.velocity_system = MovementSystem()
        self.wraparound_system = WraparoundSystem()
        self.lifetime_system = LifetimeSystem()
        self.shooting_system = ShootingSystem()
        self._create_world()
        self.input_system = InputCommandSystem(
            {
                pygame.K_LEFT: MoveCommand(pygame.Vector2(-1, 0)),
                pygame.K_RIGHT: MoveCommand(pygame.Vector2(1, 0)),
                pygame.K_UP: MoveCommand(pygame.Vector2(0, -1)),
                pygame.K_DOWN: MoveCommand(pygame.Vector2(0, 1)),
                pygame.K_SPACE: ShootCommand(self.shooting_system.fire),
                pygame.K_p: PauseCommand(self._toggle_pause),
                pygame.K_ESCAPE: SceneCommand(lambda: self.switch_to("menu")),
            }
        )

    def _create_world(self) -> None:
        create_starfield(self.world)
        create_player(self.world)

    def _toggle_pause(self) -> None:
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def handle_event(self, event: pygame.event.Event) -> None:
        self.input_system.process_event(self.world, event)

    def update(self, dt: float) -> None:
        if self.state == GameState.PAUSED:
            return
        self.shooting_system.update(dt)
        self.movement_system.update(self.world, dt)
        self.velocity_system.update(self.world, dt)
        self.wraparound_system.update(self.world, dt)
        self.lifetime_system.update(self.world, dt)
        self.audio_system.update(self.world, dt)

    def render(self) -> None:
        surface = self.virtual_screen
        self.background_system.render(surface)
        self.render_system.render(self.world, surface)
        self.hud_system.render(surface, self.engine.shared_state, self.state == GameState.PAUSED)
