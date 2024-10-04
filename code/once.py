import os
import subprocess
import time

# Function to start a script and return the process
def start_script(script_name):
    return subprocess.Popen(['python', script_name])

# Start the encryption script
encryption_process = start_script('./encryption.py')

# Start the monitor script
monitor_process = start_script('./monitor.py')

# Optional: Wait for the encryption script to finish (if needed)
# encryption_process.wait()

# Keep the script running (or you can set your own logic here)
try:
    while True:
        time.sleep(1)  # Keep alive, or implement logic to check for process health
except KeyboardInterrupt:
    print("Stopping processes...")
    encryption_process.terminate()
    monitor_process.terminate()
