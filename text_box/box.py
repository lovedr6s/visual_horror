import pygame


def bottom_text(display, lines):
    pygame.draw.rect(display, (139, 0, 0), (50, 380, 700, 2))
    font = pygame.font.Font('text_box/font.otf', 30)

    for i, line in enumerate(lines):
        text = font.render(line, True , (139, 10, 10))
        text_rect = text.get_rect(topleft=(60, 390 + i * 30))
        display.blit(text, text_rect)


def image_pixelate(image):
    width, height = image.get_size()
    pixelization_factor = 30
    for y in range(0, height, pixelization_factor):
        for x in range(0, width, pixelization_factor):
            print(x, y)
            color = image.get_at((x, y))
            pygame.draw.rect(image, color, (x, y, pixelization_factor, pixelization_factor))

def image_box(display, image_path): # добавить пикселизацию
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (650, 300))
    image_pixelate(image)
    display.blit(image, (75, 50))

def text_box(display, lines):
    result = []
    image_box(display, lines[0])
    for line in lines[1]:
        for j in range(0, len(line), 27):
                result.append(line[j:j + 27].strip())
    bottom_text(display, result)