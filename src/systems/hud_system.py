from __future__ import annotations

import pygame
from src.components.camera import Camera
from src.engine.service_locator import ServiceLocator


class HUDSystem:
    def __init__(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")
        self.world_cfg = ServiceLocator.config.get("world")
        self.hud_bottom = 42
        raw_lives_icon = ServiceLocator.images_service.get("img/interface_lives.png")

        scaled_size = (
            max(1, round(raw_lives_icon.get_width() * 1.2)),
            max(1, round(raw_lives_icon.get_height() * 1.2)),
        )

        scaled_lives_icon = pygame.transform.smoothscale(raw_lives_icon, scaled_size)
        self.lives_icon = scaled_lives_icon
        raw_smart_bomb_icon = ServiceLocator.images_service.get("img/interface_smart_bomb.png")
        smart_bomb_size = (
            max(1, round(raw_smart_bomb_icon.get_width() * 0.7)),
            max(1, round(raw_smart_bomb_icon.get_height() * 0.7)),
        )
        scaled_smart_bomb_icon = pygame.transform.smoothscale(raw_smart_bomb_icon, smart_bomb_size)
        self.smart_bomb_icon = scaled_smart_bomb_icon
        self.astronaut_icon = self._build_counter_icon("img/astronaut.png", frame_count=3, scale=0.82)

    def render(
        self,
        surface: pygame.Surface,
        shared_state: dict[str, object],
        paused: bool,
        camera: Camera | None = None,
        planet_points: list[tuple[float, float]] | None = None,
        enemy_count: int = 0,
        astronaut_count: int = 0,
        enemy_fire_disabled: bool = False,
        abduction_world_x: float | None = None,
    ) -> None:
        self._render_scanner(surface, camera, planet_points or [])
        font_path = self.interface_cfg["font"]["path"]
        pause_color = self.interface_cfg["pause_text_color"]
        score_text = ServiceLocator.texts_service.render(font_path, 8, f"{shared_state['score']:05}", (255, 255, 255))
        
        surface.blit(score_text, (10, 30))
        self._render_lives(surface, int(shared_state["lives"]))

        self._render_smart_bombs(surface, int(shared_state.get("smart_bombs", 0)))

        self._render_counts(surface, font_path, enemy_count, astronaut_count)
        if abduction_world_x is not None and camera is not None:
            self._render_abduction_arrow(surface, camera, abduction_world_x)
        if paused and pygame.time.get_ticks() // 250 % 2 == 0:
            paused_text = ServiceLocator.texts_service.render(
                font_path, 10, "PAUSED", (pause_color["r"], pause_color["g"], pause_color["b"])
            )
            rect = paused_text.get_rect(center=(160, 118))
            surface.blit(paused_text, rect)


        if enemy_fire_disabled:
            if (pygame.time.get_ticks() // 400) % 2 == 0:
                disabled_text = ServiceLocator.texts_service.render(font_path, 8, "ENEMY FIRE OFF", (220, 60, 60))
                drect = disabled_text.get_rect(center=(160, 12))
                surface.blit(disabled_text, drect)

    def _render_lives(self, surface: pygame.Surface, lives: int) -> None:
        icon = self.lives_icon
        font_path = self.interface_cfg["font"]["path"]
        text_color = (255, 255, 255)
        label = ServiceLocator.texts_service.render(font_path, 6, "LIVES", text_color)
        label_rect = label.get_rect(topleft=(8, 3))
        surface.blit(label, label_rect)

        icon_y = 12
        icon_x = 8
        spacing = max(8, icon.get_width() + 6)
        for index in range(max(0, lives)):
            surface.blit(icon, (icon_x + index * spacing, icon_y))

    def _render_smart_bombs(self, surface: pygame.Surface, smart_bombs: int) -> None:
        icon = self.smart_bomb_icon
        base_x = 234 - icon.get_width() - 150
        base_y = 16
        v_spacing = max(4, icon.get_height() + 4)
        for index in range(max(0, smart_bombs)):
            y = base_y + index * v_spacing
            surface.blit(icon, (base_x, y))

    def _render_counts(self, surface: pygame.Surface, font_path: str, enemy_count: int, astronaut_count: int) -> None:
        value_color = (255, 244, 72)
        enemies_value = ServiceLocator.texts_service.render(font_path, 8, f"{enemy_count:02}", value_color)
        astronauts_value = ServiceLocator.texts_service.render(font_path, 7, f"{astronaut_count:02}", value_color)
        surface.blit(enemies_value, enemies_value.get_rect(topright=(314, 10)))
        surface.blit(astronauts_value, astronauts_value.get_rect(topright=(314, 28)))

    def _render_scanner(
        self,
        surface: pygame.Surface,
        camera: Camera | None,
        planet_points: list[tuple[float, float]],
    ) -> None:
        green = pygame.Color(52, 174, 45)
        orange = pygame.Color(205, 106, 42)
        scanner = pygame.Rect(90, 1, 144, self.hud_bottom - 2)
        pygame.draw.line(surface, green, (0, self.hud_bottom), (320, self.hud_bottom), 2)
        pygame.draw.rect(surface, green, scanner, 2)
        pygame.draw.rect(surface, green, pygame.Rect(234, 1, 86, self.hud_bottom - 2), 2)
        if camera is None or not planet_points:
            return
        scale_x = scanner.width / camera.world_width
        world_height = float(self.world_cfg["height"])
        scaled_points = []
        for world_x, world_y in planet_points:
            x = scanner.left + world_x * scale_x
            relative_height = max(0.0, min(world_height, world_height - world_y))
            y = scanner.bottom - 3 - (relative_height / world_height) * (scanner.height - 8)
            if scanner.left <= x <= scanner.right:
                scaled_points.append((x, y))
        if len(scaled_points) > 1:
            pygame.draw.lines(surface, orange, False, scaled_points, 1)
        view_x = scanner.left + (camera.x % camera.world_width) * scale_x
        view_w = max(6, camera.width * scale_x)
        pygame.draw.line(surface, pygame.Color(245, 245, 245), (view_x, scanner.top), (view_x + view_w, scanner.top), 2)
        pygame.draw.line(surface, pygame.Color(245, 245, 245), (view_x, scanner.bottom), (view_x + view_w, scanner.bottom), 2)

    def _render_abduction_arrow(self, surface: pygame.Surface, camera: Camera, target_world_x: float) -> None:
        relative_x = (target_world_x - camera.x + camera.world_width / 2) % camera.world_width - camera.world_width / 2
        screen_x = round(relative_x)
        center_y = 56
        color = pygame.Color(255, 92, 64)
        if 0 <= screen_x <= camera.width:
            pygame.draw.polygon(
                surface,
                color,
                [(screen_x, center_y - 6), (screen_x - 5, center_y + 4), (screen_x + 5, center_y + 4)],
            )
            return

        if screen_x < 0:
            points = [(8, center_y), (20, center_y - 6), (20, center_y + 6)]
        else:
            points = [(312, center_y), (300, center_y - 6), (300, center_y + 6)]
        pygame.draw.polygon(surface, color, points)

    def _build_counter_icon(self, image_path: str, frame_count: int, scale: float) -> pygame.Surface:
        sheet = ServiceLocator.images_service.get(image_path)
        frame_width = max(1, sheet.get_width() // max(1, frame_count))
        frame = sheet.subsurface(pygame.Rect(0, 0, frame_width, sheet.get_height())).copy()
        target_size = (
            max(1, round(frame.get_width() * scale)),
            max(1, round(frame.get_height() * scale)),
        )
        if frame.get_size() != target_size:
            frame = pygame.transform.smoothscale(frame, target_size)
        return frame
