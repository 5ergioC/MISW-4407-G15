from __future__ import annotations

import pygame

class HUDSystem:
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 16)
        self.big_font = pygame.font.Font(None, 24)

    def render(self, surface: pygame.Surface, shared_state: dict[str, object], paused: bool) -> None:
        score_text = self.font.render(f"SCORE {shared_state['score']:05}", True, pygame.Color("white"))
        lives_text = self.font.render(f"LIVES {shared_state['lives']}", True, pygame.Color("white"))
        enemies_text = self.font.render("ENEMIES 0", True, pygame.Color("white"))
        surface.blit(score_text, (8, 8))
        surface.blit(lives_text, (124, 8))
        surface.blit(enemies_text, (224, 8))
        if paused and pygame.time.get_ticks() // 250 % 2 == 0:
            paused_text = self.big_font.render("PAUSED", True, pygame.Color(255, 80, 80))
            rect = paused_text.get_rect(center=(160, 40))
            surface.blit(paused_text, rect)
