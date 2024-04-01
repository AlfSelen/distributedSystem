import time
import sys
import os

import pygame.font

from network import Network
from client_settings import *
from utilities import *
from player import Player
import check
from board import Board
import _thread
import argparse


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
        window.blit(rendered_points, (0 + WIDTH * i + BORDER_WIDTH * i, 0 + TITLE_BAR))


def drawBoardPoint(window, board: Board, font: pygame.font.SysFont, offset: tuple[int, int]):
    colors = board.countCellColors()
    rendered_points = font.render(f"Blue: {colors[0]} Green: {colors[1]} Red: {colors[2]}", 1, POINTS_TEXT_COLOR)
    window.blit(rendered_points, (offset[0], offset[1]+TITLE_BAR))

def redrawBoardWindowHorizontally(window, boards, clock, font):
    window.fill((255, 255, 255))
    for i, (board_index, board) in enumerate(list(boards.items())):
    #for i, board_index in enumerate(boards):
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

def redrawBoardPlayerGridU(window, boards, clock, font):
    window.fill((255, 255, 255))

    #for i, board_index in enumerate(boards):
    for i, (board_index, board) in enumerate(list(boards.items())):
        offset = (((i % 2) * WIDTH), (i % 2) * (HEIGHT+TITLE_BAR))
        drawSinglePlayer(window, boards[board_index], font, offset)

    #drawBoardPoints(window, boards, font)
    fps_counter(window, clock, font)
    pygame.display.update()


def redrawBoardPlayerGrid(window, boards, clock, font):
    window.fill((255, 255, 255))

    num_columns = 2  # Assuming a 2x2 grid
    # Adjust WIDTH and HEIGHT if necessary to fit the window size
    for i, (board_index, board) in enumerate(list(boards.items())):
        # Calculate row and column based on index
        row = i // num_columns
        column = i % num_columns

        # Calculate offset based on row and column
        offset_x = column * (WIDTH + BORDER_WIDTH)
        offset_y = row * (HEIGHT + TITLE_BAR)

        # Pass the calculated offset to the function
        drawSinglePlayer(window, board, font, (offset_x, offset_y))
        drawBoardPoint(window, board, font, (offset_x, offset_y))

    if len(boards) == 3:
        offset_x = (WIDTH + BORDER_WIDTH)
        offset_y = (HEIGHT + TITLE_BAR)
        drawLayout(window, font, (offset_x, offset_y))

    drawBoardPoints(window, boards, font)
    fps_counter(window, clock, font)
    pygame.display.update()



def drawLayout(window, font, offset: tuple[int, int]):
    title_rect = (offset[0], offset[1], WIDTH + BORDER_WIDTH, TITLE_BAR)
    border_rect = (offset[0]-BORDER_WIDTH, offset[1], BORDER_WIDTH, HEIGHT + TITLE_BAR)
    pygame.draw.rect(window, TITLE_BAR_COLOR, title_rect)
    pygame.draw.rect(window, BORDER_COLOR, border_rect)

    rendered_player_name = font.render("Waiting for player", 1, PLAYER_NAME_TEXT_COLOR)
    text_width, text_height = font.size("Waiting for player")
    window.blit(rendered_player_name, (int(WIDTH / 2 + offset[0] - text_width / 2), offset[1]))
def drawSinglePlayer(window, board, font, offset: tuple[int, int]):
    board.draw(window, offset_x=offset[0], offset_y=offset[1] + TITLE_BAR)
    title_rect = (offset[0], offset[1], WIDTH + BORDER_WIDTH, TITLE_BAR)
    border_rect = (offset[0]-BORDER_WIDTH, offset[1], BORDER_WIDTH, HEIGHT + TITLE_BAR)

    rendered_player_name = font.render(board.name, 1, PLAYER_NAME_TEXT_COLOR)
    text_width, text_height = font.size(board.name)
    #window.blit(rendered_player_name, (int(WIDTH / 2 + offset[0] - int(text_width / 2), offset[1])))

    # window.blit(rendered_player_name, (int(WIDTH / 2 + (WIDTH + BORDER_WIDTH) * i) - int(text_width / 2), 0))

    pygame.draw.rect(window, TITLE_BAR_COLOR, title_rect)
    pygame.draw.rect(window, BORDER_COLOR, border_rect)

    window.blit(rendered_player_name, (int(WIDTH / 2 + offset[0] - text_width / 2), offset[1]))





def update_players(player_data_from_server, player_one):
    player_data_from_server["p1"] = player_one
    return player_data_from_server


def show_game_modes(game_list):
    print("The games you can select are:")
    for i, game in enumerate(game_list):
        print(f"{i}:{game}")


def threaded_receiver(client_connection: Network, data_dict) -> None:
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

    client_connection.client.close()


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
    n = Network(args.server, args.port)
    connection_data = (n.getConnectionData())
    if not connection_data:
        print("No answer from server, exiting")
        return
    show_game_modes(connection_data)
    #
    if args.game:
        game_selection = args.game
    elif DEFAULT_GAME:
        game_selection = DEFAULT_GAME
    else:
        game_selection = input("What you wanna play?")
    server_response_data = n.sendTextReceivePickle(game_selection)
    if server_response_data == "NO":
        print("Your selection were not implemented")
    # print(server_response_data)


    font = pygame.font.SysFont("Arial", 18, bold=True)

    pygame.display.set_caption(GAME_CAPTION)
    clock = pygame.time.Clock()
    counter = 0
    player_count, last_players = 1, 1

    if game_selection == "0" or game_selection == "Box":
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        p = server_response_data
        player_count = {"p1": p}

        _thread.start_new_thread(threaded_receiver, (n, player_count))
        while run:
            clock.tick(60)
            # other_players = n.getPlayers(p)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            # for player_name, player in other_players.items():
            #    players[player_name] = player
            p.move()
            redrawBoxWindow(win, player_count, clock, font)

        pygame.quit()
    elif game_selection == "1" or game_selection == "Ping":
        # win = pygame.display.set_mode((WIDTH * 2 + BORDER_WIDTH, HEIGHT))
        win = pygame.display.set_mode((WIDTH, HEIGHT + TITLE_BAR))
        board = server_response_data
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

                player_count = len(boards)
                if player_count > 1 and player_count != last_players:
                    print(f"Changing resolution, there are now {player_count} players and there were {last_players}")
                    last_players = player_count
                    if player_count == 2:
                        pygame.display.set_mode(
                            (player_count * WIDTH + BORDER_WIDTH * (player_count - 1), HEIGHT + TITLE_BAR))
                    else:
                        pygame.display.set_mode(
                            (2 * WIDTH + BORDER_WIDTH, 2 * (HEIGHT + TITLE_BAR)))

                counter += 1
                #redrawBoardWindowHorizontally(win, boards, clock, font)
                redrawBoardPlayerGrid(win, boards, clock, font)
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
