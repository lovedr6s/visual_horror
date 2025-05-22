import json


def save_level(level=0):
    with open('game/saves/save_file.txt', 'w') as file:
        file.write(str(level))


def load_level():
    with open('game/saves/save_file.txt', 'r') as file:
        level = file.read()
    return int(level)


def load_text_file(file_path):
    with open(file_path, 'r') as file:
        text = json.load(file)
    return text
