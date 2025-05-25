import pygame

class Audio:
    """Gestão de carregamento e reprodução de sons."""
    def __init__(self, initial_volume: float = 1.0):
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.sounds = {}
        self.volume = max(0.0, min(1.0, initial_volume))

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

    def set_volume(self, volume: float, name: str = None):
        """
        Define o volume master (0.0 a 1.0) para todos os sons carregados.
        """
        self.volume = max(0.0, min(1.0, volume))
        if name:
            sound = self.sounds.get(name)
            sound.set_volume(self.volume)
        else:
            for sound in self.sounds.values():
                sound.set_volume(self.volume)

    def get_volume(self) -> float:
        """
        Retorna o volume master atual.
        """
        return self.volume

    def volume_to(self, level: float, name: str = None):
        """
        Define o volume master para um valor específico (por exemplo, 0.3).
        """
        self.set_volume(level)
        if name:
            sound = self.sounds.get(name)