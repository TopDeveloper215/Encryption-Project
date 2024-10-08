import os
import subprocess
import time

def start_script(script_name):
    return subprocess.Popen(['python', script_name])

encryption_process = start_script('./encryption.py')
monitor_process = start_script('./monitor.py')

try:
    while True:
        time.sleep(1) 
except KeyboardInterrupt:
    print("Stopping processes...")
    encryption_process.terminate()
    monitor_process.terminate()
