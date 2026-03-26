import pygame
from config import *

class EndScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.result = ''
        self.score = 0

    def show(self):
        self.screen.fill(SKY_BLUE)
        title = self.font.render('Game Over', True, (0,0,0))
        self.screen.blit(title, (SCREEN_WIDTH//2 - 80, 80))

        res_text = self.font.render(self.result, True, (200,0,0))
        self.screen.blit(res_text, (SCREEN_WIDTH//2 - 80, 140))

        score_text = self.font.render(f'Score: {self.score}', True, (0,0,0))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - 80, 200))

        info = self.font.render('Press Enter to go back to menu', True, (0,0,0))
        self.screen.blit(info, (SCREEN_WIDTH//2 - 160, 300))

        pygame.display.flip()
