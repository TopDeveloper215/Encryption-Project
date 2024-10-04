import os
from cryptography.fernet import Fernet

# Generate a key (do this once and store it securely)
def generate_key():
    key_file_path = "encryption_key.key"
    
    # Check if the key file exists
    if not os.path.exists(key_file_path):
        key = Fernet.generate_key()
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)
        print(f"Encryption key generated and saved to '{key_file_path}'")
    else:
        print(f"Key file '{key_file_path}' already exists. Key generation skipped.")

# Load the encryption key
def load_key():
    return open("encryption_key.key", "rb").read()

# Authenticate the user by checking username and password
def authenticate(username, password):
    # Set allowed username and password
    correct_username = "Sniper"
    correct_password = "1"

    # Verify username and password
    if username != correct_username or password != correct_password:
        raise PermissionError("Access denied: Invalid username or password.")
    return "admin"  # Sniper has full admin privileges

# Check permission (Sniper has full admin privileges)
def check_permission(role, action):
    return True  # Sniper has full permissions

# Encrypt a file (only Sniper can do this)
def encrypt_file(file_path, username, password):
    role = authenticate(username, password)
    check_permission(role, "encrypt")

    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    print(f"File '{file_path}' encrypted successfully.")

# Decrypt a file (only Sniper can do this)
def decrypt_file(file_path, username, password):
    role = authenticate(username, password)
    check_permission(role, "decrypt")

    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    print(f"File '{file_path}' decrypted successfully.")

# Encrypt all files in a folder
def encrypt_folder(folder_path, username, password):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Encrypting: {file_path}")
            encrypt_file(file_path, username, password)

# Decrypt all files in a folder
def decrypt_folder(folder_path, username, password):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Decrypting: {file_path}")
            decrypt_file(file_path, username, password)

# Usage example
folder_to_encrypt = "C:/mysql/data/demo"

# 1. Generate the key once (run this once to create the encryption key)
generate_key()

# 2. Encrypt or Decrypt files in the folder (requires correct username and password)
encrypt_folder(folder_to_encrypt, "Sniper", "1")  # Only Sniper with password 1234 can encrypt or decrypt
decrypt_folder(folder_to_encrypt, "Sniper", "1")
