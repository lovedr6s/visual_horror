import json


def save_level(level=0):
    """Save the current level to a file."""
    with open('game/saves/save_file.txt', 'w') as file:
        file.write(str(level))


def load_level():
    """Load the current level from a file."""
    with open('game/saves/save_file.txt') as file:
        level = file.read()
    return int(level)


def load_text_file(file_path):
    """Load text from a JSON file."""
    with open(file_path) as file:
        text = json.load(file)
    return text
