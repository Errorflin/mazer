import pygame
import sys

from utils.settings import *
from utils.shared_variables import *
from utils.fonts import *

clock = pygame.time.Clock()

settings = load_settings()

# Function to display settings menu
def settings_menu(return_function):
    global settings
    settings = load_settings() # Load settings from file

    current_setting = 0
    setting_keys = ["MOVEMENT", "KEYS", "DISPLAY", "AUDIO"]

    switcher = True
    while switcher:
        screen.fill(menu_bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_setting = (current_setting - 1) % len(setting_keys)
                elif event.key == pygame.K_DOWN:
                    current_setting = (current_setting + 1) % len(setting_keys)
                elif event.key == pygame.K_RETURN:
                    if current_setting == 0: # Movement
                        switcher = False
                        settings_menu_movement(return_function)
                    elif current_setting == 1: # Keys
                        switcher = False
                        settings_menu_keys(return_function)
                    elif current_setting == 2: # Display
                        pass
                    elif current_setting == 3: # Audio
                        pass
                elif event.key == pygame.K_ESCAPE:
                    switcher = False
                    settings = load_settings()
                    return_function()
        
        # Display title text
        title_text = SegoeUIBold120.render("SETTINGS", True, base_text_color)
        title_text_rect = title_text.get_rect(center=(screen_size[0] // 2, 80))
        screen.blit(title_text, title_text_rect)

        # Display options
        for i, key in enumerate(setting_keys):
            color = (hover_text_color if i == current_setting else base_text_color)
            option_text = SegoeUIBold80.render(f"{key}", True, color)
            option_text_rect = option_text.get_rect(center=(screen_size[0] // 2, 320 + i * 65))
            screen.blit(option_text, option_text_rect)

        pygame.display.update()
        clock.tick(fps_limit)

# Function to get a key binding from the user
def get_key_binding():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

def settings_menu_movement(return_function):
    global settings

    current_setting = 0
    settings = load_settings() # Load settings from file
    movement_keys = list(settings["movement"].keys())
    keys_keys = list(settings["keys"].keys())

    switcher = True
    while switcher:
        screen.fill(menu_bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_setting = (current_setting - 1) % len(movement_keys)
                elif event.key == pygame.K_DOWN:
                    current_setting = (current_setting + 1) % len(movement_keys)
                elif event.key == pygame.K_RIGHT:
                    key = movement_keys[current_setting]
                    # Display a prompt to get a new key binding
                    prompt_text = SegoeUIBold120.render("PRESS A NEW KEY", True, base_text_color)
                    prompt_rect = prompt_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
                    screen.blit(prompt_text, prompt_rect)
                    pygame.display.update()

                    # Wait for a key press and update the setting
                    new_key = get_key_binding()
                    settings["movement"][key][0] = new_key
                elif event.key == pygame.K_RETURN:
                    save_settings(settings)
                    switcher = False
                    settings_menu(return_function)
                elif event.key == pygame.K_ESCAPE:
                    switcher = False
                    settings_menu(return_function)
        
        # Display title text
        title_text = SegoeUIBold120.render("MOVEMENT", True, base_text_color)
        title_text_rect = title_text.get_rect(center=(screen_size[0] // 2, 80))
        subtitle_text = SegoeUIBold40.render("SETTINGS", True, base_text_color)
        subtitle_text_rect = subtitle_text.get_rect(center=(screen_size[0] // 2, 160))
        screen.blit(title_text, title_text_rect)
        screen.blit(subtitle_text, subtitle_text_rect)

        # Display options
        for i, key in enumerate(movement_keys):
            color = (hover_text_color if i == current_setting else base_text_color)

            key_text = SegoeUIBold80.render(f"| {pygame.key.name((settings['movement'][key][0])).title()}", True, (255, 255, 255))
            key_text_rect = key_text.get_rect(midleft=(screen_size[0] // 2 + 10, 250 + i * 75))
            text = SegoeUIBold80.render(f"{settings['movement'][key][1]}", True, color)
            text_rect = text.get_rect(midright=(screen_size[0] // 2 - 10, 250 + i * 75))
            screen.blit(text, text_rect)
            screen.blit(key_text, key_text_rect)

        pygame.display.update()
        clock.tick(fps_limit)

def settings_menu_keys(return_function):
    global settings

    current_setting = 0
    settings = load_settings() # Load settings from file
    keys_keys = list(settings["keys"].keys())

    switcher = True
    while switcher:
        screen.fill(menu_bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_setting = (current_setting - 1) % len(keys_keys)
                elif event.key == pygame.K_DOWN:
                    current_setting = (current_setting + 1) % len(keys_keys)
                elif event.key == pygame.K_RIGHT:
                    key = keys_keys[current_setting]
                    # Display a prompt to get a new key binding
                    prompt_text = SegoeUIBold120.render("PRESS A NEW KEY", True, base_text_color)
                    prompt_rect = prompt_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
                    screen.blit(prompt_text, prompt_rect)
                    pygame.display.update()

                    # Wait for a key press and update the setting
                    new_key = get_key_binding()
                    settings["keys"][key][0] = new_key
                elif event.key == pygame.K_RETURN:
                    save_settings(settings)
                    switcher = False
                    settings_menu(return_function)
                elif event.key == pygame.K_ESCAPE:
                    switcher = False
                    settings_menu(return_function)
        
        # Display title text
        title_text = SegoeUIBold120.render("KEYS", True, base_text_color)
        title_text_rect = title_text.get_rect(center=(screen_size[0] // 2, 80))
        subtitle_text = SegoeUIBold40.render("SETTINGS", True, base_text_color)
        subtitle_text_rect = subtitle_text.get_rect(center=(screen_size[0] // 2, 160))
        screen.blit(title_text, title_text_rect)
        screen.blit(subtitle_text, subtitle_text_rect)

        # Display options
        for i, key in enumerate(keys_keys):
            color = (hover_text_color if i == current_setting else base_text_color)

            key_text = SegoeUIBold80.render(f"| {pygame.key.name((settings['keys'][key][0])).title()}", True, (255, 255, 255))
            key_text_rect = key_text.get_rect(midleft=(screen_size[0] // 2 + 10, 250 + i * 75))
            text = SegoeUIBold80.render(f"{settings['keys'][key][1]}", True, color)
            text_rect = text.get_rect(midright=(screen_size[0] // 2 - 10, 250 + i * 75))
            screen.blit(text, text_rect)
            screen.blit(key_text, key_text_rect)

        pygame.display.update()
        clock.tick(fps_limit)