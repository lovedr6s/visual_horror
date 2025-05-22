import pygame
from text_box.box import text_box
import json

pygame.init()
display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Horror Game")
clock = pygame.time.Clock()
def load_text_file(file_path):
    with open(file_path, 'r') as file:
        text = json.load(file)
    return text

lines = load_text_file('text_box/dialoges/text.json')

def main():
    level = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    level += 1
                    print("Left mouse button clicked")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    level += 1
                if event.key == pygame.K_ESCAPE:
                    print("Escape key pressed")
        display.fill((0, 0, 0))
        text_box(display, lines[level])
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
