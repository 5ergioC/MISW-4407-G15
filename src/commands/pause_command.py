from __future__ import annotations

from src.commands.command import Command


class PauseCommand(Command):
    def __init__(self, on_pause) -> None:
        self.on_pause = on_pause

    def execute(self, world, is_pressed: bool) -> None:
        if is_pressed:
            self.on_pause()
