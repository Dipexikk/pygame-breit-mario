import pygame
from config import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)
        self.small = pygame.font.SysFont(None, 24)
        self.selected = 0

        self.control_choice = 'both'
        self.options = ['WASD', 'ARROWS', 'BOTH', 'START']
        self.last_score = None


        self.items_rects = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
            if event.key == pygame.K_DOWN:
                self.selected = min(len(self.options)-1, self.selected + 1)
            if event.key == pygame.K_RETURN:
                return self.activate_selected()
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i, r in enumerate(self.items_rects):
                if r.collidepoint(mx, my):
                    self.selected = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i, r in enumerate(self.items_rects):
                if r.collidepoint(mx, my):
                    self.selected = i
                    return self.activate_selected()
        if event.type == pygame.QUIT:
            return 'quit'
        return None

    def activate_selected(self):
        if self.selected == 0:
            self.control_choice = 'wasd'
        elif self.selected == 1:
            self.control_choice = 'arrows'
        elif self.selected == 2:
            self.control_choice = 'both'
        elif self.selected == 3:
            return 'start'
        return None

    def draw(self):

        top = (70,130,180)
        bottom = SKY_BLUE
        for i in range(SCREEN_HEIGHT):
            ratio = i / SCREEN_HEIGHT
            r = int(top[0] * (1-ratio) + bottom[0] * ratio)
            g = int(top[1] * (1-ratio) + bottom[1] * ratio)
            b = int(top[2] * (1-ratio) + bottom[2] * ratio)
            pygame.draw.line(self.screen, (r,g,b), (0,i), (SCREEN_WIDTH,i))


        title_surf = self.font.render('Kočičárna', True, (255,255,255))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title_surf, title_rect)


        sub = self.small.render('Choose controls and press Start', True, (240,240,240))
        sub_rect = sub.get_rect(center=(SCREEN_WIDTH//2, 120))
        self.screen.blit(sub, sub_rect)


        self.items_rects = []
        btn_w = 260
        btn_h = 56
        start_y = 180
        gap = 80
        for i, opt in enumerate(self.options):
            cx = SCREEN_WIDTH//2
            cy = start_y + i*gap
            rect = pygame.Rect(0,0,btn_w,btn_h)
            rect.center = (cx, cy)

            if i == self.selected:
                pygame.draw.rect(self.screen, (255,80,80), rect, border_radius=12)
                text = self.font.render(opt, True, (255,255,255))
            else:
                pygame.draw.rect(self.screen, (255,255,255,50), rect, border_radius=12)
                pygame.draw.rect(self.screen, (220,220,220), rect, 2, border_radius=12)
                text = self.font.render(opt, True, (40,40,40))
            txt_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, txt_rect)
            self.items_rects.append(rect)


        info = self.small.render(f'Controls: {self.control_choice}', True, (255,255,255))
        self.screen.blit(info, (SCREEN_WIDTH//2 - 120, start_y + len(self.options)*gap))
        if self.last_score is not None:
            score_text = self.small.render(f'Last score: {self.last_score}', True, (255,255,255))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - 120, start_y + len(self.options)*gap + 30))

        pygame.display.flip()
