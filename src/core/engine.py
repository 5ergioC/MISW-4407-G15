from __future__ import annotations

from pathlib import Path

import pygame

from src.engine.service_locator import ServiceLocator
from src.scenes.bonus.attract_scene import AttractScene
from src.scenes.bonus.high_score_scene import HighScoreScene
from src.scenes.game_over_scene import GameOverScene
from src.scenes.menu_scene import MenuScene
from src.scenes.play_scene import PlayScene
from src.scenes.win_scene import WinScene


class GameEngine:
    def __init__(self) -> None:
        self.root_path = Path(__file__).resolve().parents[2]
        ServiceLocator.bootstrap(self.root_path)

        self.window_config = ServiceLocator.config.get("window")
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        pygame.mixer.init()
        pygame.joystick.init()
        pygame.display.set_caption(self.window_config["title"])

        size = self.window_config["size"]
        virtual_size = self.window_config["virtual_size"]
        self.screen = pygame.display.set_mode((size["w"], size["h"]))
        self.virtual_screen = pygame.Surface((virtual_size["w"], virtual_size["h"]))
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_config["framerate"]
        self.bg_color = pygame.Color(
            self.window_config["bg_color"]["r"],
            self.window_config["bg_color"]["g"],
            self.window_config["bg_color"]["b"],
        )
        player_cfg = ServiceLocator.config.get("player")
        self.shared_state: dict[str, object] = {
            "score": 0,
            "lives": player_cfg["lives"],
            "smart_bombs": player_cfg.get("smart_bombs", 3),
            "_last_reward_milestone": 0,
            "wave": 0,
            "level_complete": False,
            "game_over_reason": "",
        }
        self.scenes = {
            "menu": MenuScene(self),
            "play": PlayScene(self),
            "game_over": GameOverScene(self),
            "win": WinScene(self),
            "high_score": HighScoreScene(self),
            "attract": AttractScene(self),
        }
        self.current_scene = self.scenes["menu"]

    def reset_run_state(self) -> None:
        player_cfg = ServiceLocator.config.get("player")
        self.shared_state["score"] = 0
        self.shared_state["lives"] = player_cfg["lives"]
        self.shared_state["smart_bombs"] = player_cfg.get("smart_bombs", 3)
        self.shared_state["_last_reward_milestone"] = 0
        self.shared_state["wave"] = 0
        self.shared_state["level_complete"] = False
        self.shared_state["game_over_reason"] = ""

    def run(self, start_scene_name: str) -> None:
        self.current_scene = self.scenes[start_scene_name]
        self.current_scene.enter()
        self.is_running = True
        while self.is_running:
            dt = self.clock.tick(self.framerate) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    self.current_scene.handle_event(event)
            self.current_scene.update(dt)
            self.virtual_screen.fill(self.bg_color)
            self.current_scene.render()
            pygame.transform.scale(self.virtual_screen, self.screen.get_size(), self.screen)
            pygame.display.flip()
            self._handle_scene_switch()
        self.current_scene.exit()
        pygame.quit()

    def _handle_scene_switch(self) -> None:
        next_scene_name = self.current_scene.next_scene_name
        if next_scene_name is None:
            return
        self.current_scene.exit()
        self.current_scene.next_scene_name = None
        self.current_scene = self.scenes[next_scene_name]
        self.current_scene.enter()
