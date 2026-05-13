from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

from src.core.ecs_world import ECSWorld

if TYPE_CHECKING:
    from src.core.engine import GameEngine


class Scene(ABC):
    def __init__(self, engine: GameEngine) -> None:
        self.engine = engine
        self.world = ECSWorld()
        self.next_scene_name: str | None = None

    @property
    def screen(self) -> pygame.Surface:
        return self.engine.screen

    @property
    def virtual_screen(self) -> pygame.Surface:
        return self.engine.virtual_screen

    @property
    def window_config(self) -> dict:
        return self.engine.window_config

    def switch_to(self, scene_name: str) -> None:
        self.next_scene_name = scene_name

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        self.world.clear_database()

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError
