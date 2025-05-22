from math import e
import pygame


def bottom_text(display, lines):
    pygame.draw.rect(display, (139, 0, 0), (50, 380, 700, 2))
    font = pygame.font.Font('text/font.otf', 30)

    for i, line in enumerate(lines):
        text = font.render(line, True , (139, 10, 10))
        text_rect = text.get_rect(topleft=(60, 390 + i * 30))
        display.blit(text, text_rect)


def text_box(display, lines):
    result = []
    for line in lines[1]:
        for j in range(0, len(line), 27):
                result.append(line[j:j + 27].strip())
    bottom_text(display, result)