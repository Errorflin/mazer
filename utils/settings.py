import pygame
import json

# Deafult settings
settings_load = {
    "movement": {
        "up": [pygame.K_UP, "Move Up"],
        "down": [pygame.K_DOWN, "Move Down"],
        "left": [pygame.K_LEFT, "Move Left"],
        "right": [pygame.K_RIGHT, "Move Right"],
        "sprint": [pygame.K_LSHIFT, "Sprint"]
    },
    "keys": {
        "place marker": [pygame.K_m, "Place Marker"],
        "change marker": [pygame.K_n, "Change Marker"],
        "reset position": [pygame.K_r, "Reset Position"]
    },
    "display": {
        "fullscreen": True
    },
    "audio": {
        "music volume": 100,
        "sfx volume": 100
    }
}

# Function to load settings from a file
def load_settings():
    try:
        with open("data/save/settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Create a new settings file with default settings
        with open("data/save/settings.json", "w") as f:
            json.dump(settings_load, f)
        return settings_load

# Function to save settings to a file
def save_settings(settings):
    with open("data/save/settings.json", "w") as f:
        json.dump(settings, f)