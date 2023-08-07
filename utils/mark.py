import pygame

pygame.init()

class Mark(pygame.sprite.Sprite):
    def __init__(self, red_mark_image, green_mark_image, blue_mark_image, x, y, color):
        super().__init__()
        self.color = color
        if self.color == 1: # 1 - RED
            self.image = red_mark_image
        elif self.color == 2: # 2 - GREEN
            self.image = green_mark_image
        elif self.color == 3: # 3 - BLUE
            self.image = blue_mark_image
        self.rect = self.image.get_rect(center=(x, y))