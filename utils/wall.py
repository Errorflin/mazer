import pygame

from utils.shared_variables import *

pygame.init()

class Wall(pygame.sprite.Sprite):
    def __init__(self, wall_image, x, y):
        super().__init__()
        self.image = wall_image
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))