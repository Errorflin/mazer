import pickle
from cryptography.fernet import Fernet

encryption_key = b'24x6o-QgP8hapW2nqPdr1yBaleLvYp0h59rPwDgD1nA='

level_data = {
    "player": {
        "coins": 20,
        "marks": [5, 5, 5] # R, G, B
    },
    "level_1": {
        "player_pos": "S",
        "coins": [],
        "marks": []
    },
    "level_2": {
        "player_pos": "S",
        "coins": [],
        "marks": []
    },
    "level_3": {
        "player_pos": "S",
        "coins": [],
        "marks": []
    },
    "level_4": {
        "player_pos": "S",
        "coins": [],
        "marks": []
    }
}

def save_game_data(data, filename):
    fernet = Fernet(encryption_key)
    encrypted_data = fernet.encrypt(pickle.dumps(data))
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def load_game_data(filename):
    try:
        with open(filename, "rb") as file:
            encrypted_data = file.read()
            fernet = Fernet(encryption_key)
            data = pickle.loads(fernet.decrypt(encrypted_data))
        return data
    except (FileNotFoundError, pickle.UnpicklingError):
        save_game_data(level_data, filename)
        return level_data