from ui import update_ui
import subprocess
import os
import webbrowser

APPLICATION_MAP = {
    "notepad": "notepad.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
}

SEARCH_DIRECTORY = 'INSERT SEARCH DIRECTORY'

def open_application(application):
    """
    Opens an application based on the provided name if it exists in the mapping.
    """
    path = APPLICATION_MAP.get(application.lower())
    if path:
        try:
            subprocess.Popen(path)
            update_ui(f"{application.title()} opened successfully.")
        except FileNotFoundError:
            update_ui(f"Failed to open {application.title()}. Please check if it is installed.")
    else:
        update_ui(f"{application.title()} is not recognized.")

def find_and_open_file(filename):
    """
    Search for a file in the given directory and open it with the default application.
    """
    try:
        for root, dirs, files in os.walk(SEARCH_DIRECTORY):
            if filename in files:
                file_path = os.path.join(root, filename)
                try:
                    webbrowser.open(file_path)
                    update_ui(f"Opening file: {file_path}")
                    return
                except Exception as e:
                    update_ui(f"Failed to open requested file: {str(e)}")
                    return
        update_ui(f"File '{filename}' not found in {SEARCH_DIRECTORY}.")
    except Exception as e:
        update_ui(f"Error while searching for requested file: {str(e)}")