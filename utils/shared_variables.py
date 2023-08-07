import pygame
from utils.settings import *

pygame.init()

# Define your shared variables here
ver = "v.ALPHA 2.1.3"
screen_size = [1280, 720]
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
fps_limit = 60
menu_bg_color = (20, 20, 20)
base_text_color = (255, 255, 255)
hover_text_color = (66, 185, 245)
tile_size = 3

settings = load_settings()