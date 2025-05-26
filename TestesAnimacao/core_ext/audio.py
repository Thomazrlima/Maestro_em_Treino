import pygame

class Audio:
    def __init__(self, initial_volume: float = 2.0):
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.sounds = {}
        self.master_volume = max(0.0, min(2.0, initial_volume))

    def load(self, name: str, filepath: str, volume: float = None):
        try:
            sound = pygame.mixer.Sound(filepath)
            init_vol = self.master_volume if volume is None else max(0.0, min(2.0, volume))
            sound.set_volume(init_vol)
            self.sounds[name] = {"sound": sound, "volume": init_vol}
        except pygame.error as e:
            print(f"Erro ao carregar som '{filepath}': {e}")

    def play(self, name: str):
        entry = self.sounds.get(name)
        if entry:
            entry["sound"].play()
        else:
            print(f"Áudio: som '{name}' não encontrado.")

    def set_master_volume(self, volume: float):
        self.master_volume = max(0.0, min(2.0, volume))
        for entry in self.sounds.values():
            entry["sound"].set_volume(entry["volume"] * self.master_volume)

    def get_master_volume(self) -> float:
        return self.master_volume

    def set_sound_volume(self, name: str, volume: float):
        entry = self.sounds.get(name)
        if entry:
            ivol = max(0.0, min(2.0, volume))
            entry["volume"] = ivol
            entry["sound"].set_volume(ivol * self.master_volume)
        else:
            print(f"Áudio: som '{name}' não encontrado.")

    def get_sound_volume(self, name: str) -> float:
        entry = self.sounds.get(name)
        if entry:
            return entry["volume"]
        print(f"Áudio: som '{name}' não encontrado.")
        return 0.0

    def volume_to(self, level: float):
        self.set_master_volume(level)