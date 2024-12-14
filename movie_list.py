movies_list = []

def add_movie(title):
    movies_list.append(title)
    return f"'{title}' has been added to your movies to watch list."

def view_movies_list():
    return movies_list if movies_list else "Your movies to watch list is empty."

def process_movies_command(command, title=None):
    if command == "add":
        return add_movie(title)
    elif command == "view":
        return view_movies_list()
    else:
        return "Invalid command for movies list."
