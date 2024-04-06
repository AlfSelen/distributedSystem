import json
import random
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


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


def fps_counter(window, clock, font):
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps, 1, pygame.Color("RED"))
    window.blit(fps_t, (5, 5))


def gen_random_name():
    names = ["Dennisrex",
             "IHasLegs",
             "Dennis Charming Legs",
             # "Dennisasaurus Rex",
             # "Dennis Kind Arm Pits",
             # "Dennis Australian",
             # "Uber Charming Donkey",
             # "Disguised Donkey",
             # "CharmingLegsOMG",
             # "KindLegsLOL",
             # "ViolentLegsOMG",
             # "CharmingArm PitsLOL",
             # "KindArm PitsOMG",
             # "ViolentArm PitsLMAO",
             # "Iamcharming",
             # "Iamkind",
             # "Iamviolent",
             # "IamDennis",
             # "DonkeyMilk",
             # "Dennis Violent Donkey",
             # "MindOfDennis",
             # "Gamerdonkey",
             # "The Charming Gamer",
             # "The Kind Gamer",
             # "The Violent Gamer",
             # "DrCharming",
             # "DennisLegspopper",
             # "BigCharmingDonkey",
             # "ItIsYeDonkey",
             # "D3nn1s",
             # "Donkey Boy",
             # "Donkey Girl",
             # "Donkey Person",
             # "Captain Charming",
             # "IHasArm Pits",
             # "Total Donkey",
             # "The Charming Australian Dude",
             # "The Gaming Donkey",
             # "Gaming With Dennis",
             # "Leondrarex",
             # "IHasArms",
             # "Leondra Noble Arms",
             # "Leondraasaurus Rex",
             # "Leondra Fluffy Insides",
             # "Leondra Australian",
             # "Uber Noble Kitten",
             # "Disguised Kitten",
             # "NobleArmsOMG",
             # "FluffyArmsLOL",
             # "FriendlyArmsOMG",
             # "NobleInsidesLOL",
             # "FluffyInsidesOMG",
             # "FriendlyInsidesLMAO",
             # "Iamnoble",
             # "Iamfluffy",
             # "Iamfriendly",
             # "IamLeondra",
             # "KittenMilk",
             # "Leondra Friendly Kitten",
             # "MindOfLeondra",
             # "Gamerkitten",
             # "The Noble Gamer",
             # "The Fluffy Gamer",
             # "The Friendly Gamer",
             # "DrNoble",
             # "LeondraArmspopper",
             # "BigNobleKitten",
             # "ItIsYeKitten",
             # "L30ndr4",
             # "Kitten Boy",
             # "Kitten Girl",
             # "Kitten Person",
             # "Captain Noble",
             # "IHasInsides",
             # "Total Kitten",
             # "The Noble Australian Dude",
             # "The Gaming Kitten",
             # "Gaming With Leondra",
             # "Mr Game Kitten",
             # "Ms Game Kitten",
             # "Mr Game Donkey",
             "Ms Game Donkey"]
    return random.choice(names)
