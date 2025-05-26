import pygame
import sys
import subprocess
import os
from core_ext.audio import Audio

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maestro em Treino")

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (240, 240, 240)
BLUE = (50, 100, 255)
RED_DARK = (139, 0, 0)
RED_HOVER = (180, 30, 30)
DARK_RED_BORDER = (100, 0, 0)

font_large = pygame.font.SysFont('Georgia', 60, bold=True)
font_medium = pygame.font.SysFont('Verdana', 28)
font_small = pygame.font.SysFont('Verdana', 22)

IMAGE_DIR = "images"
PALCO_IMAGE_PATH = os.path.join(IMAGE_DIR, "palco.jpg")
palco_image = None
if os.path.exists(PALCO_IMAGE_PATH):
    palco_image = pygame.image.load(PALCO_IMAGE_PATH)
    palco_image = pygame.transform.scale(palco_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(surface, GRAY, shadow_rect, border_radius=10)

        color = RED_HOVER if self.is_hovered else RED_DARK
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        pygame.draw.rect(surface, DARK_RED_BORDER, self.rect, 2, border_radius=10)

        text_surf = font_medium.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

def main_menu():
    audio = Audio()
    audio.load(name='elevator', filepath='used_sounds/elevador.mp3')
    audio.set_master_volume(3)
    audio.play(name='elevator')

    buttons = [
        Button(SCREEN_WIDTH // 2 - 150, 240, 300, 60, "Jogar", "instrument_menu.py"),
        Button(SCREEN_WIDTH // 2 - 150, 320, 300, 60, "Tutorial", "harmonica_tutorial.py"),
        Button(SCREEN_WIDTH // 2 - 150, 400, 300, 60, "Sair", "exit")
    ]

    return buttons

def run_menu():
    buttons = main_menu()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        action = button.action
                        if action == "exit":
                            running = False
                            break
                        else:
                            pygame.quit()
                            subprocess.run([sys.executable, action])
                            sys.exit()

        if palco_image:
            screen.blit(palco_image, (0, 0))
        else:
            screen.fill(WHITE)

        title = font_large.render("Maestro em Treino", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_menu()
