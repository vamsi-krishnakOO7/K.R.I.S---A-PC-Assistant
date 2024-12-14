import time
from ui import update_ui
from speech import ui_speak

def start_pomodoro():
    try:
        work_time = 25 * 60  # 25 minutes
        break_time = 5 * 60  # 5 minutes

        update_ui("Starting Pomodoro Timer for 25 minutes of work.")
        ui_speak("Starting Pomodoro Timer for 25 minutes of work.")
        time.sleep(work_time)
        
        update_ui("Work session completed. Take a 5-minute break.")
        ui_speak("Work session completed. Take a 5-minute break.")
        time.sleep(break_time)
        
        update_ui("Break time is over. Ready to start another session?")
        ui_speak("Break time is over. Ready to start another session?")
    except Exception as e:
        update_ui(f"Error in Pomodoro Timer: {str(e)}")
