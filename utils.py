import pygame

def setSize_W(image, width): 
    w, h = image.get_size()
    ratio = w / h
    height = int(width / ratio)
    return pygame.transform.scale(image, (width, height))

def setSize_WH(image, width, height):
    return pygame.transform.scale(image, (width, height))

def loadImage(path):
    return pygame.image.load(path)

def calc_align_right(WINDOW_WIDTH, surface):
    return WINDOW_WIDTH - surface.get_width()

def calc_align_bottom(WINDOW_HEIGHT, surfce):
    return WINDOW_HEIGHT - surfce.get_height()

def flip_x(surface):
    return pygame.transform.flip(surface, True, False)

def flip_y(surface):
    return pygame.transform.flip(surface, False, True)

def flip_xy(surface):
    return pygame.transform.flip(surface, True, True)