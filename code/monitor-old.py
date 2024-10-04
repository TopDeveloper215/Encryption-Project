import time
import os
import subprocess

# Function to check if a process is running
def is_process_running(process_names):
    try:
        # List all processes
        tasks = subprocess.check_output(['tasklist']).decode()
        # Check if any of the process names are in the task list
        return any(name in tasks for name in process_names)
    except Exception as e:
        print(f"Error checking for processes: {e}")
        return False

# Main monitoring loop
if __name__ == "__main__":
    # List of process names to check for
    process_names = ["SQLyogCommunity.exe", "OpenDental.exe"]
    
    # Flags to track if decryption or encryption has been performed
    process_running = False

    # Continuous loop
    while True:
        # Check if either of the target processes is running
        if is_process_running(process_names):
            # If the process is running and encryption is currently active
            if not process_running:
                print("One of the specified processes is running. Running decryption...")
                os.system('python ./decryption.py')  # Execute the decryption Python script
                process_running = True  # Mark the process as running (decryption done)
                time.sleep(10)  # Give time to complete the decryption

        else:
            # If no process is running and decryption has been performed
            if process_running:
                print("None of the specified processes are running. Running encryption...")
                os.system('python ./encryption.py')  # Execute the encryption Python script
                process_running = False  # Mark the process as stopped (encryption done)
                time.sleep(10)  # Give time to complete the encryption

        time.sleep(5)  # Check every 5 seconds
