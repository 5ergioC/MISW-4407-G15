from __future__ import annotations

import pygame
from src.components.camera import Camera
from src.engine.service_locator import ServiceLocator


class HUDSystem:
    def __init__(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        raw_lives_icon = ServiceLocator.images_service.get("img/interface_lives.png")
        scaled_size = (
            max(1, round(raw_lives_icon.get_width() * 0.7)),
            max(1, round(raw_lives_icon.get_height() * 0.7)),
        )
        scaled_lives_icon = pygame.transform.smoothscale(raw_lives_icon, scaled_size)
        self.lives_icon = pygame.mask.from_surface(scaled_lives_icon).to_surface(
            setcolor=(255, 255, 255, 255),
            unsetcolor=(0, 0, 0, 0),
        )
        self.lives_icon = ServiceLocator.images_service.get("img/interface_lives.png")

    def render(
        self,
        surface: pygame.Surface,
        shared_state: dict[str, object],
        paused: bool,
        camera: Camera | None = None,
        planet_points: list[tuple[float, float]] | None = None,
    ) -> None:
        self._render_scanner(surface, camera, planet_points or [])
        font_path = self.interface_cfg["font"]["path"]
        pause_color = self.interface_cfg["pause_text_color"]
        text_color = (255, 244, 72)
        score_text = ServiceLocator.texts_service.render(font_path, 16, f"{shared_state['score']:05}", text_color)
        enemies_text = ServiceLocator.texts_service.render(font_path, 8, "ENEMIES 0", text_color)
        surface.blit(score_text, (26, 16))
        self._render_lives(surface, int(shared_state["lives"]))
        surface.blit(enemies_text, (236, 7))
        if paused and pygame.time.get_ticks() // 250 % 2 == 0:
            paused_text = ServiceLocator.texts_service.render(
                font_path, 10, "PAUSED", (pause_color["r"], pause_color["g"], pause_color["b"])
            )
            rect = paused_text.get_rect(center=(160, 118))
            surface.blit(paused_text, rect)

    def _render_lives(self, surface: pygame.Surface, lives: int) -> None:
        icon = self.lives_icon
        font_path = self.interface_cfg["font"]["path"]
        text_color = (255, 255, 255)
        label = ServiceLocator.texts_service.render(font_path, 6, "LIVES", text_color)
        label_rect = label.get_rect(topleft=(8, 3))
        surface.blit(label, label_rect)

        icon_y = 12
        icon_x = 8
        spacing = max(5, icon.get_width() + 3)
        for index in range(max(0, lives)):
            surface.blit(icon, (icon_x + index * spacing, icon_y))

    def _render_scanner(
        self,
        surface: pygame.Surface,
        camera: Camera | None,
        planet_points: list[tuple[float, float]],
    ) -> None:
        green = pygame.Color(52, 174, 45)
        orange = pygame.Color(205, 106, 42)
        hud_bottom = 42
        scanner = pygame.Rect(90, 1, 144, hud_bottom - 2)
        pygame.draw.line(surface, green, (0, hud_bottom), (320, hud_bottom), 2)
        pygame.draw.rect(surface, green, scanner, 2)
        pygame.draw.rect(surface, green, pygame.Rect(234, 1, 86, hud_bottom - 2), 2)
        if camera is None or not planet_points:
            return
        scale_x = scanner.width / camera.world_width
        min_y = min(y for _, y in planet_points)
        max_y = max(y for _, y in planet_points)
        height = max(1.0, max_y - min_y)
        scaled_points = []
        for world_x, world_y in planet_points:
            x = scanner.left + world_x * scale_x
            y = scanner.bottom - 4 - ((max_y - world_y) / height) * (scanner.height - 10)
            if scanner.left <= x <= scanner.right:
                scaled_points.append((x, y))
        if len(scaled_points) > 1:
            pygame.draw.lines(surface, orange, False, scaled_points, 1)
        view_x = scanner.left + (camera.x % camera.world_width) * scale_x
        view_w = max(6, camera.width * scale_x)
        pygame.draw.line(surface, pygame.Color(245, 245, 245), (view_x, scanner.top), (view_x + view_w, scanner.top), 2)
        pygame.draw.line(surface, pygame.Color(245, 245, 245), (view_x, scanner.bottom), (view_x + view_w, scanner.bottom), 2)
