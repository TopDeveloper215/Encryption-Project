import os
import sys
import ctypes
from cryptography.fernet import Fernet

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def stop_mysql_service():
    print("Stopping MySQL service...")
    os.system("net stop mysql")

def start_mysql_service():
    print("Starting MySQL service...")
    os.system("net start mysql")
    

def generate_key():
    key_file_path = "encryption_key.key"
    
    if not os.path.exists(key_file_path):
        key = Fernet.generate_key()
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)
        print(f"Encryption key generated and saved to '{key_file_path}'")
    else:
        print(f"Key file '{key_file_path}' already exists. Key generation skipped.")

def load_key():
    return open("encryption_key.key", "rb").read()

def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    print(f"File '{file_path}' encrypted successfully.")

def encrypt_myd_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".MYD"):
                file_path = os.path.join(root, file)
                print(f"Encrypting: {file_path}")
                encrypt_file(file_path)

if __name__ == "__main__":
    if not is_admin():
        print("Re-running script with administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    folder_to_encrypt = "C:/mysql/data/demo"
    
    stop_mysql_service()   
    generate_key()
    encrypt_myd_files_in_folder(folder_to_encrypt)
    start_mysql_service()

    
