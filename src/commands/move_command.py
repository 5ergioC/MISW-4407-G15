from __future__ import annotations

import pygame

from src.commands.command import Command
from src.components.player import Player
from src.components.input_command import InputCommand, CommandPhase


class MoveCommand(Command):
    def __init__(self, axis: pygame.Vector2) -> None:
        self.axis = axis

    def execute(self, world, is_pressed: bool) -> None:
        value = self.axis if is_pressed else pygame.Vector2()

        for _, (player,) in world.get_components(Player):
            # Actualizar entrada de empuje en el eje X
            if self.axis.x != 0:
                player.thrust_input.x = value.x

            # Actualizar entrada de empuje en el eje Y
            if self.axis.y != 0:
                player.thrust_input.y = value.y

            # Actualizar dirección visual si hay movimiento horizontal
            if value.x != 0:
                player.facing = value.x

    def execute_with_phase(self, world, c_input: InputCommand) -> None:
        if c_input.phase not in (CommandPhase.START, CommandPhase.END):
            return

        for _, (player,) in world.get_components(Player):
            horizontal = 0.0
            vertical = 0.0

            for _, (command_input,) in world.get_components(InputCommand):
                if not command_input.active:
                    continue

                if command_input.name == "PLAYER_LEFT":
                    horizontal -= 1.0
                elif command_input.name == "PLAYER_RIGHT":
                    horizontal += 1.0
                elif command_input.name == "PLAYER_UP":
                    vertical -= 1.0
                elif command_input.name == "PLAYER_DOWN":
                    vertical += 1.0

            player.thrust_input.x = horizontal
            player.thrust_input.y = vertical

            if horizontal != 0.0:
                player.facing = horizontal
