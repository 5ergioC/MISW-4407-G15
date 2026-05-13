from __future__ import annotations

import pygame


class InputCommandSystem:
    def __init__(self, bindings: dict[int, object]) -> None:
        self.bindings = bindings

    def process_event(self, world, event: pygame.event.Event) -> None:
        if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
            return
        command = self.bindings.get(event.key)
        if command is None:
            return
        command.execute(world, event.type == pygame.KEYDOWN)
