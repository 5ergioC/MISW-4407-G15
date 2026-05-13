from __future__ import annotations

from src.commands.command import Command


class SmartBombCommand(Command):
    def __init__(self, on_smart_bomb) -> None:
        self.on_smart_bomb = on_smart_bomb

    def execute(self, world, is_pressed: bool) -> None:
        if is_pressed:
            self.on_smart_bomb(world)

