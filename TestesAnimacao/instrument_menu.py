import pygame
import sys
import subprocess
import os
from menu import SCREEN_WIDTH, SCREEN_HEIGHT, screen, draw_gradient_background, Button, font_large, DARK_BLUE


def instrument_menu():
    # Define buttons for each instrument
    buttons = [
        Button(SCREEN_WIDTH // 2 - 150, 180, 300, 60, "Harmónica", "harmonica.py"),
        Button(SCREEN_WIDTH // 2 - 150, 260, 300, 60, "Gaita", "gaita.py"),
        Button(SCREEN_WIDTH // 2 - 150, 340, 300, 60, "Concertina", "concertina.py"),
        Button(SCREEN_WIDTH // 2 - 150, 420, 300, 60, "Triângulo", "triangulo.py")
    ]

    # Set window title
    font_large = pygame.font.SysFont(None, 75)
    pygame.display.set_caption("Selecione o seu instrumento")
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.execute_action()

        # Update hover state
        for button in buttons:
            button.check_hover(mouse_pos)

        # Draw background and title
        draw_gradient_background()
        title_surf = font_large.render("Selecione o seu instrumento", True, DARK_BLUE)
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 80))

        # Draw instrument buttons
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    instrument_menu()
