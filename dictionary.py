import requests
from ui import update_ui
from speech import ui_speak

def get_word_definition(word):
    
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    if response.status_code == 200:
        definitions = response.json()
        try:
            # Extracting the first definition of the first meaning of the word
            definition = definitions[0]['meanings'][0]['definitions'][0]['definition']
            return definition
        except (IndexError, KeyError):
            return "Definition not found."
    else:
        return "Failed to retrieve the definition."

def process_dictionary_command(word):
    definition = get_word_definition(word)
    update_ui(f"Definition of {word}: {definition}")
    ui_speak(f"Definition of {word} is: {definition}")