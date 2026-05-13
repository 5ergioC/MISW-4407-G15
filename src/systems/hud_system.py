from __future__ import annotations

import pygame
from src.engine.service_locator import ServiceLocator

class HUDSystem:
    def __init__(self) -> None:
        self.interface_cfg = ServiceLocator.config.get("interface")

    def render(self, surface: pygame.Surface, shared_state: dict[str, object], paused: bool) -> None:
        font_path = self.interface_cfg["font"]["path"]
        normal_color = self.interface_cfg["normal_text_color"]
        pause_color = self.interface_cfg["pause_text_color"]
        text_color = (normal_color["r"], normal_color["g"], normal_color["b"])
        score_text = ServiceLocator.texts_service.render(font_path, 8, f"SCORE {shared_state['score']:05}", text_color)
        lives_text = ServiceLocator.texts_service.render(font_path, 8, f"LIVES {shared_state['lives']}", text_color)
        enemies_text = ServiceLocator.texts_service.render(font_path, 8, "ENEMIES 0", text_color)
        surface.blit(score_text, (8, 8))
        surface.blit(lives_text, (124, 8))
        surface.blit(enemies_text, (224, 8))
        if paused and pygame.time.get_ticks() // 250 % 2 == 0:
            paused_text = ServiceLocator.texts_service.render(
                font_path, 10, "PAUSED", (pause_color["r"], pause_color["g"], pause_color["b"])
            )
            rect = paused_text.get_rect(center=(160, 40))
            surface.blit(paused_text, rect)
