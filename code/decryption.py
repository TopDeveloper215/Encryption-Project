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

# Load the encryption key
def load_key():
    return open("encryption_key.key", "rb").read()

# Decrypt the .MYD file
def decrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    print(f"File '{file_path}' decrypted successfully.")

# Decrypt all .MYD files in the folder and its subfolders
def decrypt_myd_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".MYD"):
                file_path = os.path.join(root, file)
                print(f"Decrypting: {file_path}")
                decrypt_file(file_path)

# Optionally, remove the key file after decryption
def remove_key_file():
    key_file_path = "encryption_key.key"
    if os.path.exists(key_file_path):
        os.remove(key_file_path)
        print(f"Key file '{key_file_path}' has been removed.")

# Main script
if __name__ == "__main__":
    # Check if the script is running with admin privileges
    if not is_admin():
        print("Re-running script with administrator privileges...")
        # If not admin, restart the script with elevated privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    # Folder path to decrypt
    folder_to_decrypt = "C:/mysql/data/demo"
    
    

    # Decrypt the files
    decrypt_myd_files_in_folder(folder_to_decrypt)
    
    # Optionally, remove the key file after decryption
    remove_key_file()

    # Stop the MySQL service
    stop_mysql_service()
    # Start the MySQL service again after decryption
    start_mysql_service()
