import socket
import threading
import _thread
import sys
from server_settings import *
from utilities import *
import client_settings
import json
from time import time, sleep
import pickle
from player import Player
from board import Board
from check import *


def print_types(*args):
    for arg in args:
        print(type(arg))


def new_player():
    pos = get_new_player_position()
    color = get_new_player_color()
    jsn = {
        "pos": pos,
        "color": color
    }
    return jsn


def create_new_player():
    new_player = Player(get_new_player_position(client_settings.PLAYER_WIDTH, client_settings.PLAYER_HEIGHT, client_settings.WIDTH, client_settings.HEIGHT), client_settings.PLAYER_WIDTH, client_settings.PLAYER_HEIGHT, get_new_player_color())
    return new_player


def create_new_board():
    new_board = gen_board(10)
    return Board(new_board, client_settings.WIDTH, gen_random_name())


def threaded_timer(timer, player_data: dict):
    while True:
        if time() - timer > 5 and player_data:
            timer = time()
            copied_player_data = player_data.copy()
            for player_name, player_obj in copied_player_data.items():
                print(player_name, ":", (player_obj.x, player_obj.y), end="\t")
            print()
        else:
            sleep(5)


def game_options():
    return ["Box", "Ping"]


def threaded_client(client_connection, client_address, player_positions, player_boards):
    client_connection.send(pickle.dumps(game_options()))
    game_selection = client_connection.recv(2048).decode()
    print(f"{client_address} wanna play {game_selection}")
    if game_selection == "0" or game_selection == game_options()[0]:
        new_player_data = create_new_player()
        client_connection.send(pickle.dumps(new_player_data))
        while True:
            try:
                data = client_connection.recv(2048)
                if not data:
                    print(f"Client {client_address} disconnected")
                    break
                else:
                    reply = pickle.loads(data)
                    update_player_position(player_positions, client_address, reply)
                    player_pos = player_positions.pop(str(client_address))
                    client_connection.sendall(pickle.dumps(player_positions))
                    player_positions[str(client_address)] = player_pos

            except Exception as e:
                print(f"Unknown error: {e}")
                break
        remove_player_position(player_positions, client_address)
        client_connection.close()


    elif game_selection == "1" or game_selection == game_options()[1]:
        # response = "NO"
        # client_connection.send(pickle.dumps(response))
        # client_connection.close()
        # print(f"Client {client_address} disconnected by server")
        # return
        new_board_data = create_new_board()
        client_connection.send(pickle.dumps(new_board_data))
        # client_connection.send(pickle.dumps("Just initializing"))
        while True:
            try:
                data = client_connection.recv(2048)
                if not data:
                    print(f"Client {client_address} disconnected")
                    break
                else:
                    reply = pickle.loads(data)
                    update_player_board(player_boards, client_address, reply)
                    player_board = player_boards.pop(str(client_address))
                    client_connection.sendall(pickle.dumps(player_boards))
                    player_boards[str(client_address)] = player_board

            except Exception as e:
                print(f"Unknown error: {e}")
                break
        remove_player_position(player_boards, client_address)
        client_connection.close()

    # update_player_position(player_positions, client_address, new_player_data["pos"])


def update_player_position(dic, player_name, box_obj):
    dic[str(player_name)] = box_obj


def update_player_board(dic, player_name, board_obj):
    dic[str(player_name)] = board_obj


def remove_player_position(dic, player_name):
    dic.pop(str(player_name))


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc.bind((SERVER_IP, SERVER_PORT))
    except socket.error as e:
        print(str(e))

    soc.listen(MAX_BACKLOG_CONNECTIONS)
    print("Waiting for a connection, server started")

    player_positions = {}
    player_boards = {}

    timer = time()
    _thread.start_new_thread(threaded_timer, (timer, player_positions))

    while True:

        try:
            connection, cli_address = soc.accept()
            print("Connected to:", cli_address)
            _thread.start_new_thread(threaded_client, (connection, cli_address, player_positions, player_boards))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping server")
            soc.close()
        except Exception as e:
            print(f"Unexpected error {e}")
            soc.close()
            break


if __name__ == '__main__':
    main()
