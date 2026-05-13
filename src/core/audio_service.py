from __future__ import annotations

from pathlib import Path

import pygame


class AudioService:
    def __init__(self, root_path: Path) -> None:
        self._root_path = root_path / "assets"
        self._sounds: dict[str, pygame.mixer.Sound] = {}

    def play(self, relative_path: str) -> None:
        path = self._root_path / relative_path
        if not path.exists():
            return
        if relative_path not in self._sounds:
            self._sounds[relative_path] = pygame.mixer.Sound(path)
        self._sounds[relative_path].play()
