import time
import os
import subprocess
from datetime import datetime

def is_process_running(process_names):
    try:
        tasks = subprocess.check_output(['tasklist']).decode()  
        return any(name in tasks for name in process_names)  
    except Exception as e:
        print(f"Error checking for processes: {e}")
        return False

def close_process(process_name):
    try:
        subprocess.call(f'taskkill /F /IM {process_name}', shell=True)  
        print(f"{process_name} closed.")
    except Exception as e:
        print(f"Error closing {process_name}: {e}")

if __name__ == "__main__":
    process_names = ["SQLyogCommunity.exe", "OpenDental.exe"]
    
    process_running = False
    encryption_done = False

    while True:
        current_time = datetime.now().strftime("%H:%M")
        current_day = datetime.now().strftime("%Y-%m-%d")
        
        if current_time == "20:00" and not encryption_done:
            if is_process_running(["OpenDental.exe"]):
                print("It's 20:00. Closing OpenDental...")
                close_process("OpenDental.exe")  
            
            if is_process_running(["SQLyogCommunity.exe"]):
                print("It's 20:00. Closing SQLyog...")
                close_process("SQLyogCommunity.exe")  
            
            time.sleep(5)  
            
            print("Running encryption after closing applications...")
            os.system('python ./encryption.py') 
            encryption_done = True  
            process_running = False 
            time.sleep(10)  

        elif is_process_running(process_names):
            if not process_running:
                print("One of the specified processes is running. Running decryption...")
                os.system('python ./decryption.py')  
                process_running = True  
                time.sleep(10)  

        else:
            if process_running and not encryption_done:
                print("None of the specified processes are running. Running encryption...")
                os.system('python ./encryption.py')  
                process_running = False  
                time.sleep(10)  

        if datetime.now().strftime("%Y-%m-%d") != current_day:
            encryption_done = False  

        time.sleep(5)  
