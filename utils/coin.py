import pygame

pygame.init()

class Coin(pygame.sprite.Sprite):
    def __init__(self, coin_image, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect(center=(x, y))