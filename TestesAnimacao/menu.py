import pygame
import sys
import subprocess
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maestro em Treino")

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (240, 240, 240)
BLUE = (50, 100, 255)
HOVER_BLUE = (30, 80, 220)
DARK_BLUE = (20, 40, 100)
SHADOW = (0, 0, 0, 100)

font_large = pygame.font.SysFont('Georgia', 60, bold=True)
font_medium = pygame.font.SysFont('Verdana', 28)
font_small = pygame.font.SysFont('Verdana', 22)

def draw_gradient_background():
    for y in range(SCREEN_HEIGHT):
        color = (
            255 - y // 3,
            255 - y // 5,
            255
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

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

        color = HOVER_BLUE if self.is_hovered else BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        pygame.draw.rect(surface, DARK_BLUE, self.rect, 2, border_radius=10)

        text_surf = font_medium.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def execute_action(self):
        if self.action:
            print(f"Executando: {self.action}")
            try:
                if self.action.endswith(".py"):
                    pygame.quit()
                    subprocess.run([sys.executable, self.action])
                    pygame.init()
                    global screen
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                elif self.action == "exit":
                    pygame.quit()
                    sys.exit()
            except Exception as e:
                print(f"Erro ao executar o script: {e}")

def main_menu():
    buttons = [
        Button(SCREEN_WIDTH // 2 - 150, 240, 300, 60, "Jogar", "instrument_menu.py"),
        Button(SCREEN_WIDTH // 2 - 150, 320, 300, 60, "Tutorial", "harmonica_tutorial.py"),
        Button(SCREEN_WIDTH // 2 - 150, 400, 300, 60, "Sair", "exit")
    ]

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
                        if button.action != "exit":
                            running = False

        draw_gradient_background()

        title = font_large.render("Maestro em Treino", True, DARK_BLUE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    while True:
        main_menu()