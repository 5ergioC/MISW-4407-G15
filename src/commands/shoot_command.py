from __future__ import annotations

from src.commands.command import Command


class ShootCommand(Command):
    def __init__(self, on_shoot) -> None:
        self.on_shoot = on_shoot

    def execute(self, world, is_pressed: bool) -> None:
        if is_pressed:
            self.on_shoot(world)
