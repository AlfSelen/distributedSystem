import socket
import threading
import queue
import concurrent.futures
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
import argparse
from network import ServerNetwork, send_data, load_data, receive


def print_types(*args):
    for arg in args:
        print(type(arg))


# def new_player():
#     pos = get_new_player_position()
#     color = get_new_player_color()
#     jsn = {
#         "pos": pos,
#         "color": color
#     }
#     return jsn


def create_new_player():
    new_player = Player(get_new_player_position(client_settings.PLAYER_WIDTH, client_settings.PLAYER_HEIGHT, client_settings.WIDTH, client_settings.HEIGHT), client_settings.PLAYER_WIDTH, client_settings.PLAYER_HEIGHT, get_new_player_color())
    return new_player


def create_new_board(existing_boards: dict[str, Board]):
    new_board = gen_board(10)
    new_name = gen_random_name()

    existing_board_names = [b.name for b in existing_boards.values()]
    while new_name in existing_board_names:
        new_name = gen_random_name()
    return Board(new_board, client_settings.WIDTH, gen_random_name())


def threaded_timer(timer, player_data: dict, player_boards: dict):
    while True:
        if time() - timer > 5 and player_data:
            timer = time()
            # copied_player_data = player_data.copy()
            # for player_name, player_obj in copied_player_data.items():
            #     print(player_name, player_obj, sep="\t")
            print(f"There are {len(player_boards) + len(player_data)} players connected.")
        else:
            sleep(5)


def game_options():
    return ["Box", "Ping"]


def threaded_client(client_connection: socket.socket, client_address, player_positions, player_boards):
    # server_connection.send((game_options()))
    # server_connection.initial_send(pickle.dumps(game_options()))

    try:
        send_data(client_connection, game_options())
        print("sending game options")
        # game_selection = receive(client_connection)
        game_selection = client_connection.recv(2048).decode()
        print(f"{':'.join(list(map(str, client_address)))} wanna play {game_selection}")

        if game_selection == "0" or game_selection == game_options()[0]:
            # client_connection.send(pickle.dumps(new_player_data))
            new_player_data = create_new_player()
            print(f"sending new_player: {type(new_player_data)}")
            # what_is_this = send_data(client_connection, new_player_data)
            client_connection.sendall(pickle.dumps(new_player_data))
            # print(f"what_is_this:{what_is_this}")
            # server_connection.send(new_player_data)
            while True:
                try:
                    data = receive(client_connection)
                    if not data:
                        print(f"Client {client_address} disconnected")
                        break
                    else:
                        update_player_position(player_positions, client_address, data)
                        player_pos = player_positions.pop(str(client_address))
                        # server_connection.send(player_positions)
                        send_data(client_connection, player_positions)
                        player_positions[str(client_address)] = player_pos
                except ConnectionResetError as e:
                    if e.winerror == 10054:
                        print(f"Client {':'.join(list(map(str, client_address)))} disconnected")
                        break
                except Exception as e:
                    print(f"Unexpected error game:{game_selection} {e}")
                    break
            remove_player_position(player_positions, client_address)

        elif game_selection == "1" or game_selection == game_options()[1]:
            new_board_data = create_new_board(player_boards)
            print(f"sending board: {type(new_board_data)}")
            send_data(client_connection, new_board_data)
            # client_connection.send(pickle.dumps("Just initializing"))

            while True:
                try:
                    # data = client_connection.recv(2048)
                    # data = server_connection.receive()
                    data = receive(client_connection)
                    if not data:
                        print(f"Client {client_address} disconnected")
                        break
                    else:
                        update_player_board(player_boards, client_address, data)
                        player_board = player_boards.pop(str(client_address))
                        # client_connection.sendall(pickle.dumps(player_boards))
                        # server_connection.send(player_boards)
                        send_data(client_connection, player_boards)
                        player_boards[str(client_address)] = player_board

                except ConnectionResetError as e:
                    if e.winerror == 10054:
                        print(f"Connection terminated by client")
                    else:
                        print(f"Unknown connection reset error {e}")
                    break
                except Exception as e:
                    print(f"Unexpected error game:{game_selection} {e}")
                    remove_player_position(player_boards, client_address)
                    break
        else:
            send_data(client_connection, ["No"])
            print(f"Invalid game option terminating {':'.join(list(map(str, client_address)))}")

    finally:
        remove_player_position(player_boards, client_address)
        client_connection.close()
        # client_connection.close()
        # server_connection.close()

    # update_player_position(player_positions, client_address, new_player_data["pos"])


