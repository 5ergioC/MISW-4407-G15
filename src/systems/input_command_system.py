from __future__ import annotations

from typing import Callable

import esper
import pygame

from src.components.input_command import CommandPhase, InputCommand


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


def system_input_command(
    world: esper.World,
    event: pygame.event.Event,
    do_action: Callable[[InputCommand], None],
) -> None:
    if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
        return

    components = world.get_components(InputCommand)
    for _, (c_input,) in components:
        if c_input.key != event.key:
            continue

        if event.type == pygame.KEYDOWN:
            if c_input.active:
                return
            c_input.phase = CommandPhase.START
            c_input.active = True
        else:
            c_input.phase = CommandPhase.END
            c_input.active = False

        do_action(c_input)
