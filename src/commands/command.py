from __future__ import annotations

from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, world, is_pressed: bool) -> None:
        raise NotImplementedError
