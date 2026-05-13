from __future__ import annotations

from pathlib import Path

import pygame


class SoundsService:
    def __init__(self, root_path: Path) -> None:
        self._root_path = root_path / "assets"
        self._sounds: dict[str, pygame.mixer.Sound] = {}

    def play(self, path: str) -> None:
        sound_path = self._root_path / path
        if not sound_path.exists():
            return
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(sound_path)
        self._sounds[path].play()
