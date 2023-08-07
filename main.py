import pygame
import random
import sys
import json

from utils.settings import *
from utils.settings_menus import *
from utils.encryption import *
import utils.shared_variables as shared_variables
import utils.fonts as fonts

from utils.player import *
from utils.wall import *
from utils.mark import *
from utils.coin import *

# Game version
ver = "v.ALPHA 2.1.3"
shared_variables.ver = ver

# Initialize pygame
pygame.init()

# Load settings
settings = load_settings()
shared_variables.settings = settings
game_data = load_game_data("data/save/data.dat")

# Screen settings
screen_size = [1280, 720]
shared_variables.screen_size = screen_size
if settings["display"]["fullscreen"]:
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(screen_size)
shared_variables.screen = screen
pygame.display.set_caption(f"Mazer {ver}")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Frame rate settings
fps_limit = 60
shared_variables.fps_limit = fps_limit
clock = pygame.time.Clock()

# ------------------------------ IMAGES ------------------------------
player_image = pygame.image.load("data/gfx/player/light_green.png").convert()
wall_image = pygame.image.load("data/gfx/wall.png").convert()
red_mark_image = pygame.image.load("data/gfx/marks/red_mark.png").convert()
red_mark_image.set_colorkey((255, 255, 255))
green_mark_image = pygame.image.load("data/gfx/marks/green_mark.png").convert()
green_mark_image.set_colorkey((255, 255, 255))
blue_mark_image = pygame.image.load("data/gfx/marks/blue_mark.png").convert()
blue_mark_image.set_colorkey((255, 255, 255))
select_image = pygame.image.load("data/gfx/marks/select.png").convert()
coin_image = pygame.image.load("data/gfx/coin.png").convert()

blank_grey_image = pygame.image.load("data/gfx/blanks/blank_grey.png").convert()
blank_red_image = pygame.image.load("data/gfx/blanks/blank_red.png").convert()

# ------------------------------ COLORS ------------------------------
menu_bg_color = shared_variables.menu_bg_color
base_text_color = shared_variables.base_text_color
hover_text_color = shared_variables.hover_text_color

# Define a function that smoothly interpolate values (lerp)
def lerp(a, b, t):
    return a + (b - a) * t

