import pygame
import sys
import json
import random
import math
import colorsys

import pickle
from cryptography.fernet import Fernet

# ------------------------------------------------------------------------ ENCRYPTION
# Encrypt & Decrypt
encryption_key = b'24x6o-QgP8hapW2nqPdr1yBaleLvYp0h59rPwDgD1nA='

game_data = {
    "player": {
        "coins": 20,
        "marks": [5, 5, 5] # R, G, B
    },
    "level_1": {
        "locked": False,
        "player_pos": "S",
        "coins": [],
        "marks": []
    },
    "level_2": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "marks": []
    },
    "level_3": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "marks": []
    },
    "level_4": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "marks": []
    },
    "level_5": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "marks": []
    },
    "level_6": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "keys": [],
        "marks": []
    },
    "level_7": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "keys": [],
        "marks": []
    },
    "level_8": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "keys": [],
        "marks": []
    },
    "level_9": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "keys": [],
        "marks": []
    },
    "level_10": {
        "locked": True,
        "player_pos": "S",
        "coins": [],
        "keys": [],
        "marks": []
    },
}

game_data_location = "save/data.dat"

def save_game_data(data):
    fernet = Fernet(encryption_key)
    encrypted_data = fernet.encrypt(pickle.dumps(data))
    with open(game_data_location, "wb") as file:
        file.write(encrypted_data)

def load_game_data():
    try:
        with open(game_data_location, "rb") as file:
            encrypted_data = file.read()
            fernet = Fernet(encryption_key)
            data = pickle.loads(fernet.decrypt(encrypted_data))
        return data
    except (FileNotFoundError, pickle.UnpicklingError):
        save_game_data(game_data)
        return game_data

# ------------------------------------------------------------------------ INITIALIZE & DISPLAY
# Initialize Pygame
pygame.init()

ver = "v.ALPHA 2.1.0"

# Screen settings
screen_size = [1280, 720]
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
pygame.display.set_caption(f"Mazer {ver}")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Frame rate settings
fps_limit = 60

# ------------------------------------------------------------------------ FONTS
# Load the font files once
SegoeUIFile = "fonts/Segoe/Segoe UI.ttf"
SegoeUI = {}
SegoeUIBoldFile = "fonts/Segoe/Segoe UI Bold.ttf"
SegoeUIBold = {}

# Define the font sizes
font_sizes = [10, 20, 30, 40, 50, 60, 80, 90, 100, 120]

# Load the fonts and store them in the dictionary
for size in font_sizes:
    SegoeUI[size] = pygame.font.Font(SegoeUIFile, size)
    SegoeUIBold[size] = pygame.font.Font(SegoeUIBoldFile, size)

# Access fonts in different sizes:
SegoeUI10 = SegoeUI[10]; SegoeUIBold10 = SegoeUIBold[10]
SegoeUI20 = SegoeUI[20]; SegoeUIBold20 = SegoeUIBold[20]
SegoeUI30 = SegoeUI[30]; SegoeUIBold30 = SegoeUIBold[30]
SegoeUI40 = SegoeUI[40]; SegoeUIBold40 = SegoeUIBold[40]
SegoeUI60 = SegoeUI[60]; SegoeUIBold60 = SegoeUIBold[60]
SegoeUI80 = SegoeUI[80]; SegoeUIBold80 = SegoeUIBold[80]
SegoeUI90 = SegoeUI[90]; SegoeUIBold90 = SegoeUIBold[90]
SegoeUI100 = SegoeUI[100]; SegoeUIBold100 = SegoeUIBold[100]
SegoeUI120 = SegoeUI[120]; SegoeUIBold120 = SegoeUIBold[120]

# ------------------------------------------------------------------------ SETTINGS
# Deafult settings
settings = {
    "keys": {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "sprint": pygame.K_LSHIFT,
        "place marker": pygame.K_m,
        "change marker": pygame.K_n,
        "reset level": pygame.K_r
    }
}

