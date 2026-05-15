from __future__ import annotations

from typing import Callable

import pygame
import esper

from src.components.input_command import InputCommand, CommandPhase


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


def system_input_command(world: esper.World,
                          event: pygame.event.Event,
                          do_action: Callable[[InputCommand], None]) -> None:
    
    if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
        return

    components = world.get_components(InputCommand)

    for _, (c_input,) in components:
        if c_input.key == event.key:
            # Actualizar fase según el tipo de evento
            if event.type == pygame.KEYDOWN:
                c_input.phase = CommandPhase.START
                c_input.active = True
            elif event.type == pygame.KEYUP:
                c_input.phase = CommandPhase.END
                c_input.active = False

            # Ejecutar la acción con la nueva fase
            do_action(c_input)
