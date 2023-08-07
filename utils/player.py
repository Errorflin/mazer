import pygame

from utils.shared_variables import *
from utils.settings import *

settings = load_settings()

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, coins, marks, spawn_pos=(screen_size[0] // 2, screen_size[1] // 2)):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=spawn_pos)
        self.speed = 2
        self.coins = coins
        self.marks = marks

    def update(self, walls):
        self.move_x, self.move_y = 0, 0
        keys = pygame.key.get_pressed()
        if keys[settings["movement"]["left"][0]]:
            self.move_x = -self.speed
        if keys[settings["movement"]["right"][0]]:
            self.move_x = self.speed
        if keys[settings["movement"]["up"][0]]:
            self.move_y = -self.speed
        if keys[settings["movement"]["down"][0]]:
            self.move_y = self.speed
        if keys[settings["movement"]["sprint"][0]]:
            self.speed = 4
        else:
            self.speed = 2

        # Calculate the desired player position
        desired_x = self.rect.x + self.move_x
        desired_y = self.rect.y + self.move_y

        # Create a rect for the desired position
        desired_rect = pygame.Rect(desired_x, desired_y, self.rect.width, self.rect.height)

        # Check if the desired position collides with walls
        if not any(desired_rect.colliderect(wall.rect) for wall in walls):
            # Update the player's position
            self.rect.x = desired_x
            self.rect.y = desired_y