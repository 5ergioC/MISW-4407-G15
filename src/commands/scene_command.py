from __future__ import annotations

from src.commands.command import Command


class SceneCommand(Command):
    def __init__(self, callback) -> None:
        self.callback = callback

    def execute(self, world, is_pressed: bool) -> None:
        if is_pressed:
            self.callback()
