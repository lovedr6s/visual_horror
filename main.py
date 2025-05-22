import pygame
from game.text_box.box import scene
from game.level_settings import load_text_file
from game.game_menu import menu, create_menu_buttons


pygame.init()
display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Horror Game")
clock = pygame.time.Clock()
content = load_text_file('game/text_box/dialoges/text.json')


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
    buttons = create_menu_buttons(state)  # ← теперь передаём состояние

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
