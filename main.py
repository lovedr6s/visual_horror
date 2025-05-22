import pygame
from game.text_box.box import scene
from game.level_settings import load_level, save_level, load_text_file


pygame.init()
display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Horror Game")
clock = pygame.time.Clock()
content = load_text_file('game/text_box/dialoges/text.json')

def update_scene(level):
    scene(display, content[level])

def main():
    level = load_level()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    level += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    level += 1
                if event.key == pygame.K_ESCAPE:
                    print("Escape key pressed")
        display.fill((0, 0, 0))
        update_scene(level)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
