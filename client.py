import time
import sys
import os

from network import ClientNetwork
from client_settings import *
from utilities import *
from player import Player
import check
from board import Board
import _thread
import argparse
import pickle


def redrawBoxWindow(window, players, clock, font: pygame.font.SysFont):
    window.fill((255, 255, 255))
    for key in players.__reversed__():
        if hasattr(players[key], "draw"):
            players[key].draw(window)
        else:
            print(key)
    fps_counter(window, clock, font)
    pygame.display.update()


def drawBoardPoints(window, boards: list[Board], font: pygame.font.SysFont):
    for i, (_, board) in enumerate(boards.items()):
        colors = board.countCellColors()
        rendered_points = font.render(f"Blue: {colors[0]} Green: {colors[1]} Red: {colors[2]}", 1, POINTS_TEXT_COLOR)
        #window.blit(rendered_points, (0, 0 +TITLE_BAR))
        window.blit(rendered_points, (0 + WIDTH * i + BORDER_WIDTH * i, 0 + TITLE_BAR))


        

def redrawBoardWindow(window, boards, clock, font):
    window.fill((255, 255, 255))

    for i, board_index in enumerate(boards):
        boards[board_index].draw(window, offset_x=i * WIDTH + BORDER_WIDTH * i, offset_y=TITLE_BAR)
        title_rect = (WIDTH * i + (TITLE_BAR * i), 0, WIDTH + BORDER_WIDTH, TITLE_BAR)
        border_rect = (WIDTH * (i + 1) + BORDER_WIDTH * i, 0, BORDER_WIDTH, HEIGHT + TITLE_BAR)
        pygame.draw.rect(window, TITLE_BAR_COLOR, title_rect)

        rendered_player_name = font.render(boards[board_index].name, 1, PLAYER_NAME_TEXT_COLOR)
        text_width, text_height = font.size(boards[board_index].name)
        window.blit(rendered_player_name, (int(WIDTH / 2 + (WIDTH + BORDER_WIDTH) * i) - int(text_width / 2), 0))

        # pygame.draw.
        pygame.draw.rect(window, BORDER_COLOR, border_rect)
    drawBoardPoints(window, boards, font)
    fps_counter(window, clock, font)
    pygame.display.update()


def update_players(player_data_from_server, player_one):
    player_data_from_server["p1"] = player_one
    return player_data_from_server


def show_game_modes(game_list):
    print("The games you can select are:")
    for i, game in enumerate(game_list):
        print(f"{i}:{game}")


def threaded_receiver(client_connection: ClientNetwork, data_dict) -> None:
    """
    Updates data_dict with data from server
    :param client_connection: n Network
    :param data_dict: dict of data. e.g boards or players d= {"p1": Board(), "127.0.0.1, 50242: Board()}
    :return:
    """
    while True:
        try:
            other_players = client_connection.getPlayers(data_dict["p1"])
            for player_name, other_player_board in other_players.items():
                data_dict[player_name] = other_player_board
            time.sleep(1 / GAME_SERVER_UPDATES_PER_SECOND)
        except Exception as e:
            print(f"Unknown error: {e}")
            break

    client_connection.socket.close()


def arg_int_or_string(arg):
    selections = set("0", "1")
    try:
        return int(arg)
    except ValueError:
        pass
    if arg in selections:
        return arg


def argparse_setup():
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", help="Given number or name of game to skip initial input, e.g. 0, 1, Box or Ping")
    parser.add_argument("--server", help="IP of server e.g. 127.0.0.1", type=str)
    parser.add_argument("--port", help="IP of server e.g. 5555", type=int)
    return parser.parse_args()


def main():
    args = argparse_setup()
    run = True
    pygame.font.init()
    n = ClientNetwork(args.server, args.port)
    connection_data = (n.getConnectionData())
    if not connection_data:
        print("No answer from server, exiting")
        return

    if args.game:
        game_selection = args.game
    elif DEFAULT_GAME:
        game_selection = DEFAULT_GAME
    else:
        show_game_modes(connection_data)
        game_selection = input("What you wanna play?")
    # server_response_data = n.send_and_receive(game_selection)
    # server_response_data = pickle.loads(n.socket.recv(2048))
    n.socket.sendall(game_selection.encode())
    server_response_data = pickle.loads(n.socket.recv(2048))
    if not isinstance(server_response_data, (Board, Player)):
        print("Your selection were not implemented, and were rejected by server")
        return
    # print(server_response_data)


    font = pygame.font.SysFont("Arial", 18, bold=True)

    pygame.display.set_caption(GAME_CAPTION)
    clock = pygame.time.Clock()
    counter = 0
    players, last_players = 1, 1

    if game_selection == "0" or game_selection == "Box":
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        p: Player = server_response_data
        players = {"p1": p}

        _thread.start_new_thread(threaded_receiver, (n, players))
        while run:
            clock.tick(60)
            # other_players = n.getPlayers(p)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            # for player_name, player in other_players.items():
            #    players[player_name] = player
            p.move()
            redrawBoxWindow(win, players, clock, font)

        pygame.quit()
    elif game_selection == "1" or game_selection == "Ping":
        # win = pygame.display.set_mode((WIDTH * 2 + BORDER_WIDTH, HEIGHT))
        win = pygame.display.set_mode((WIDTH, HEIGHT + TITLE_BAR))
        board: Board = server_response_data
        boards = {"p1": board}

        _thread.start_new_thread(threaded_receiver, (n, boards))
        while run:
            try:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                if counter % 60 == 0:
                    check.corrupt_board(board.board)

                players = len(boards)
                if players > 1 and players != last_players:
                    print(f"Changing resolution, there are now {players} players and there were {last_players}")
                    pygame.display.set_mode((players * WIDTH + BORDER_WIDTH * (players - 1), HEIGHT + TITLE_BAR))
                    last_players = players

                counter += 1
                redrawBoardWindow(win, boards, clock, font)
            except KeyboardInterrupt:
                print("Keyboard Interrupt: Quitting:")
                break
            except ConnectionResetError as e:
                if e.winerror == 10054:
                    print(f"Server disconnected")
                else:
                    print(f"Unexpected connection reset error {e}")
                break
            except Exception as e:
                print(f"Unexpected error {e}")

                break

        pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
