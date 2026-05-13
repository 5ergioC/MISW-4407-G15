from __future__ import annotations

import pygame

from src.commands.command import Command
from src.components.player import Player


class MoveCommand(Command):
    def __init__(self, axis: pygame.Vector2) -> None:
        self.axis = axis

    def execute(self, world, is_pressed: bool) -> None:
        value = self.axis if is_pressed else pygame.Vector2()
        for _, (player,) in world.get_components(Player):
            if self.axis.x != 0:
                player.thrust_input.x = value.x
            if self.axis.y != 0:
                player.thrust_input.y = value.y
            if value.x != 0:
                player.facing = value.x
