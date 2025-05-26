import pygame
import sys
import subprocess
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Selecione o seu instrumento")

BUTTON_COLOR = (200, 0, 0)
HOVER_COLOR = (255, 50, 50)
BORDER_COLOR = (150, 0, 0)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (100, 0, 0)

IMAGE_DIR = "images"
IMAGE_PATHS = {
    "Mapa": os.path.join(IMAGE_DIR, "mapa.png"),
    "Harmónica": os.path.join(IMAGE_DIR, "harmonica.png"),
    "Gaita": os.path.join(IMAGE_DIR, "gaita.png"),
    "Concertina": os.path.join(IMAGE_DIR, "sanfona.png"),
    "Triângulo": os.path.join(IMAGE_DIR, "triangulo.png")
}
CURTAIN_IMAGE_PATH = os.path.join(IMAGE_DIR, "cortina.jpeg")

font_title = pygame.font.SysFont('Georgia', 50, bold=True)
font_button = pygame.font.SysFont('Verdana', 28)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False

    def draw(self, surface):
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(surface, SHADOW_COLOR, shadow_rect, border_radius=10)

        color = HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, 2, border_radius=10)

        text_surf = font_button.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

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
                pygame.init()

def load_images():
    images = {}
    for name, path in IMAGE_PATHS.items():
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (50, 50))
            images[name] = img
    return images

def instrument_menu():
    buttons = [
        Button(SCREEN_WIDTH // 2 - 150, 180, 300, 60, "Mapa", "Mapa.py"),
        Button(SCREEN_WIDTH // 2 - 150, 260, 300, 60, "Harmónica", "harmonica.py"),
        Button(SCREEN_WIDTH // 2 - 150, 340, 300, 60, "Gaita", "gaita.py"),
        Button(SCREEN_WIDTH // 2 - 150, 420, 300, 60, "Concertina", "concertina.py"),
        Button(SCREEN_WIDTH // 2 - 150, 500, 300, 60, "Triângulo", "triangulo.py")
    ]

    images = load_images()

    curtain_image = None
    if os.path.exists(CURTAIN_IMAGE_PATH):
        curtain_image = pygame.image.load(CURTAIN_IMAGE_PATH)
        curtain_image = pygame.transform.scale(curtain_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
                            return

        for button in buttons:
            button.check_hover(mouse_pos)

        if curtain_image:
            screen.blit(curtain_image, (0, 0))
        else:
            screen.fill((0, 0, 0))

        title_surf = font_title.render("Selecione o seu instrumento", True, TEXT_COLOR)
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 80))

        for button in buttons:
            button.draw(screen)
            img = images.get(button.text)
            if img:
                img_y = button.rect.y + (button.rect.height - img.get_height()) // 2
                img_x = button.rect.x - img.get_width() - 10

                shadow_offset = 3
                shadow_pos = (img_x + shadow_offset, img_y + shadow_offset)
                shadow_surf = img.copy()
                shadow_surf.fill((0, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(shadow_surf, shadow_pos)

                screen.blit(img, (img_x, img_y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    while True:
        instrument_menu()
