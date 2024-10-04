import os
import sys
import ctypes
from cryptography.fernet import Fernet

# Function to check if the script is run as administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to stop MySQL service
def stop_mysql_service():
    print("Stopping MySQL service...")
    os.system("net stop mysql")

# Function to start MySQL service
def start_mysql_service():
    print("Starting MySQL service...")
    os.system("net start mysql")
    

# Generate a key only if the key file doesn't already exist
def generate_key():
    key_file_path = "encryption_key.key"
    
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

# Encrypt the .MYD file
def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    print(f"File '{file_path}' encrypted successfully.")

# Encrypt all .MYD files in the folder and its subfolders
def encrypt_myd_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".MYD"):
                file_path = os.path.join(root, file)
                print(f"Encrypting: {file_path}")
                encrypt_file(file_path)

# Main script
if __name__ == "__main__":
    # Check if the script is running with admin privileges
    if not is_admin():
        print("Re-running script with administrator privileges...")
        # If not admin, restart the script with elevated privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    # Folder path to encrypt
    folder_to_encrypt = "C:/mysql/data/demo"
    
    # Stop the MySQL service
    stop_mysql_service()
    
    # Generate encryption key if it doesn't exist
    generate_key()
    
    # Encrypt all .MYD files in the folder
    encrypt_myd_files_in_folder(folder_to_encrypt)
    
    # Start the MySQL service again after encryption
    start_mysql_service()

    
