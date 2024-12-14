from ui import initialize_ui, update_ui
from speech import ui_speak, listen_for_input
from applications import open_application, find_and_open_file
from web import perform_web_search, get_weather, get_news
from system import get_cpu_info, get_memory_info, get_disk_info, open_system_settings
from dictionary import process_dictionary_command
#from reminder import authenticate_google, create_reminder
from pomodoro import start_pomodoro
from writing_assistant import process_writing_command
from reading_list import process_reading_command
from movie_list import process_movies_command
import speech_recognition as sr
from datetime import datetime, timedelta, time
from plyer import notification
import dateparser
from threading import Thread
from applications import APPLICATION_MAP
import os
import noisereduce as nr
import numpy as np

USER_NAME = "ENTER USER NAME"
ASSISTANT_NAME = "ENTER ASSISTANT NAME"

def customized_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = f"Good morning {USER_NAME}, this is {ASSISTANT_NAME}. What would you like me to assist you with?"
    elif 12 <= current_hour < 18:
        greeting = f"Good afternoon {USER_NAME}, this is {ASSISTANT_NAME}. What would you like me to assist you with?"
    else:
        greeting = f"Good evening {USER_NAME}, this is {ASSISTANT_NAME}. What would you like me to assist you with?"
    update_ui(greeting)
    ui_speak(greeting)
    return greeting

def display_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,  # Path to an .ico file if you have one; otherwise, this can be None
        timeout=10,  # Duration in seconds before the notification disappears
    )

def listen_and_execute_commands():
    recognizer = sr.Recognizer()
    #service = authenticate_google()  # Authenticate Google Calendar API
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        customized_greeting()
        listening = True
        while listening:
            update_ui("\nListening for your command...")
            found = False
            try:
                audio = recognizer.listen(source, timeout=5)
                audio_data = np.frombuffer(audio.get_raw_data(), np.int16)
                reduced_noise_data = nr.reduce_noise(y=audio_data, sr=source.SAMPLE_RATE)
                reduced_audio = sr.AudioData(reduced_noise_data.tobytes(), source.SAMPLE_RATE, 2)
                command = recognizer.recognize_google(reduced_audio).lower()
                update_ui(f"You said: {command}")

                if 'stop' in command:
                    SIGNING_OFF = f"Assistant signing off. Goodbye {USER_NAME}"
                    update_ui(SIGNING_OFF)
                    ui_speak(SIGNING_OFF)
                    listening = False
                    ui_root.after(1000, ui_root.destroy)
                    break
                #elif 'create reminder' in command:
                    #summary = listen_for_input(recognizer, source, "What is the reminder about?")
                    #description = listen_for_input(recognizer, source, "Any description for the reminder?")
                    #date_str = listen_for_input(recognizer, source, "On what date? Please say it in DD-MM-YYYY format.")
                    #time_str = listen_for_input(recognizer, source, "At what time? Please say it in HH:MM format.")
                    
                    #start_date = dateparser.parse(date_str, settings={'DATE_ORDER': 'DMY'})
                    #if start_date and len(time_str) == 4 and time_str.isdigit():
                        #hours=int(time_str[:2])
                        #minutes=int(time_str[2:])
                        #combined_start_datetime = datetime.combine(start_date.date(), time(hour=hours, minute=minutes))
                        #end_time = combined_start_datetime + timedelta(minutes=10)
                        #create_reminder(service, summary, description, combined_start_datetime, end_time)
                    #else:
                        #update_ui("Failed to parse date or time.")
                    #found = True
                        
                elif 'open file' in command:
                    filename = command.replace('open file ', '').strip()
                    find_and_open_file(filename)
                    found = True
                elif 'search for' in command:
                    query = command.replace('search for ', '')
                    perform_web_search(query)
                    found = True
                elif 'weather' in command:
                    city = command.replace('weather in ', '')
                    get_weather(city)
                    found = True
                elif 'news' in command:
                    get_news()
                    found = True
                elif 'system info' in command or 'cpu usage' in command:
                    cpu_info = get_cpu_info()
                    update_ui(cpu_info)
                    ui_speak(cpu_info)
                    found = True
                elif 'memory info' in command:
                    memory_info = get_memory_info()
                    update_ui(memory_info)
                    ui_speak(memory_info)
                    found = True
                elif 'disk info' in command:
                    disk_info = get_disk_info()
                    update_ui(disk_info)
                    ui_speak(disk_info)
                    found = True
                elif 'bluetooth' in command:
                    open_system_settings("bluetooth")
                    found = True
                elif 'define' in command or 'what is the meaning of' in command:
                    word = command.replace('define ', '').replace('what is the meaning of ', '')
                    process_dictionary_command(word)
                    found = True
                elif command.lower() in ['full form', 'your name', 'yourself']:
                    ACRONYM = "My name KRIS, is short for - Knowledgeable Responsive Interface System"
                    update_ui(ACRONYM)
                    ui_speak(ACRONYM)
                    found = True
                elif 'wi-fi' in command:
                    open_system_settings("wifi")
                    found = True
                elif 'pomodoro' in command:
                    start_pomodoro()
                    found = True
                elif 'writing assistant' in command:
                    text = command.replace('writing assistant ', '')
                    process_writing_command(text)
                    found = True
                elif 'add book' in command:
                    title = command.replace('add book ', '')
                    response = process_reading_command("add", title)
                    update_ui(response)
                    ui_speak(response)
                    found = True
                elif 'view reading list' in command:
                    response = process_reading_command("view")
                    update_ui(response)
                    ui_speak(response)
                    found = True
                elif 'add movie' in command:
                    title = command.replace('add movie ', '')
                    response = process_movies_command("add", title)
                    update_ui(response)
                    ui_speak(response)
                    found = True
                elif 'view movies list' in command:
                    response = process_movies_command("view")
                    update_ui(response)
                    ui_speak(response)
                    found = True
                else:
                    for app in APPLICATION_MAP:
                        if app in command:
                            open_application(app)
                            found = True
                            break
                if not found:
                    update_ui("Sorry, I did not understand the command.")
            except sr.UnknownValueError:
                update_ui("I could not understand the audio.")
            except sr.RequestError as e:
                update_ui(f"Could not request results; {e}")

def main():
    global ui_root, ui_text
    ui_root, ui_text = initialize_ui()
    
    Thread(target=listen_and_execute_commands, daemon=True).start()
    ui_root.mainloop()

if __name__ == "__main__":
    main()