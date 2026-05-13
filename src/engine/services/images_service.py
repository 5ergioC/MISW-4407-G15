from __future__ import annotations

from pathlib import Path

import pygame


class ImagesService:
    def __init__(self, root_path: Path) -> None:
        self._root_path = root_path / "assets"
        self._images: dict[str, pygame.Surface] = {}

    def get(self, path: str) -> pygame.Surface:
        if path not in self._images:
            self._images[path] = pygame.image.load(self._root_path / path).convert_alpha()
        return self._images[path]
