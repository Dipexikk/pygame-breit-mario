import pygame

def main_menu(screen):
    font = pygame.font.Font(None, 74)
    title_text = font.render("Breit Mario", True, (255, 255, 255))
    play_text = font.render("Press ENTER to Play", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))

    running = True
    while running:
        screen.fill((0, 0, 128))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))
        screen.blit(play_text, (screen.get_width() // 2 - play_text.get_width() // 2, 200))
        screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
