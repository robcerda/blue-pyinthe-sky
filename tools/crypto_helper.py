from cryptography.fernet import Fernet
import json
import base64
import os
import getpass

def generate_key():
    key = Fernet.generate_key()
    return key

def save_key_to_file(key, file_path):
    with open(file_path, "wb") as key_file:
        key_file.write(key)

def load_key(file_path):
    with open(file_path, "rb") as key_file:
        return key_file.read()

def prompt_credentials():
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    return {"identifier": email, "password": password}

def encode_credentials(credentials):
    json_str = json.dumps(credentials)
    return base64.b64encode(json_str.encode('utf-8'))

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data)

def main():
    key_directory = ".secrets"
    key_file = "secret.key"
    key_path = os.path.join(key_directory, key_file)

    if not os.path.exists(key_directory):
        os.makedirs(key_directory)

    key = generate_key()
    save_key_to_file(key, key_path)

    loaded_key = load_key(key_path)

    credentials = prompt_credentials()
    encoded_credentials = encode_credentials(credentials)
    encrypted_credentials = encrypt_data(encoded_credentials, loaded_key)

    print(encrypted_credentials)

if __name__ == "__main__":
    main()
