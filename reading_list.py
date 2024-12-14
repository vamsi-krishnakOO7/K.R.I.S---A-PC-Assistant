reading_list = []

def add_book(title):
    reading_list.append(title)
    return f"'{title}' has been added to your reading list."

def view_reading_list():
    return reading_list if reading_list else "Your reading list is empty."

def process_reading_command(command, title=None):
    if command == "add":
        return add_book(title)
    elif command == "view":
        return view_reading_list()
    else:
        return "Invalid command for reading list."
