import requests
from ui import update_ui
from speech import ui_speak

def grammar_check(text):
    try:
        api_url = "https://api.textgears.com/grammar?text={text}&key=SS6dxbM7xRXFiZUC"
        response = requests.get(api_url)
        if response.status_code == 200:
            result = response.json()
            return result['result']
        else:
            return "Failed to check grammar."
    except Exception as e:
        return f"Error in grammar check: {str(e)}"

def spell_check(text):
    try:
        api_url = f"https://api.textgears.com/spelling?text={text}&key=SS6dxbM7xRXFiZUC"
        response = requests.get(api_url)
        if response.status_code == 200:
            result = response.json()
            return result['result']
        else:
            return "Failed to check spelling."
    except Exception as e:
        return f"Error in spell check: {str(e)}"

def get_synonyms(word):
    try:
        api_url = f"https://api.datamuse.com/words?rel_syn={word}"
        response = requests.get(api_url)
        if response.status_code == 200:
            synonyms = [item['word'] for item in response.json()]
            return synonyms
        else:
            return "Failed to retrieve synonyms."
    except Exception as e:
        return f"Error in retrieving synonyms: {str(e)}"

def process_writing_command(text):
    grammar_result = grammar_check(text)
    spell_result = spell_check(text)
    update_ui(f"Grammar Check: {grammar_result}")
    ui_speak(f"Grammar Check: {grammar_result}")
    update_ui(f"Spell Check: {spell_result}")
    ui_speak(f"Spell Check: {spell_result}")
