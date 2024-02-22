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


def get_new_player_position(player_width, player_height, map_width, map_height):
    rand_x, rand_y = random.random(), random.random()
    x, y = position_scaler(rand_x, rand_y, player_width, player_height, map_width, map_height)
    return x, y


def position_scaler(x, y, player_width, player_height, map_width, map_height):
    minimum_x = int(player_width / 2)
    minimum_y = int(player_height / 2)
    maximum_x = map_width - minimum_x - player_width
    maximum_y = map_height - minimum_y - player_height
    # print_types(minimum_x, maximum_x, x)

    new_x = int((x * (maximum_x - minimum_x)) + minimum_x)
    new_y = int((y * (maximum_y - minimum_y)) + minimum_y)

    return new_x, new_y