# ------------------------------ MAIN MENU ------------------------------
# Function to display main menu
def main_menu():
    global settings
    settings = load_settings() # Load settings from file

    item_selected = 0
    menu_items = ["PLAY", "SETTINGS", "INFO", "QUIT"]

    switcher = True
    while switcher:
        screen.fill(menu_bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    item_selected = (item_selected - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    item_selected = (item_selected + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if item_selected == 0: # PLAY
                        switcher = False
                        level_select()
                    elif item_selected == 1: # SETTINGS
                        switcher = False
                        settings_menu(main_menu)
                        settings = load_settings()
                    elif item_selected == 2: # INFO
                        pass
                    elif item_selected == 3: # QUIT
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Blit title image
        #screen.blit(title_img, (0, 0))

        # Draw menu options
        for i, item in enumerate(menu_items):
            if i == item_selected:
                if item == "QUIT":
                    color = (220, 50, 50)
                elif item == "PLAY":
                    color = (50, 50, 200)
                elif item == "SETTINGS":
                    color = (252, 186, 3)
                elif item == "INFO":
                    color = (50, 220, 50)
            else:
                color = base_text_color

            text = SegoeUIBold80.render(item, True, color)
            text_rect = text.get_rect(center=(screen_size[0] // 2, 280 + i * 65))
            screen.blit(text, text_rect)

        pygame.display.update()
        clock.tick(fps_limit)

# ------------------------------ TILEMAP ------------------------------
# Tile settings
tile_size = 3
shared_variables.tile_size = tile_size

# Load the tilemap from a file
def load_tilemap(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    tilemap = [line.strip() for line in data]
    return tilemap

# Load tilemap
tilemap = None

level1_map = "data/levels/level_1.txt"
level2_map = "data/levels/level_2.txt"
level3_map = "data/levels/level_3.txt"
level4_map = "data/levels/level_4.txt"

# ------------------------------ SHOP ------------------------------
# Create a simple shop
def shop():
    pass

# ------------------------------ LEVEL SELECT ------------------------------
def level_select():
    global tilemap, settings
    settings = load_settings()

    levels_items = ["LEVEL 1", "LEVEL 2", "LEVEL 3", "LEVEL 4"]
    item_selected = 0

    initial_hue = pygame.time.get_ticks() / 10

    difficulty = 2 # 0 out of 100
    difficulty_prcent = "2%"
    difficulty_precent_color = (50, 220, 50)
    level_name = "SMALLER MAZE"
    level_time = "<2min"

    switcher = True
    while switcher:
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    item_selected = (item_selected - 1) % len(levels_items)
                elif event.key == pygame.K_DOWN:
                    item_selected = (item_selected + 1) % len(levels_items)
                elif event.key == pygame.K_RETURN:
                    if item_selected == 0:  # LEVEL 1
                        tilemap = load_tilemap(level1_map)
                        switcher = False
                        game("level_1")
                    elif item_selected == 1:  # LEVEL 2
                        tilemap = load_tilemap(level2_map)
                        switcher = False
                        game("level_2")
                    elif item_selected == 2:  # LEVEL 3
                        tilemap = load_tilemap(level3_map)
                        switcher = False
                        game("level_3")
                    elif item_selected == 3:  # LEVEL 4
                        tilemap = load_tilemap(level4_map)
                        switcher = False
                        game("level_4")
                elif event.key == pygame.K_s:
                    switcher = False
                    shop()
                elif event.key == pygame.K_ESCAPE:
                    switcher = False
                    main_menu()

        # Draw title and version
        title_text = SegoeUIBold120.render("LEVELS", True, base_text_color)
        title_text_rect = title_text.get_rect(center=(screen_size[0] // 2, 80))
        screen.blit(title_text, title_text_rect)

        # Draw menu options
        for i, item in enumerate(levels_items):
            if i == item_selected:
                hue = (initial_hue + i * 30) % 360
                color = pygame.Color(0, 0, 0)
                color.hsva = (hue, 100, 100, 100)
            else:
                color = (255, 255, 255)

            text = SegoeUIBold80.render(item, True, color)
            text_rect = text.get_rect(topright=(screen_size[0] // 2 - 100, 150 + i * 75))
            screen.blit(text, text_rect)

            # Info about level
            if item_selected == 0: # LEVEL 1
                difficulty = 2 # 0 out of 100
                difficulty_prcent = "2%"
                difficulty_precent_color = (50, 220, 50)
                level_name = "SMALLER MAZE"
                level_time = "<2min"
            if item_selected == 1: # LEVEL 2
                pass
            if item_selected == 2: # LEVEL 3
                pass
            if item_selected == 3: # LEVEL 4
                pass

        level_title_text = SegoeUIBold120.render(level_name, True, base_text_color)
        level_title_text_rect = level_title_text.get_rect(topleft=(screen_size[0] // 2 - 90, 150))
        
        """
        for grey in range(5):
            img = pygame.transform.scale(blank_grey_image, (30, 20))
            screen.blit(img, img.get_rect(center=(title_info_pos[0] + grey * 35 + 15, title_info_pos[1] + 80)))

        for red in range(difficulty):
            img = pygame.transform.scale(blank_red_image, (30, 20))
            screen.blit(img, img.get_rect(center=(title_info_pos[0] + diff * 35 + 15, title_info_pos[1] + 80)))
        """

        pygame.display.update()
        clock.tick(fps_limit)

# ------------------------------ GAME ------------------------------
# Main game function
def game(level):
    global settings, game_data
    settings = load_settings()
    game_data = load_game_data("data/save/data.dat")

    player = Player(player_image, game_data["player"]["coins"], game_data["player"]["marks"])

    walls = pygame.sprite.Group()
    marks = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()

    current_mark_color = 2 # 1 - RED, 2 - GREEN, 3 - BLUE

    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 'W':
                wall = Wall(wall_image, x, y)
                walls.add(wall)
            if tile == 'S' and game_data[level]["player_pos"] == 'S':
                player.rect.center = (x * tile_size, y * tile_size)
            elif tile == '0' and game_data[level]["coins"] == [] and y > 5:
                n = random.randint(0, 1000)
                if n <= 2:
                    coin = Coin(coin_image, x * tile_size, y * tile_size)
                    coins_group.add(coin)
    coinP = Coin(coin_image, 50000 * tile_size, 50000 * tile_size)
    coins_group.add(coinP)

    if game_data[level]["player_pos"] != 'S':
        player.rect.center = game_data[level]["player_pos"]
    if game_data[level]["coins"] != []:
        o = 0
        for coin_ in game_data[level]["coins"]:
            coin = Coin(coin_image, coin_[0], coin_[1])
            coins_group.add(coin)
            o += 1

    i = 0
    for mark_ in game_data[level]["marks"]:
        mark = Mark(red_mark_image, green_mark_image, blue_mark_image, mark_[0], mark_[1], mark_[2])
        marks.add(mark)
        i += 1

    # Camera position initialization
    camera_x, camera_y = player.rect.center

    m_key_pressed = False
    r_key_pressed = False

    switcher = True
    while switcher:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dat_marks_list = []
                dat_coins_list = []
                for mark in marks:
                    dat_marks_list.append([mark.rect.centerx, mark.rect.centery, mark.color])
                for coin in coins_group:
                    dat_coins_list.append([coin.rect.centerx, coin.rect.centery])
                game_data[level]["marks"] = dat_marks_list
                game_data[level]["player_pos"] = (player.rect.centerx, player.rect.centery)
                game_data[level]["coins"] = dat_coins_list
                game_data["player"]["coins"] = player.coins
                save_game_data(game_data, "data/save/data.dat")
                switcher = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == settings["keys"]["place marker"][0]:
                    m_key_pressed = True
                if event.key == settings["keys"]["reset position"][0]:
                    r_key_pressed = True
                if event.key == settings["keys"]["change marker"][0]:
                    if current_mark_color == 1:
                        current_mark_color = 2
                    elif current_mark_color == 2:
                        current_mark_color = 3
                    elif current_mark_color == 3:
                        current_mark_color = 1
                if event.key == pygame.K_ESCAPE:
                    dat_marks_list = []
                    dat_coins_list = []
                    for mark in marks:
                        dat_marks_list.append([mark.rect.centerx, mark.rect.centery, mark.color])
                    for coin in coins_group:
                        dat_coins_list.append([coin.rect.centerx, coin.rect.centery])
                    game_data[level]["marks"] = dat_marks_list
                    game_data[level]["player_pos"] = (player.rect.centerx, player.rect.centery)
                    game_data[level]["coins"] = dat_coins_list
                    game_data["player"]["coins"] = player.coins
                    save_game_data(game_data, "data/save/data.dat")
                    switcher = False
                    level_select()
                    break
            elif event.type == pygame.KEYUP:
                if event.key == settings["keys"]["place marker"][0]:
                    if m_key_pressed and player.marks[current_mark_color-1] > 0:
                        player.marks[current_mark_color-1] -= 1
                        mark = Mark(red_mark_image, green_mark_image, blue_mark_image, player.rect.centerx, player.rect.centery, current_mark_color)
                        marks.add(mark)
                        m_key_pressed = False
                if event.key == settings["keys"]["reset position"][0]:
                    if r_key_pressed:
                        # deafult_level_dat[level]["marks"] = []
                        dat_marks_list = []
                        dat_coins_list = []
                        for mark in marks:
                            dat_marks_list.append([mark.rect.centerx, mark.rect.centery, mark.color])
                        for coin in coins_group:
                            dat_coins_list.append([coin.rect.centerx, coin.rect.centery])
                        game_data[level]["coins"] = dat_coins_list
                        game_data[level]["marks"] = dat_marks_list
                        game_data["player"]["coins"] = player.coins
                        game_data[level]["player_pos"] = "S"
                        save_game_data(game_data, "data/save/data.dat")
                        switcher = False
                        game(level)
                        r_key_pressed = False

        coin_hit = pygame.sprite.spritecollide(player, coins_group, True)
        if coin_hit:
            player.coins += 1

        # Update game objects
        player.update(walls)

        # Calculate camera's new position using lerp (smooth camera follow)
        camera_x = lerp(camera_x, player.rect.centerx - screen_size[0] // 2, 0.1)
        camera_y = lerp(camera_y, player.rect.centery - screen_size[1] // 2, 0.1)

        # Render to the screen
        screen.fill((20, 20, 20))

        # Calculate the camera boundaries for image rendering
        camera_rect = pygame.Rect(camera_x, camera_y, screen_size[0], screen_size[1])

        # Draw walls and player relative to the camera's position and within boundaries
        for wall in walls:
            if wall.rect.colliderect(camera_rect):
                screen.blit(wall.image, (wall.rect.x - camera_x, wall.rect.y - camera_y))
        for mark_ in marks:
            if mark_.rect.colliderect(camera_rect):
                screen.blit(mark_.image, (mark_.rect.x - camera_x, mark_.rect.y - camera_y))
        for coin_ in coins_group:
            if coin_.rect.colliderect(camera_rect):
                screen.blit(coin_.image, (coin_.rect.x - camera_x, coin_.rect.y - camera_y))
        if player.rect.colliderect(camera_rect):
            screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))
        
        # Display frame rate in the top-left corner
        frame_rate = clock.get_fps()
        frame_rate_text = SegoeUIBold20.render(f"FPS: {frame_rate:.2f}", True, (255, 255, 255))
        screen.blit(frame_rate_text, (10, 10))

        # Display coins at the bottom | GUI
        coins = player.coins
        coins_lenght = len(str(coins))
        coins_text = SegoeUIBold20.render(f"{coins}", True, (255, 255, 255))
        coins_text_rect = coins_text.get_rect(center=(45 + 5 * coins_lenght, screen_size[1] - 50))
        screen.blit(coins_text, coins_text_rect)
        screen.blit(pygame.transform.scale(coin_image, (20, 20)), (pygame.transform.scale(coin_image, (20, 20)).get_rect(center=(20, screen_size[1] - 50))))
        
        for mark_i in range(3):
            mark_gui_pos = (20 + mark_i * 60, screen_size[1] - 20)
            mark_gui_image = None
            text = ""
            if mark_i == 0:
                mark_gui_image = pygame.transform.scale(red_mark_image, (20, 20))
                text = f"{player.marks[0]}"
            elif mark_i == 1:
                mark_gui_image = pygame.transform.scale(green_mark_image, (20, 20))
                text = f"{player.marks[1]}"
            elif mark_i == 2:
                mark_gui_image = pygame.transform.scale(blue_mark_image, (20, 20))
                text = f"{player.marks[2]}"
            mark_text = SegoeUIBold20.render(text, True, (255, 255, 255))
            screen.blit(mark_text, mark_text.get_rect(center=(mark_gui_pos[0] + 25, mark_gui_pos[1])))
            screen.blit(select_image, select_image.get_rect(center=(57 + (current_mark_color-1) * 60, mark_gui_pos[1])))
            screen.blit(mark_gui_image, mark_gui_image.get_rect(center=(mark_gui_pos)))
            
        pygame.display.update()

        # Limit the frame rate
        clock.tick(fps_limit)

if __name__ == "__main__":
    settings = load_settings()
    main_menu()