import pickle
from cryptography.fernet import Fernet

def encrypt_level(location, encryption_key):
    encryption_key_ = encryption_key.encode()
    with open(location, "r") as file:
        data = file.readlines()
    fernet = Fernet(encryption_key_)
    encrypted_data = fernet.encrypt(pickle.dumps(data))
    with open(location, "wb") as file:
        file.write(encrypted_data)

if __name__ == "__main__":
    x = input("W, S, E?")
    key = input("Encryption key: ")
    loc = input("Level location: ")
    encrypt_level(loc, key)
    print("Encrypted level succesfully!")