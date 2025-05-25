import pygame
import math


class Input:
    def __init__(self):
        self._quit = False
        self._key_down_list = []
        self._key_pressed_list = []
        self._key_up_list = []
        # Mouse control
        self._mouse_position = (0, 0)
        self._mouse_rel = (0, 0)
        self._mouse_captured = False

    @property
    def key_down_list(self):
        return self._key_down_list

    @property
    def key_pressed_list(self):
        return self._key_pressed_list

    @property
    def key_up_list(self):
        return self._key_up_list

    @property
    def quit(self):
        return self._quit

    @property
    def mouse_position(self):
        return self._mouse_position

    @property
    def mouse_rel(self):
        return self._mouse_rel

    @property
    def mouse_captured(self):
        return self._mouse_captured

    def is_key_down(self, key_code):
        return key_code in self._key_down_list

    def is_key_pressed(self, key_code):
        return key_code in self._key_pressed_list

    def is_key_up(self, key_code):
        return key_code in self._key_up_list

    def update(self):
        self._key_down_list = []
        self._key_up_list = []
        self._mouse_rel = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True

            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                self._key_down_list.append(key_name)
                self._key_pressed_list.append(key_name)
                if key_name == "escape":
                    self._mouse_captured = not self._mouse_captured
                    pygame.mouse.set_visible(not self._mouse_captured)
                    if self._mouse_captured:
                        pygame.mouse.set_pos(pygame.display.get_surface().get_rect().center)

            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                if key_name in self._key_pressed_list:
                    self._key_pressed_list.remove(key_name)
                self._key_up_list.append(key_name)

            if event.type == pygame.MOUSEMOTION:
                self._mouse_position = event.pos
                self._mouse_rel = event.rel