import pygame

class Audio:
    """Gestão de carregamento e reprodução de sons."""
    def __init__(self):
        # Inicializa o mixer (se ainda não estiver)
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.sounds = {}

    def load(self, name: str, filepath: str):
        """
        Carrega um ficheiro de áudio (.wav, .ogg…) e associa-o a um nome.
        `name` é a chave para depois tocar o som.
        """
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Erro ao carregar som '{filepath}': {e}")

    def play(self, name: str):
        """
        Toca o som previamente carregado com a chave `name`.
        """
        sound = self.sounds.get(name)
        if sound:
            sound.play()
        else:
            print(f"Áudio: som '{name}' não encontrado.")