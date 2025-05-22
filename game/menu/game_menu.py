import pygame
from game.level_settings import load_level, save_level


RED = (130, 10, 10)
GRAY = (138, 100, 100)
DARK_GRAY = (100, 100, 0)
text_font = "game/fonts/font.otf"


class Button:
    def __init__(self, text, pos, size, callback):
        self.rect = pygame.Rect(pos, size)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.sound = pygame.mixer.Sound("game/menu/sounds/button.mp3")

    def draw(self, surface):
        color = DARK_GRAY if self.hovered else GRAY
        font = pygame.font.Font(text_font, 30)
        pygame.draw.rect(surface, color, self.rect, border_radius=0)
        text_surf = font.render(self.text, True, RED)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos, mouse_click):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_click:
            self.sound.play()
            pygame.time.wait(1000)
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
    load_button = Button("Load", (50, 400), (200, 50),
                         lambda: _load_and_exit_menu(state))
    save_button = Button("Save", (300, 400), (200, 50),
                         lambda: _save_and_exit_menu(state))
    quit_button = Button("Quit", (550, 400), (200, 50),
                         lambda: pygame.quit())
    reset_game = Button("New Game", (250, 500), (300, 50),
                        lambda: _reset_game(state))
    return [load_button, save_button, quit_button, reset_game]


def menu(display, buttons, offset_x_y):
    text = pygame.font.Font(text_font, 50).render("Menu", True, RED)
    display.blit(text, (310, 100))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    real_mouse_position = mouse_x - offset_x_y[0], mouse_y - offset_x_y[1]
    for button in buttons:
        button.draw(display)
        button.update(real_mouse_position, pygame.mouse.get_pressed()[0])
