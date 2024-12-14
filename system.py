import psutil
import subprocess
from ui import update_ui
import speech_recognition as sr

def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"Sure, Your CPU Usage is at {cpu_usage}%"

def get_memory_info():
    memory = psutil.virtual_memory()
    total = round(memory.total / (1024**3), 2)  # Convert to GB
    available = round(memory.available / (1024**3), 2)  # Convert to GB
    used_percentage = memory.percent
    return f"The Total System Memory is {total}GB out of which, {available}GB is available. You have used {used_percentage}% of the total memory"

def get_disk_info():
    disk_usage = psutil.disk_usage('/')
    total = round(disk_usage.total / (1024**3), 2)  # Convert to GB
    used = round(disk_usage.used / (1024**3), 2)  # Convert to GB
    free = round(disk_usage.free / (1024**3), 2)  # Convert to GB
    percentage = disk_usage.percent
    return f"Disk Total: {total}GB, Used: {used}GB, Free: {free}GB, Used Percentage: {percentage}%"

def open_system_settings(setting):
    try:
        if setting == "bluetooth":
            subprocess.run("start ms-settings:bluetooth", shell=True)
        elif setting == "wifi":
            subprocess.run("start ms-settings:network-wifi", shell=True)
        update_ui(f"Opening {setting} settings.")
    except sr.RequestError as e:
                update_ui(f"Could not request results; {e}")