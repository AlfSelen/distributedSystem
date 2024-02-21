import json
import random

def pos_encode(pos):
    x, y = pos
    """takes X, Y position transforms to 'X#Y' and encodes"""
    return f"{str(x)} {str(y)}".encode()


def pos_decode(position):
    """from character format of X#Y e.g. 51#373 to x,y"""
    x, y = map(int, position.split())
    return x, y


def color_encode(color):
    return "Color:" + " ".join(map(str, color))


def decode_new_player_data(json_text):
    json_obj = json.loads(json_text)
    return json_obj

def get_new_player_color():
    return int(random.random() * 255), int(random.random() * 255), int(random.random() * 255)
