from __future__ import annotations

import pygame

from src.commands.move_command import MoveCommand
from src.components.camera import Camera
from src.components.input_command import InputCommand, CommandPhase
from src.core.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.factories.entity_factory import (
    create_audio_event,
    create_input_commands,
    create_player_death_fx,
    create_planet,
    create_player,
    create_starfield,
)
from src.components.tag import Tag
from src.components.player import Player
from src.components.enemy import Enemy
from src.components.astronaut import Astronaut
from src.components.state import State
from src.components.renderable import Renderable
from src.components.transform import Transform
from src.components.velocity import Velocity
from src.systems.abduction_system import AbductionSystem
from src.systems.animation_system import AnimationSystem
from src.systems.astronaut_system import AstronautSystem
from src.systems.audio_system import AudioSystem
from src.systems.background_system import BackgroundSystem
from src.systems.bonus.debug_system import DebugSystem
from src.systems.bonus.reward_system import RewardSystem
from src.systems.bonus.smart_bomb_system import SmartBombSystem
from src.systems.camera_system import CameraSystem
from src.systems.collision_system import CollisionSystem
from src.systems.enemy_spawn_system import EnemySpawnSystem
from src.systems.enemy_fire_system import EnemyFireSystem
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
        self.enemy_fire_system = EnemyFireSystem()
        self.lander_ai_system = LanderAISystem()
        self.mutant_ai_system = MutantAISystem()
        self.abduction_system = AbductionSystem()
        self.astronaut_system = AstronautSystem()
        self.gravity_system = GravitySystem()
        self.projectile_system = ProjectileSystem()
        self.collision_system = CollisionSystem()
        self.particle_system = ParticleSystem()
        self.smart_bomb_system = SmartBombSystem()
        self.debug_system = DebugSystem()
        self.reward_system = RewardSystem()
        self.scoring_system = ScoringSystem()
        self.pause_visibility_system = PauseVisibilitySystem()
        self.movement_system = PlayerMovementSystem()
        self.velocity_system = MovementSystem()
        self.wraparound_system = WraparoundSystem()
        self.lifetime_system = LifetimeSystem()
        self.shooting_system = ShootingSystem()
        self.player_respawn_delay = 2.2
        self.player_respawn_timer = 0.0
        self.player_dying = False
        self.player_death_outcome: str | None = None
        self._player_exploded = False
        self._player_flash_timer = 0.0
        self._player_flash_duration = 0.45
        self._create_world()
        self.enemy_fire_disabled = not self.enemy_fire_system.enabled

    def _create_world(self) -> None:
        create_starfield(self.world)
        create_planet(self.world)
        create_player(self.world)
        create_input_commands(self.world)
        create_audio_event(self.world, "snd/game_start.ogg")

    def _reset_run_after_player_death(self) -> None:
        self.world.clear_database()
        self.enemy_spawn_system.reset()
        self.player_respawn_timer = 0.0
        self.player_dying = False
        self.player_death_outcome = None
        self._player_exploded = False
        self._player_flash_timer = 0.0
        self._create_world()

    def _on_player_enemy_collision(self, player_position: pygame.Vector2) -> None:
        if self.player_dying:
            return
        lives = max(0, int(self.engine.shared_state["lives"]) - 1)
        self.engine.shared_state["lives"] = lives
        self.player_death_outcome = "respawn" if lives > 0 else "game_over"
        self.player_dying = True
        self.player_respawn_timer = self.player_respawn_delay
        self._player_exploded = False
        self._player_flash_timer = 0.0
        ServiceLocator.sounds_service.play(ServiceLocator.config.get("audio")["sounds"]["player_die"])
        for _, (_, velocity, player, renderable) in self.world.get_components(Transform, Velocity, Player, Renderable):
            velocity.value = pygame.Vector2(0, 0)
            renderable.color = pygame.Color(255, 50, 50)

    # Death animation: frame timings (seconds per blink step)
    _DEATH_BLINK = 0.09   # on/off duration per blink
    _DEATH_FRAMES = 3     # frames in player_death.png

    def _update_player_death_flash(self, dt: float) -> None:
        if self._player_exploded:
            return
        self._player_flash_timer += dt

        # Sequence per frame: on-off-on-off = 4 blinks = 4 * 2 * BLINK seconds
        blinks_per_frame = 2
        step_duration = self._DEATH_BLINK
        frame_duration = blinks_per_frame * 2 * step_duration  # 0.36s per frame
        total_flash = self._DEATH_FRAMES * frame_duration       # 1.08s total

        t = self._player_flash_timer
        if t >= total_flash:
            # Trigger explosion
            self._player_exploded = True
            for _, (transform, _, player, renderable) in self.world.get_components(Transform, Velocity, Player, Renderable):
                renderable.visible = False
                # hide burner too
                if player.burner_entity >= 0 and self.world.has_component(player.burner_entity, Renderable):
                    self.world.component_for_entity(player.burner_entity, Renderable).visible = False
                from src.factories.entity_factory import create_explosion
                create_explosion(
                    self.world, transform.position.copy(),
                    kind="player", count=80,
                    speed_min=30, speed_max=200,
                    lifetime_min=0.7, lifetime_max=1.5,
                    radius_min=1.5, radius_max=3.5,
                    spawn_radius=6.0,
                )
            return

        frame_idx = int(t / frame_duration)
        frame_idx = min(frame_idx, self._DEATH_FRAMES - 1)
        time_in_frame = t % frame_duration
        blink_on = int(time_in_frame / step_duration) % 2 == 0

        has_death_sprite = ServiceLocator.images_service.has("img/player_death.png") if hasattr(ServiceLocator.images_service, "has") else False
        try:
            ServiceLocator.images_service.get("img/player_death.png")
            has_death_sprite = True
        except Exception:
            has_death_sprite = False

        for _, (_, _, player, renderable) in self.world.get_components(Transform, Velocity, Player, Renderable):
            renderable.visible = blink_on
            if blink_on:
                if has_death_sprite:
                    renderable.image_path = "img/player_death.png"
                    sheet = ServiceLocator.images_service.get("img/player_death.png")
                    fw = max(1, sheet.get_width() // self._DEATH_FRAMES)
                    renderable.sprite_frame_width = fw
                    renderable.sprite_frame = frame_idx
                else:
                    renderable.color = pygame.Color(255, 50, 50)
            # hide burner during death
            if player.burner_entity >= 0 and self.world.has_component(player.burner_entity, Renderable):
                self.world.component_for_entity(player.burner_entity, Renderable).visible = False

    def _finish_player_respawn(self) -> None:
        if self.player_death_outcome == "game_over":
            self.engine.shared_state["game_over_reason"] = "No lives left"
            self.switch_to("game_over")
            return
        self._reset_run_after_player_death()

    def _toggle_pause(self) -> None:
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
            self.pause_visibility_system.set_paused(self.world, True)
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            self.pause_visibility_system.set_paused(self.world, False)

    def _use_smart_bomb(self) -> None:
        self.smart_bomb_system.activate(self.world, self.camera, self.engine.shared_state)

    def _set_boost(self, active: bool) -> None:
        for _, (player,) in self.world.get_components(Player):
            player.is_boosting = active

    def _do_action(self, c_input: InputCommand) -> None:
        move_commands = {
            "PLAYER_LEFT":  MoveCommand(pygame.Vector2(-1, 0)),
            "PLAYER_RIGHT": MoveCommand(pygame.Vector2(1, 0)),
            "PLAYER_UP":    MoveCommand(pygame.Vector2(0, -1)),
            "PLAYER_DOWN":  MoveCommand(pygame.Vector2(0, 1)),
        }

        if c_input.name in move_commands:
            move_commands[c_input.name].execute_with_phase(self.world, c_input)

        elif c_input.name == "PLAYER_FIRE":
            if c_input.phase == CommandPhase.START:
                self.shooting_system.fire(self.world)

        elif c_input.name == "PLAYER_PAUSE":
            if c_input.phase == CommandPhase.START:
                self._toggle_pause()

        elif c_input.name == "PLAYER_SMART_BOMB":
            if c_input.phase == CommandPhase.START:
                self._use_smart_bomb()

        elif c_input.name == "TOGGLE_ENEMY_FIRE":
            if c_input.phase == CommandPhase.START:
                self.enemy_fire_system.enabled = not getattr(self.enemy_fire_system, "enabled", True)
                self.enemy_fire_disabled = not self.enemy_fire_system.enabled

        elif c_input.name == "PLAYER_LOSE_LIFE":
            if c_input.phase == CommandPhase.START:
                lives = int(self.engine.shared_state["lives"])
                self.engine.shared_state["lives"] = max(0, lives - 1)
                if self.engine.shared_state["lives"] <= 0:
                    self.engine.shared_state["game_over_reason"] = "No lives left"
                    self.switch_to("game_over")

        elif c_input.name == "PLAYER_WIN":
            if c_input.phase == CommandPhase.START:
                self.engine.reset_run_state()
                self.switch_to("win")

        elif c_input.name == "PLAYER_MENU":
            if c_input.phase == CommandPhase.START:
                self.switch_to("menu")

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            self.debug_system.toggle()
        system_input_command(self.world, event, self._do_action)

    def update(self, dt: float) -> None:
        if self.state == GameState.PAUSED:
            return
        if self.player_dying:
            self.player_respawn_timer -= dt
            self._update_player_death_flash(dt)
            self.particle_system.update(self.world, dt)
            self.animation_system.update(self.world, dt)
            self.lifetime_system.update(self.world, dt)
            self.audio_system.update(self.world, dt)
            if self.player_respawn_timer <= 0.0:
                self._finish_player_respawn()
            return
        self.shooting_system.update(dt)
        self.enemy_spawn_system.update(self.world, dt)
        self.enemy_fire_system.set_wave_context(self.enemy_spawn_system.current_wave())
        self.lander_ai_system.update(self.world, dt)
        self.mutant_ai_system.update(self.world, dt)
        self.enemy_fire_system.update(self.world, dt, self.camera)
        self.abduction_system.update(self.world, dt)
        self.astronaut_system.update(self.world, dt)
        self.gravity_system.update(self.world, dt)
        self.movement_system.update(self.world, dt)
        self.velocity_system.update(self.world, dt)
        self.projectile_system.update(self.world, dt)
        self.wraparound_system.update(self.world, dt)
        self.collision_system.update(self.world, dt, self.camera, self._on_player_enemy_collision)
        self.particle_system.update(self.world, dt)
        self.animation_system.update(self.world, dt)
        self.planet_system.update(self.world, dt)
        self.camera_system.update(self.world, dt)
        self.scoring_system.update(self.world, self.engine.shared_state)
        self.reward_system.update(self.world, self.engine.shared_state)
        self.lifetime_system.update(self.world, dt)
        self.audio_system.update(self.world, dt)
        self._evaluate_run_outcome()

    def render(self) -> None:
        surface = self.virtual_screen
        self.background_system.render(surface)
        gameplay_clip = pygame.Rect(
            0,
            self.hud_system.hud_bottom + 1,
            surface.get_width(),
            surface.get_height() - (self.hud_system.hud_bottom + 1),
        )
        previous_clip = surface.get_clip()
        surface.set_clip(gameplay_clip)
        self.planet_system.render(self.world, surface, self.camera)
        self.render_system.render(self.world, surface, self.camera)
        surface.set_clip(previous_clip)

        for _, (_, _, player) in self.world.get_components(Transform, Velocity, Player):
            player.is_shooting = False

        enemy_count = sum(1 for _, (tag,) in self.world.get_components(Tag) if tag.has("enemy"))
        astronaut_count = sum(
            1 for _, (astronaut, tag) in self.world.get_components(Astronaut, Tag)
            if tag.has("astronaut") and astronaut.state != "dead"
        )

        abduction_world_x = None
        for _, (transform, enemy, state, tag) in self.world.get_components(Transform, Enemy, State, Tag):
            if not tag.has("enemy") or enemy.kind != "lander":
                continue
            if state.name in {"abducting", "ascending"} or enemy.alerting:
                abduction_world_x = transform.position.x
                break

        self.hud_system.render(
            surface,
            self.engine.shared_state,
            self.state == GameState.PAUSED,
            self.camera,
            self.planet_system.points,
            self.world,
            enemy_count,
            astronaut_count,
            self.enemy_fire_disabled,
            abduction_world_x,
        )
        self.debug_system.render(self.world, surface, self.camera)

    def _evaluate_run_outcome(self) -> None:
        live_astronauts = 0
        for _, (astronaut, tag) in self.world.get_components(Astronaut, Tag):
            if tag.has("astronaut") and astronaut.state != "dead":
                live_astronauts += 1
        if live_astronauts <= 0:
            self.engine.shared_state["game_over_reason"] = "All astronauts lost"
            self.switch_to("game_over")
            return
        if self.enemy_spawn_system.is_campaign_complete(self.world):
            self.switch_to("win")
