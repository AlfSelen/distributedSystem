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


def print_types(*args):
    for arg in args:
        print(type(arg))


def position_scaler(x, y):
    minimum_x = int(client_settings.PLAYER_WIDTH / 2)
    minimum_y = int(client_settings.PLAYER_HEIGHT / 2)
    maximum_x = client_settings.WIDTH - minimum_x - client_settings.PLAYER_WIDTH
    maximum_y = client_settings.HEIGHT - minimum_y - client_settings.PLAYER_HEIGHT
    # print_types(minimum_x, maximum_x, x)

    new_x = int((x * (maximum_x - minimum_x)) + minimum_x)
    new_y = int((y * (maximum_y - minimum_y)) + minimum_y)

    return new_x, new_y


def get_new_player_position():
    rand_x, rand_y = random.random(), random.random()
    x, y = position_scaler(rand_x, rand_y)
    return x, y


def new_player():
    pos = get_new_player_position()
    color = get_new_player_color()
    jsn = {
        "pos": pos,
        "color": color
    }
    return jsn


def threaded_timer(timer, positions):
    while True:
        if time() - timer > 5 and positions:
            timer = time()
            for player_name, player_obj in positions.items():
                print(player_name, ":", (player_obj.x, player_obj.y), end="\t")
            print()
        else:
            sleep(5)


def threaded_client(client_connection, client_address, player_positions):
    new_player_data = new_player()

    client_connection.send(json.dumps(new_player_data).encode())
    # update_player_position(player_positions, client_address, new_player_data["pos"])
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
                # client_connection.sendall(json.dumps(player_positions).encode())
                client_connection.sendall(pickle.dumps(player_positions))
                player_positions[str(client_address)] = player_pos

            #   print("Received: ", data.decode())
            #   print("Sending: ", reply)
            # client_connection.sendall(reply.encode())
        except Exception as e:
            print(f"Unknown error: {e}")
            break
    remove_player_position(player_positions, client_address)
    client_connection.close()


def update_player_position(dic, player_name, pos):
    dic[str(player_name)] = pos


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

    timer = time()
    _thread.start_new_thread(threaded_timer, (timer, player_positions))

    while True:

        try:
            connection, cli_address = soc.accept()
            print("Connected to:", cli_address)
            _thread.start_new_thread(threaded_client, (connection, cli_address, player_positions))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping server")
            soc.close()
        except Exception as e:
            print(f"Unexpected error {e}")
            soc.close()


if __name__ == '__main__':
    main()
