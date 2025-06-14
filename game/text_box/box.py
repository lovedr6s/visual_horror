import contextlib

import pygame


def bottom_text(display, lines):
    """Display text at the bottom of the screen."""
    pygame.draw.rect(display, (139, 0, 0), (50, 380, 700, 2))
    font = pygame.font.Font('game/fonts/font.otf', 30)

    for i, line in enumerate(lines):
        text = font.render(line, True, (139, 10, 10))
        text_rect = text.get_rect(topleft=(60, 390 + i * 30))
        display.blit(text, text_rect)


def image_pixelate(image):
    """Apply pixelation effect to an image."""
    width, height = image.get_size()
    pixelization_factor = 5
    for y in range(0, height, pixelization_factor):
        for x in range(0, width, pixelization_factor):
            color = image.get_at((x, y))
            pygame.draw.rect(image, color,
                             (x, y, pixelization_factor, pixelization_factor))


def image_box(display, image_path):
    """Load and display an image with pixelation effect."""
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (650, 300))
    image_pixelate(image)
    display.blit(image, (75, 50))


def scene(display, scene_data):
    """Render the scene with an image and text."""
    clean_text = []
    try:
        image_box(display, scene_data['image'])
    except KeyError:
        with contextlib.suppress(KeyError):
            image_box(display, 'game/text_box/images/empty.png')
    for line in scene_data['text']:
        for j in range(0, len(line), 27):
            clean_text.append(line[j:j + 27].strip())
    bottom_text(display, clean_text)
