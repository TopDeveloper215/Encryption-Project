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

def load_key():
    return open("encryption_key.key", "rb").read()

def decrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    print(f"File '{file_path}' decrypted successfully.")

def decrypt_myd_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".MYD"):
                file_path = os.path.join(root, file)
                print(f"Decrypting: {file_path}")
                decrypt_file(file_path)

def remove_key_file():
    key_file_path = "encryption_key.key"
    if os.path.exists(key_file_path):
        os.remove(key_file_path)
        print(f"Key file '{key_file_path}' has been removed.")

if __name__ == "__main__":
    if not is_admin():
        print("Re-running script with administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    folder_to_decrypt = "C:/mysql/data/demo"
    
    decrypt_myd_files_in_folder(folder_to_decrypt) 
    remove_key_file()
    stop_mysql_service()
    start_mysql_service()
