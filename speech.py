import speech_recognition as sr
import pyttsx3
from ui import update_ui

engine = pyttsx3.init()

def ui_speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
        # Update the UI with the text
        update_ui(text)
    except Exception as e:
        update_ui(f"An Error has Occured while Speaking: {str(e)}")   

def listen_for_input(recognizer, source, prompt, phrase_time_limit=3):
    update_ui(prompt)
    try:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=phrase_time_limit)
        try:
            text = recognizer.recognize_google(audio)
            update_ui(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            update_ui("Could not understand the audio")
            return None
        except sr.RequestError as reqerr:
            update_ui(f"Could not request results; {reqerr}")
            return None
    except Exception as e:
        update_ui(f"An error has occured while Listening: {str(e)}")
        return None