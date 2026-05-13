from __future__ import annotations

from pathlib import Path

import pygame


class AssetService:
    def __init__(self, root_path: Path) -> None:
        self._root_path = root_path / "assets"
        self._images: dict[str, pygame.Surface] = {}
        self._fonts: dict[tuple[str, int], pygame.font.Font] = {}

    def image(self, relative_path: str) -> pygame.Surface:
        if relative_path not in self._images:
            self._images[relative_path] = pygame.image.load(
                self._root_path / relative_path
            ).convert_alpha()
        return self._images[relative_path]

    def font(self, relative_path: str, size: int) -> pygame.font.Font:
        key = (relative_path, size)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(self._root_path / relative_path, size)
        return self._fonts[key]
