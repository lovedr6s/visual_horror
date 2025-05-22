import pygame
from game.text_box.box import scene
from game.level_settings import load_text_file
from game.menu.game_menu import menu, create_menu_buttons
import numpy as np


pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)
icon = pygame.image.load('game/.icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Horror Game")
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
content = load_text_file('game/text_box/dialoges/text.json')


def generate_white_noise(volume, sample_rate=44100):
    samples = sample_rate * 2
    noise = np.random.normal(0, 1, samples) * volume
    noise = np.clip(noise, -1.0, 1.0)
    wave = np.int16(noise * 32767)
    stereo_wave = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound(stereo_wave)


def update_scene(state, buttons):
    if state['is_menu']:
        menu(display, buttons)
    else:
        try:
            scene(display, content[state['level']])
        except IndexError:
            pass


def main():
    state = {
        'level': 0,
        'is_menu': True
    }
    buttons = create_menu_buttons(state)
    creepy_noise = generate_white_noise(volume=0.05)
    creepy_noise.play(loops=-1)
    while True:
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not state['is_menu']:
                    state['level'] += 1
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    state['level'] += 1
                if event.key == pygame.K_ESCAPE:
                    state['is_menu'] = not state['is_menu']

        update_scene(state, buttons)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
