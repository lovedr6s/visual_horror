from turtle import st
import pygame
from game.level_settings import load_level, save_level
WHITE = (255, 255, 255)
GRAY = (138, 10, 10)
DARK_GRAY = (100, 100, 100)

class Button:
    def __init__(self, text, pos, size, callback):
        self.rect = pygame.Rect(pos, size)
        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        color = DARK_GRAY if self.hovered else GRAY
        font = pygame.font.Font('game/text_box/fonts/font.otf', 30)
        pygame.draw.rect(surface, color, self.rect, border_radius=0)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos, mouse_click):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_click:
            self.callback()

def _load_and_exit_menu(state):
    state['level'] = load_level()
    state['is_menu'] = False

def _save_and_exit_menu(state):
    save_level(state['level'])
    state['is_menu'] = False

def _reset_game(state):
    state['level'] = 0
    state['is_menu'] = False

def create_menu_buttons(state):
    load_button = Button("Load", (50, 400), (200, 50), lambda: _load_and_exit_menu(state))
    save_button = Button("Save", (300, 400), (200, 50), lambda: _save_and_exit_menu(state))
    quit_button = Button("Quit", (550, 400), (200, 50), lambda: pygame.quit())
    reset_game = Button("Reset Game", (250, 500), (300, 50), lambda: _reset_game(state))
    return [load_button, save_button, quit_button, reset_game]


def menu(display, buttons):
    for button in buttons:
        button.draw(display)
        button.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