def update_player_position(dic, player_name, box_obj):
    dic[str(player_name)] = box_obj


def update_player_board(dic, player_name, board_obj):
    dic[str(player_name)] = board_obj


def remove_player_position(dic, player_name):
    print(f"checking if {str(player_name)=} in {dic=}")
    if str(player_name) in dic:
        print("removing player from dict")
        dic.pop(str(player_name))


def argparse_setup():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="IP of server e.g. 127.0.0.1", type=str)
    parser.add_argument("--port", help="IP of server e.g. 5555", type=int)
    return parser.parse_args()


def accept_new_connections(server_network: ServerNetwork, player_positions: dict[str, Player], player_boards: dict[str, Board]):
    while True:
        try:
            cli_connection, cli_address = server_network.socket.accept()
            print(f"Connection: {cli_connection}")
            print("Connected to:", ':'.join(list(map(str, cli_address))))
            # _thread.start_new_thread(threaded_client, (cli_connection, cli_address, player_positions, player_boards))
            threading.Thread(target=threaded_client, args=[cli_connection, cli_address, player_positions, player_boards], daemon=True).start()
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping server")
            server_network.socket.close()
            break
        except ConnectionResetError as e:
            if e.winerror == 10054:
                print(f"Client {':'.join(list(map(str, cli_address)))} disconnected")
            else:
                print(f"Unexpected Connection reset error, {e}")
            break
        except Exception as e:
            print(f"Unexpected error {e}")
            break


def accept_admin_commands(command_queue: queue.Queue):
    while True:
        inp = input("Enter command: ")
        # Process the command using the command_queue or directly
        command_queue.put(inp)
        if inp == "exit":
            break


def admin_command_processor(command_queue: queue.Queue):
    try:
        while True:
            command = input("Enter command: ")
            # command = command_queue.get()
            match command:
                case "exit":
                    print("shtting down")
                case "player":
                    ...
                case "conn" | "connection":
                    ...
                case "help" | "h":
                    ...  # print_help()
                case _:
                    print(f"Unknown command {command}")
    except UnicodeDecodeError as e:
        ...
        # this happens when shutting down within an ide, e.g. "stop process"
        # print(f"admin_command_processor Decode : {e}")
    except Exception as e:
        print(f"admin_command_processor shutting down: {e}")


def main():
    args = argparse_setup()

    server_ip = args.server if args.server else SERVER_IP
    server_port = args.port if args.port else SERVER_PORT
    server_network = ServerNetwork(server_ip, server_port)
    print(f"Waiting for a connection, server started on {server_ip}:{server_port}")

    player_positions = {}
    player_boards = {}

    timer = time()

    command_queue = queue.Queue()

    # threading.Thread(target=accept_admin_commands, args=[command_queue], daemon=True).start()
    threading.Thread(target=admin_command_processor, args=[command_queue], daemon=True).start()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # executor.submit(threaded_timer, timer, player_boards, player_positions)
        accept_new_connections(server_network, player_boards, player_boards)
    # while True:
    #
    #     try:
    #         cli_connection, cli_address = server_network.socket.accept()
    #         print(f"Connection: {cli_connection}")
    #         print("Connected to:", ':'.join(list(map(str, cli_address))))
    #         _thread.start_new_thread(threaded_client, (cli_connection, cli_address, player_positions, player_boards))
    #     except KeyboardInterrupt:
    #         print("KeyboardInterrupt: Stopping server")
    #         server_network.socket.close()
    #         break
    #     except ConnectionResetError as e:
    #         if e.winerror == 10054:
    #             print(f"Client {':'.join(list(map(str, cli_address)))} disconnected")
    #         else:
    #             print(f"Unexpected Connection reset error, {e}")
    #         break
    #     except Exception as e:
    #         print(f"Unexpected error {e}")
    #         break

    # while True:
    #     inp = input()
    #     if inp == "player":
    #         print(player_boards)
    #     if inp == "conn" or inp == "connection":
    #         print()
    #     if inp == "clear":
    #         player_boards = {}
    #         player_positions = {}


if __name__ == '__main__':
    main()
