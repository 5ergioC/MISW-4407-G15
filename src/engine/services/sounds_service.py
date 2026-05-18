from __future__ import annotations

from pathlib import Path

import pygame


class SoundsService:
    def __init__(self, root_path: Path) -> None:
        self._root_path = root_path / "assets"
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._volume: float = 1.0

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            sound.set_volume(self._volume)

    def play(self, path: str) -> None:
        sound_path = self._root_path / path
        if not sound_path.exists():
            return
        if path not in self._sounds:
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(self._volume)
            self._sounds[path] = sound
        self._sounds[path].play()
