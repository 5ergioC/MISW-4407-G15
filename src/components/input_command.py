from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import pygame


class CommandPhase(Enum):
    NA = 0        # Sin acción
    START = 1     # Tecla presionada
    END = 2       # Tecla liberada


@dataclass
class InputCommand:
    name: str
    key: int
    phase: CommandPhase = field(default=CommandPhase.NA)
    active: bool = field(default=False)
    mouse_pos: pygame.Vector2 | None = field(default=None)