# Function to load settings from a file
def load_settings():
    try:
        with open("save/settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Create a new settings file with default settings
        with open("save/settings.json", "w") as f:
            json.dump(settings, f)
        return settings

# Function to save settings to a file
def save_settings(settings):
    with open("save/settings.json", "w") as f:
        json.dump(settings, f)

# Function to get a key binding from the user
def get_key_binding():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

# Function to display the settings menu
def settings_menu():
    global settings
    
    current_setting = 0
    settings = load_settings()
    setting_keys = list(load_settings()["keys"].keys())

    while True:
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_setting = (current_setting - 1) % len(setting_keys)
                elif event.key == pygame.K_DOWN:
                    current_setting = (current_setting + 1) % len(setting_keys)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    key = setting_keys[current_setting]
                    # Display a prompt to get a new key binding
                    prompt_text = SegoeUIBold100.render("PRESS A NEW KEY", True, (255, 255, 255))
                    prompt_rect = prompt_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
                    screen.blit(prompt_text, prompt_rect)
                    pygame.display.update()

                    # Wait for a key press and update the setting
                    new_key = get_key_binding()
                    settings["keys"][key] = new_key
                elif event.key == pygame.K_RETURN:
                    save_settings(settings)
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

        for i, key in enumerate(setting_keys):
            color = ((45, 234, 247) if i == current_setting else (255, 255, 255))
            
            if key.lower() == "up": name = "Move Up"
            elif key.lower() == "down": name = "Move Down"
            elif key.lower() == "left": name = "Move Left"
            elif key.lower() == "right": name = "Move Right"
            elif key.lower() == "sprint": name = "Sprint"
            elif key.lower() == "place marker": name = "Place Marker"
            elif key.lower() == "change marker": name = "Change Marker"
            elif key.lower() == "reset level": name = "Reset Position"

            w_text = SegoeUIBold60.render(f"| {pygame.key.name(settings['keys'][key]).title()}", True, (255, 255, 255))
            text = SegoeUIBold60.render(f"{name.upper()}", True, color)
            text_rect = text.get_rect(topright=(screen_size[0] // 2 - 20, 130 + i * 70))
            screen.blit(text, text_rect)
            screen.blit(w_text, w_text.get_rect(topleft=(screen_size[0] // 2, 130 + i * 70)))

        sett_title_txt = SegoeUIBold120.render("SETTINGS", True, (255, 255, 255))
        sett_title_txt_rect = sett_title_txt.get_rect(center=(screen_size[0] // 2, 70))
        screen.blit(sett_title_txt, sett_title_txt_rect)
        
        info_txt1 = SegoeUIBold20.render("[ESC] Back", True, (40, 40, 40))
        screen.blit(info_txt1, (sett_title_txt_rect.topright[0] + 10, sett_title_txt_rect.topright[1] + 50))
        info_txt2 = SegoeUIBold20.render("[ENTER] Apply", True, (40, 40, 40))
        screen.blit(info_txt2, (sett_title_txt_rect.midright[0] + 10, sett_title_txt_rect.midright[1]))
        info_txt3 = SegoeUIBold20.render("[RIGHT] Change", True, (40, 40, 40))
        screen.blit(info_txt3, (sett_title_txt_rect.bottomright[0] + 10, sett_title_txt_rect.bottomright[1] - 50))

        pygame.display.update()
        clock.tick(fps_limit)
# ------------------------------------------------------------------------ SPLASH SCREEN
def splash():
    elapsed = 0

    switcher = True
    while switcher:
        screen.fill((20, 20, 20))

        elapsed += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                switcher = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    switcher = False
                    pygame.quit()
                    sys.exit()

        if elapsed < 120:
            studios = SegoeUIBold90.render("ERRORFLIN STUDIOS", True, (255, 255, 255))
            studios_rect = studios.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
            screen.blit(studios, studios_rect)
        else:
            dedication = SegoeUI30.render("Made for IGI", True, (255, 255, 255))
            dedication_rect = dedication.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
            screen.blit(dedication, dedication_rect)
        if elapsed == 240:
            switcher = False
            return

        pygame.display.update()
        clock.tick(fps_limit)

# ------------------------------------------------------------------------ MAIN MENU
# Create a simple menu
def main_menu():
    global settings

    menu_items = ["PLAY", "SETTINGS", "INFO", "QUIT"]
    item_selected = 0

    # Game title and version
    version_text = SegoeUIBold20.render(f"{ver}", True, (50, 50, 50))
    version_rect = version_text.get_rect(center=(screen_size[0] // 2, screen_size[1] - 20))

    while True:
        screen.fill((20, 20, 20))

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
                    if item_selected == 0:  # PLAY
                        level_select()
                    elif item_selected == 1:  # SETTINGS
                        settings = load_settings()
                        settings_menu()
                    elif item_selected == 2:  # INFO
                        # Implement your info functionality here
                        pass
                    elif item_selected == 3:  # QUIT
                        pygame.quit()
                        sys.exit()

        # Draw title and version
        screen.blit(title_image, (30, -50 + 10*math.sin(pygame.time.get_ticks() / 500)))
        screen.blit(version_text, version_rect)

        # Draw menu options
        for i, item in enumerate(menu_items):
            if i == item_selected:
                if item == "QUIT":
                    color = (220, 70, 70)
                elif item == "PLAY":
                    color = (50, 220, 100)
                elif item == "SETTINGS":
                    color = (220, 150, 20)
                elif item == "INFO":
                    color = (50, 100, 220)
            else:
                color = (255, 255, 255)

            text = SegoeUIBold100.render(item, True, color)
            text_rect = text.get_rect(center=(screen_size[0] // 2, 280 + i * 75))
            screen.blit(text, text_rect)

        pygame.display.update()

        # Limit the frame rate
        clock.tick(fps_limit)

# ------------------------------------------------------------------------ TILEMAP
# Tile settings
tile_size = 3

# Load the tilemap from a file
def load_tilemap(filename):
    with open(filename, 'r') as file:
        encrypted_data = file.read()
        fernet = Fernet(encryption_key)
        data = pickle.loads(fernet.decrypt(encrypted_data))
        #data = file.readlines()
    tilemap = [line.strip() for line in data]
    return tilemap

# ------------------------------------------------------------------------ IMAGES
# Preload images
player_image = pygame.image.load("skins/blue.png").convert()
wall_image = pygame.image.load("sprites/wall.png").convert()
red_mark_image = pygame.image.load("sprites/red_mark.png").convert()
red_mark_image.set_colorkey((255, 255, 255))
green_mark_image = pygame.image.load("sprites/green_mark.png").convert()
green_mark_image.set_colorkey((255, 255, 255))
blue_mark_image = pygame.image.load("sprites/blue_mark.png").convert()
blue_mark_image.set_colorkey((255, 255, 255))
coin_image = pygame.image.load("sprites/coin.png").convert()
select_image = pygame.image.load("sprites/select.png").convert()
end_marker_image = pygame.image.load("sprites/end_marker.png").convert()
key_image = pygame.image.load("sprites/key.png").convert()
key_image.set_colorkey((255, 255, 255))

blank_grey_image = pygame.image.load("sprites/blank_grey.png").convert()
blank_red_image = pygame.image.load("sprites/blank_red.png").convert()

title_image = pygame.image.load("sprites/title.png")

# ------------------------------------------------------------------------ CLASSES
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, coins, marks, spawn_pos=(screen_size[0] // 2, screen_size[1] // 2), speed=2):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=spawn_pos)
        self.speed = speed
        self.coins = coins
        self.marks = marks

    def update(self, walls):
        self.move_x, self.move_y = 0, 0
        keys = pygame.key.get_pressed()
        if keys[settings["keys"]["left"]]:
            self.move_x = -self.speed
        if keys[settings["keys"]["right"]]:
            self.move_x = self.speed
        if keys[settings["keys"]["up"]]:
            self.move_y = -self.speed
        if keys[settings["keys"]["down"]]:
            self.move_y = self.speed
        if keys[settings["keys"]["sprint"]]:
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

# Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_image
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))

class Mark(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        if self.color == 1: # 1 - RED
            self.image = red_mark_image
        elif self.color == 2: # 2 - GREEN
            self.image = green_mark_image
        elif self.color == 3: # 3 - BLUE
            self.image = blue_mark_image
        self.rect = self.image.get_rect(center=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect(center=(x, y))

class EndMarker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = end_marker_image
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = key_image
        self.rect = self.image.get_rect(center=(x * tile_size, y * tile_size))

# ------------------------------------------------------------------------ UTILS
# Define a function that smoothly interpolate values (lerp)
def lerp(a, b, t):
    return a + (b - a) * t

def hsl_to_rgb(h, s, l):
    # Convert HSL to RGB using colorsys
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return int(r * 255), int(g * 255), int(b * 255)

def get_color_for_value(value):
    # Clamp the value between 0 and 100 (percentage range)
    value = min(max(value, 0), 100)

    # Calculate the hue value based on the percentage
    hue = (120 * (1 - value / 100)) % 360

    # Set constant saturation and lightness for a more consistent color transition
    saturation = 100
    lightness = 50

    # Convert HSL to RGB
    return hsl_to_rgb(hue, saturation, lightness)
# ------------------------------------------------------------------------ SHOP
# Create a simple shop
def shop():
    global game_data
    
    game_data = load_game_data()
    
    player = Player(game_data["player"]["coins"], game_data["player"]["marks"])
    
    shop_items = [["RED MARKER", 50], ["GREEN MARKER", 50], ["BLUE MARKER", 50]]
    item_selected = 0

    # Game title and version
    title_text = SegoeUIBold120.render("SHOP", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_size[0] // 2, 70))

    color = (20, 20, 20)
    switcher = True
    while switcher:
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data["player"]["marks"] = player.marks
                game_data["player"]["coins"] = player.coins
                save_game_data(game_data)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    item_selected = (item_selected - 1) % len(shop_items)
                elif event.key == pygame.K_DOWN:
                    item_selected = (item_selected + 1) % len(shop_items)
                elif event.key == pygame.K_RETURN:
                    if item_selected == 0:  # RED MARK
                        if player.marks[0] < 9 and player.coins >= shop_items[item_selected][1]:
                            player.marks[0] += 1
                            player.coins -= shop_items[item_selected][1]
                    elif item_selected == 1:  # GREEN MARK
                        if player.marks[1] < 9  and player.coins >= shop_items[item_selected][1]:
                            player.marks[1] += 1
                            player.coins -= shop_items[item_selected][1]
                    elif item_selected == 2:  # BLUE MARK
                        if player.marks[2] < 9  and player.coins >= shop_items[item_selected][1]:
                            player.marks[2] += 1
                            player.coins -= shop_items[item_selected][1]
                elif event.key == pygame.K_ESCAPE:
                    game_data["player"]["marks"] = player.marks
                    game_data["player"]["coins"] = player.coins
                    save_game_data(game_data)
                    switcher = False
                    level_select()

        # Draw title and version
        screen.blit(title_text, title_rect)

        # Draw menu options
        for i, item in enumerate(shop_items):
            if i == item_selected:
                color = (45, 234, 247)
            else:
                color = (255, 255, 255)

            text = SegoeUIBold40.render(f'x1 {item[0]}', True, color)
            text_rect = text.get_rect(topleft=(300, 150 + i * 50))
            screen.blit(text, text_rect)
            price = SegoeUIBold40.render(f'{item[1]}', True, (255, 255, 255))
            price_rect = price.get_rect(midright=(text_rect.midleft[0] - 10, text_rect.midleft[1]))
            screen.blit(price, price_rect)
            coin_img = pygame.transform.scale(coin_image, (30, 30))
            coin_img_rect = coin_img.get_rect(midright=(price_rect.midleft[0] - 10, price_rect.midleft[1]))
            screen.blit(coin_img, coin_img_rect)

        # Display coins at the bottom | GUI
        coins_img = pygame.transform.scale(coin_image, (20, 20))
        coins_img_rect = coins_img.get_rect(center=(20, screen_size[1] - 50))
        coins = player.coins
        coins_text = SegoeUIBold20.render(f"{coins}", True, (255, 255, 255))
        screen.blit(coins_text, coins_text.get_rect(midleft=(coins_img_rect.midright[0] + 10, coins_img_rect.midright[1])))
        screen.blit(coins_img, coins_img_rect)
        
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
            screen.blit(mark_gui_image, mark_gui_image.get_rect(center=(mark_gui_pos)))

        info_txt1 = SegoeUIBold20.render("[ESC] Back", True, (40, 40, 40))
        screen.blit(info_txt1, info_txt1.get_rect(midleft=(title_rect.midright[0] + 10, title_rect.midright[1])))
        info_txt2 = SegoeUIBold20.render("[ENTER] Buy", True, (40, 40, 40))
        screen.blit(info_txt2, info_txt2.get_rect(bottomleft=(title_rect.bottomright[0] + 10, title_rect.bottomright[1] - 30)))

        pygame.display.update()

        # Limit the frame rate
        clock.tick(fps_limit)

# ------------------------------------------------------------------------ LEVEL SELECT
# Load tilemap
tilemap = None

level1_map = "levels/level_1.lvl" # 5
level2_map = "levels/level_2.lvl" # 10
level3_map = "levels/level_3.lvl" # 12
level4_map = "levels/level_4.lvl" # 15
level5_map = "levels/level_5.lvl" # 17
level6_map = "levels/level_6.lvl" # 20
level7_map = "levels/level_7.lvl" # 23
level8_map = "levels/level_8.lvl" # 26
level9_map = "levels/level_9.lvl" # 30
level10_map = "levels/level_10.lvl" # 33

def level_select():
    global tilemap, game_data
    game_data = load_game_data()

    levels_items = ["LEVEL 1", "LEVEL 2", "LEVEL 3", "LEVEL 4", "LEVEL 5", "LEVEL 6", "LEVEL 7", "LEVEL 8", "LEVEL 9", "LEVEL 10"]
    item_selected = 0

    # Game title and version
    title_text = SegoeUIBold120.render("LEVELS", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_size[0] // 2, 70))

    initial_hue = pygame.time.get_ticks() / 10

    locked = True # True - Locked, False - Unlocked
    difficulty = 0 # 0 out of 100 representing %
    level_title = "" # For ex. SMALLER MAZE
    est_time = "" # For ex. <2min in level 1
    coins_remaining = 0 # For ex. 67 from level 1

    color = (20, 20, 20)
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
                    if item_selected == 0 and not game_data["level_1"]["locked"]:  # LEVEL 1
                        tilemap = load_tilemap(level1_map)
                        switcher = False
                        game("level_1")
                    elif item_selected == 1 and not game_data["level_2"]["locked"]:  # LEVEL 2
                        tilemap = load_tilemap(level2_map)
                        switcher = False
                        game("level_2")
                    elif item_selected == 2 and not game_data["level_3"]["locked"]:  # LEVEL 3
                        tilemap = load_tilemap(level3_map)
                        switcher = False
                        game("level_3")
                    elif item_selected == 3 and not game_data["level_4"]["locked"]:  # LEVEL 4
                        tilemap = load_tilemap(level4_map)
                        switcher = False
                        game("level_4")
                    elif item_selected == 4 and not game_data["level_5"]["locked"]:  # LEVEL 5
                        tilemap = load_tilemap(level5_map)
                        switcher = False
                        game("level_5")
                    elif item_selected == 5 and not game_data["level_6"]["locked"]:  # LEVEL 6
                        tilemap = load_tilemap(level6_map)
                        switcher = False
                        game("level_6")
                    elif item_selected == 6 and not game_data["level_7"]["locked"]:  # LEVEL 7
                        tilemap = load_tilemap(level7_map)
                        switcher = False
                        game("level_7")
                    elif item_selected == 7 and not game_data["level_8"]["locked"]:  # LEVEL 8
                        tilemap = load_tilemap(level8_map)
                        switcher = False
                        game("level_8")
                    elif item_selected == 8 and not game_data["level_9"]["locked"]:  # LEVEL 9
                        tilemap = load_tilemap(level9_map)
                        switcher = False
                        game("level_9")
                    elif item_selected == 9 and not game_data["level_10"]["locked"]:  # LEVEL 10
                        tilemap = load_tilemap(level10_map)
                        switcher = False
                        game("level_10")
                elif event.key == pygame.K_s:
                    switcher = False
                    shop()
                elif event.key == pygame.K_ESCAPE:
                    switcher = False
                    main_menu()

        # Draw title and version
        screen.blit(title_text, title_rect)

        # Draw menu options
        for i, item in enumerate(levels_items):
            if i == item_selected:
                hue = (initial_hue + i * 30) % 360
                color = pygame.Color(0, 0, 0)
                color.hsva = (hue, 100, 100, 100)
            else:
                color = (255, 255, 255)

            text = SegoeUIBold60.render(item, True, color)
            text_rect = text.get_rect(topleft=(20, 125 + i * 55))
            screen.blit(text, text_rect)

            # Change info about level
            if item_selected == 0: # LEVEL 1
                locked = game_data["level_1"]["locked"]
                difficulty = 0.2
                level_title = "NANO NEXUS"
                est_time = "~7s"
                coins_remaining = len(game_data["level_1"]["coins"])
            if item_selected == 1: # LEVEL 2
                locked = game_data["level_2"]["locked"]
                difficulty = 1
                level_title = "MICROCOSM MAZE"
                est_time = "~25s"
                coins_remaining = len(game_data["level_2"]["coins"])
            if item_selected == 2: # LEVEL 3
                locked = game_data["level_3"]["locked"]
                difficulty = 4
                level_title = "PETITE PASSAGEWAY"
                est_time = "~30s"
                coins_remaining = len(game_data["level_3"]["coins"])
            if item_selected == 3: # LEVEL 4
                locked = game_data["level_4"]["locked"]
                difficulty = 6
                level_title = "Diminutive Dungeon".upper()
                est_time = "~46s"
                coins_remaining = len(game_data["level_4"]["coins"])
            if item_selected == 4: # LEVEL 5
                locked = game_data["level_5"]["locked"]
                difficulty = 11
                level_title = "Atom Alley".upper()
                est_time = "~53s"
                coins_remaining = len(game_data["level_5"]["coins"])
            if item_selected == 5: # LEVEL 6
                locked = game_data["level_6"]["locked"]
                difficulty = 16
                level_title = "Compact Corridor".upper()
                est_time = "~1min 10s"
                coins_remaining = len(game_data["level_6"]["coins"])
            if item_selected == 6: # LEVEL 7
                locked = game_data["level_7"]["locked"]
                difficulty = 21
                level_title = "Pocket-Sized Path".upper()
                est_time = "~2min 30s"
                coins_remaining = len(game_data["level_7"]["coins"])
            if item_selected == 7: # LEVEL 8
                locked = game_data["level_8"]["locked"]
                difficulty = 27
                level_title = "Middling Maze".upper()
                est_time = "x min"
                coins_remaining = len(game_data["level_8"]["coins"])
            if item_selected == 8: # LEVEL 9
                locked = game_data["level_9"]["locked"]
                difficulty = 32
                level_title = "Average Amaze".upper()
                est_time = "x min"
                coins_remaining = len(game_data["level_9"]["coins"])
            if item_selected == 9: # LEVEL 10
                locked = game_data["level_10"]["locked"]
                difficulty = 38
                level_title = "Balanced Bafflement".upper()
                est_time = "x min"
                coins_remaining = len(game_data["level_10"]["coins"])

        # Display info about level
        if locked: info_color = (150, 150, 150)
        else: info_color = (255, 255, 255)
        maze_title = SegoeUIBold80.render(f"{level_title}", True, info_color)
        difficulty_info = SegoeUIBold30.render(f"{difficulty}%", True, get_color_for_value(difficulty))
        difficulty_text = SegoeUIBold30.render("DIFFICULTY", True, info_color)
        time_info = SegoeUIBold30.render(f"{est_time}", True, info_color)
        locked_info = SegoeUIBold30.render(f"{'LOCKED' if locked else 'UNLOCKED'}", True, info_color)

        maze_title_rect = maze_title.get_rect(topleft=(300, 200))
        difficulty_info_rect = difficulty_info.get_rect(topleft=(300, 285))
        difficulty_text_rect = difficulty_text.get_rect(midleft=(difficulty_info_rect.midright[0] + 10, difficulty_info_rect.midright[1]))
        time_info_rect = time_info.get_rect(bottomleft=(300, 230))
        locked_info_rect = locked_info.get_rect(midleft=(time_info_rect.midright[0] + 30, time_info_rect.midright[1]))
        if coins_remaining == 0:
            coins_remaining = "???"
        if coins_remaining == 1:
            coins_remaining = 0
        coin_img = pygame.transform.scale(coin_image, (20, 20))
        coin_info = SegoeUIBold30.render(f"{coins_remaining}", True, info_color)
        coin_img_rect = coin_img.get_rect(midleft=(difficulty_text_rect.midright[0] + 20, difficulty_text_rect.midright[1] + 2))
        coin_info_rect = coin_info.get_rect(midleft=(coin_img_rect.midright[0] + 10, coin_img_rect.midright[1] - 2))
        screen.blit(coin_img, coin_img_rect)
        screen.blit(coin_info, coin_info_rect)
        screen.blit(maze_title, maze_title_rect)
        screen.blit(difficulty_info, difficulty_info_rect)
        screen.blit(difficulty_text, difficulty_text_rect)
        screen.blit(time_info, time_info_rect)
        screen.blit(locked_info, locked_info_rect)

        info_txt1 = SegoeUIBold20.render("[ESC] Back", True, (40, 40, 40))
        screen.blit(info_txt1, (title_rect.topright[0] + 10, title_rect.topright[1] + 50))
        info_txt2 = SegoeUIBold20.render("[ENTER] Select Level", True, (40, 40, 40))
        screen.blit(info_txt2, (title_rect.midright[0] + 10, title_rect.midright[1]))
        info_txt3 = SegoeUIBold20.render("[S] Shop", True, (255, 255, 255))
        screen.blit(info_txt3, (title_rect.bottomright[0] + 10, title_rect.bottomright[1] - 50))

        pygame.display.update()

        # Limit the frame rate
        clock.tick(fps_limit)

# ------------------------------------------------------------------------ NEW LEVEL
def new_level(prev_level, time):
    global settings, game_data, tilemap
    game_data = load_game_data()
    settings = load_settings()

    next_level = ""
    if prev_level == "level_1": next_level = "level_2"; tilemap = load_tilemap(level2_map)
    if prev_level == "level_2": next_level = "level_3"; tilemap = load_tilemap(level3_map)
    if prev_level == "level_3": next_level = "level_4"; tilemap = load_tilemap(level4_map)
    if prev_level == "level_4": next_level = "level_5"; tilemap = load_tilemap(level5_map)
    if prev_level == "level_5": next_level = "level_6"; tilemap = load_tilemap(level6_map)
    if prev_level == "level_6": next_level = "level_7"; tilemap = load_tilemap(level7_map)
    if prev_level == "level_7": next_level = "level_8"; tilemap = load_tilemap(level8_map)
    if prev_level == "level_8": next_level = "level_9"; tilemap = load_tilemap(level9_map)
    if prev_level == "level_9": next_level = "level_10"; tilemap = load_tilemap(level10_map)

    game_data[f"{next_level}"]["locked"] = False
    game_data[prev_level]["player_pos"] = 'S'
    save_game_data(game_data)

    switcher = True
    while switcher:
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                switcher = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    switcher = False
                    main_menu()
                if event.key == pygame.K_RETURN:
                    switcher = False
                    game(next_level)

        title = SegoeUIBold80.render("CONGRATULATIONS!", True, (50, 200, 130))
        title_rect = title.get_rect(center=(screen_size[0] // 2, 55))
        screen.blit(title, title_rect)
        subtitle = SegoeUIBold60.render(f"On completing {prev_level.replace('_', ' ').title()}", True, (255, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(screen_size[0] // 2, 130))
        screen.blit(subtitle, subtitle_rect)
        subtitle2 = SegoeUIBold40.render(f'{game_data["player"]["coins"]}/{len(game_data[prev_level]["coins"])-1} in this level', True, (255, 255, 255))
        subtitle2_rect = subtitle2.get_rect(center=(screen_size[0] // 2, 300))
        coins_img = pygame.transform.scale(coin_image, (30, 30))
        coins_img_rect = coins_img.get_rect(midright=(subtitle2_rect.midleft[0] - 10, subtitle2_rect.midleft[1] + 2))
        screen.blit(coins_img, coins_img_rect)
        screen.blit(subtitle2, subtitle2_rect)
        subtitle3 = SegoeUIBold40.render(f'{time[0]:02d}:{time[1]:02d}:{time[2]:03d}', True, (255, 255, 255))
        subtitle3_rect = subtitle3.get_rect(center=(screen_size[0] // 2, 340))
        screen.blit(subtitle3, subtitle3_rect)

        info_txt1 = SegoeUIBold20.render("[ESC] Level Select", True, (40, 40, 40))
        screen.blit(info_txt1, (title_rect.midright[0] + 10, title_rect.midright[1] - 15))
        info_txt2 = SegoeUIBold20.render("[ENTER] Next Level", True, (40, 40, 40))
        screen.blit(info_txt2, (title_rect.bottomright[0] + 10, title_rect.bottomright[1] - 40))

        for mark_i in range(3):
            mark_gui_pos = (screen_size[0] // - 100, 320)
            mark_gui_image = None
            text = ""
            if mark_i == 0:
                mark_gui_image = pygame.transform.scale(red_mark_image, (20, 20))
                text = f'{game_data["player"]["marks"][0]}'
            elif mark_i == 1:
                mark_gui_image = pygame.transform.scale(green_mark_image, (20, 20))
                text = f'{game_data["player"]["marks"][1]}'
            elif mark_i == 2:
                mark_gui_image = pygame.transform.scale(blue_mark_image, (20, 20))
                text = f'{game_data["player"]["marks"][2]}'
            mark_text = SegoeUIBold20.render(text, True, (255, 255, 255))
            mark_gui_rect = mark_gui_image.get_rect(center=(mark_gui_pos))
            screen.blit(mark_gui_image, mark_gui_rect)
            screen.blit(mark_text, mark_text.get_rect(midleft=(mark_gui_rect.midright[0] + 10, mark_gui_rect.midright[1])))

        pygame.display.update()
        clock.tick(fps_limit)

# ------------------------------------------------------------------------ GAME
# Main game function
def game(level):
    global settings, game_data
    game_data = load_game_data()
    settings = load_settings()
    
    player = Player(game_data["player"]["coins"], game_data["player"]["marks"])
    walls = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    marks = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    end_marks = pygame.sprite.Group()
    keys = pygame.sprite.Group()

    current_mark_color = 2 # 1 - RED, 2 - GREEN, 3 - BLUE

    if game_data[level]["coins"] == []:
        coinP = Coin(50000 * tile_size, 50000 * tile_size)
        coins_group.add(coinP)

    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 'W':
                wall = Wall(x, y)
                walls.add(wall)
            if tile == 'E':
                end_mark = EndMarker(x, y)
                end_marks.add(end_mark)
            if tile == 'S' and game_data[level]["player_pos"] == 'S':
                player.rect.center = (x * tile_size, y * tile_size)
            if tile == '0' and game_data[level]["coins"] == []:
                n = random.randint(0, 1000)
                if n <= 2:
                    coin = Coin(x * tile_size, y * tile_size)
                    coins_group.add(coin)
            if tile == 'K':
                key = Key(x, y)
                keys.add(key)

    if game_data[level]["player_pos"] != 'S':
        player.rect.center = game_data[level]["player_pos"]
    if game_data[level]["coins"] != []:
        o = 0
        for coin_ in game_data[level]["coins"]:
            coin = Coin(coin_[0], coin_[1])
            coins_group.add(coin)
            o += 1

    i = 0
    for mark_ in game_data[level]["marks"]:
        mark = Mark(mark_[0], mark_[1], mark_[2])
        marks.add(mark)
        i += 1

    # Camera position initialization
    camera_x, camera_y = player.rect.center

    m_key_pressed = False
    r_key_pressed = False

    ticks = 0
    starttime = pygame.time.get_ticks()
    minutes = 0
    seconds = 0
    millis = 0

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
                save_game_data(game_data)
                switcher = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == settings["keys"]["place marker"]:
                    m_key_pressed = True
                if event.key == settings["keys"]["reset level"]:
                    r_key_pressed = True
                if event.key == settings["keys"]["change marker"]:
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
                    save_game_data(game_data)
                    switcher = False
                    # print("after switcher")
                    level_select()
                    break
            elif event.type == pygame.KEYUP:
                if event.key == settings["keys"]["place marker"]:
                    if m_key_pressed and player.marks[current_mark_color-1] > 0:
                        player.marks[current_mark_color-1] -= 1
                        mark = Mark(player.rect.centerx, player.rect.centery, current_mark_color)
                        marks.add(mark)
                        m_key_pressed = False
                if event.key == settings["keys"]["reset level"]:
                    if r_key_pressed:
                        # game_data[level]["marks"] = []
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
                        save_game_data(game_data)
                        switcher = False
                        game(level)
                        r_key_pressed = False

        coin_hit = pygame.sprite.spritecollide(player, coins_group, True)
        if coin_hit:
            player.coins += 1

        end_hit = pygame.sprite.spritecollide(player, end_marks, False)
        if end_hit:
            dat_marks_list = []
            dat_coins_list = []
            for mark in marks:
                dat_marks_list.append([mark.rect.centerx, mark.rect.centery, mark.color])
            for coin in coins_group:
                dat_coins_list.append([coin.rect.centerx, coin.rect.centery])
            game_data[level]["marks"] = dat_marks_list
            game_data[level]["player_pos"] = 'S'
            game_data[level]["coins"] = dat_coins_list
            game_data["player"]["coins"] = player.coins
            save_game_data(game_data)
            switcher = False
            new_level(level, [minutes, seconds, millis])

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
        for end_mark_ in end_marks:
            if end_mark_.rect.colliderect(camera_rect):
                screen.blit(end_mark_.image, (end_mark_.rect.x - camera_x, end_mark_.rect.y - camera_y))
        for mark_ in marks:
            if mark_.rect.colliderect(camera_rect):
                screen.blit(mark_.image, (mark_.rect.x - camera_x, mark_.rect.y - camera_y))
        for coin_ in coins_group:
            if coin_.rect.colliderect(camera_rect):
                screen.blit(coin_.image, (coin_.rect.x - camera_x, coin_.rect.y - camera_y))
        for key_ in keys:
            if key_.rect.colliderect(camera_rect):
                screen.blit(key_.image, (key_.rect.x - camera_x, key_.rect.y - camera_y))
        if player.rect.colliderect(camera_rect):
            screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))
        
        # Display frame rate in the top-left corner
        frame_rate = clock.get_fps()
        frame_rate_text = SegoeUIBold20.render(f"FPS: {frame_rate:.2f}", True, (255, 255, 255))
        screen.blit(frame_rate_text, (10, 10))

        level_info = SegoeUIBold20.render(f"{level.replace('_', ' ').title()}", True, (255, 255, 255))
        level_info_rect = level_info.get_rect(center=(screen_size[0] // 2, 90))
        screen.blit(level_info, level_info_rect)

        ticks = pygame.time.get_ticks() - starttime
        millis = ticks % 1000
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)

        timer_text = SegoeUIBold80.render(f'{minutes:02d}:{seconds:02d}:{millis:03d}', True, (255, 255, 255))
        timer_text_rect = timer_text.get_rect(center=(screen_size[0] // 2, 35))
        screen.blit(timer_text, timer_text_rect)

        # Display coins at the bottom | GUI
        coins_img = pygame.transform.scale(coin_image, (20, 20))
        coins_img_rect = coins_img.get_rect(center=(20, screen_size[1] - 50))
        coins = player.coins
        coins_text = SegoeUIBold20.render(f"{coins}", True, (255, 255, 255))
        screen.blit(coins_text, coins_text.get_rect(midleft=(coins_img_rect.midright[0] + 10, coins_img_rect.midright[1])))
        screen.blit(coins_img, coins_img_rect)
        
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

# Run the game
clock = pygame.time.Clock()
splash()
main_menu()

# Quit Pygame when the game loop ends
pygame.quit()
