from __future__ import annotations

from pathlib import Path

import pygame


class TextsService:
    def __init__(self, root_path: Path) -> None:
        self._root_path = root_path / "assets"
        self._fonts: dict[tuple[str | None, int], pygame.font.Font] = {}
        self._renders: dict[tuple[str | None, int, str, tuple[int, int, int]], pygame.Surface] = {}

    def get_font(self, path: str | None, size: int) -> pygame.font.Font:
        key = (path, size)
        if key not in self._fonts:
            if path is None:
                self._fonts[key] = pygame.font.Font(None, size)
            else:
                self._fonts[key] = pygame.font.Font(self._root_path / path, size)
        return self._fonts[key]

    def render(
        self,
        path: str | None,
        size: int,
        text: str,
        color: tuple[int, int, int],
    ) -> pygame.Surface:
        key = (path, size, text, color)
        if key not in self._renders:
            font = self.get_font(path, size)
            self._renders[key] = font.render(text, True, color)
        return self._renders[key]
