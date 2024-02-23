import time
import sys
import pygame
from network import Network
from client_settings import *
from utilities import *
from player import Player
import check
from board import Board
import _thread


def redrawBoxWindow(window, players, clock, font):
    window.fill((255, 255, 255))
    for key in players.__reversed__():
        if hasattr(players[key], "draw"):
            players[key].draw(window)
        else:
            print(key)
    fps_counter(window, clock, font)
    pygame.display.update()


def redrawBoardWindow(window, boards, clock, font):
    window.fill((255, 255, 255))

    for i, board_index in enumerate(boards):
        boards[board_index].draw(window, offset_x=i * WIDTH + BORDER_WIDTH * i, offset_y=TITLE_BAR)
        # (players * (WIDTH + (BORDER_WIDTH - 1)), HEIGHT)
        title_rect = (WIDTH * i + (TITLE_BAR * i), 0, WIDTH + BORDER_WIDTH, TITLE_BAR)
        border_rect = (WIDTH * (i + 1) + BORDER_WIDTH * i, 0, BORDER_WIDTH, HEIGHT + TITLE_BAR)
        pygame.draw.rect(window, TITLE_BAR_COLOR, title_rect)

        rendered_player_name = font.render(boards[board_index].name, 1, PLAYER_NAME_TEXT_COLOR)
        text_width, text_height = font.size(boards[board_index].name)
        window.blit(rendered_player_name, (int(WIDTH / 2 + (WIDTH + BORDER_WIDTH) * i) - int(text_width / 2), 0))

        # pygame.draw.
        pygame.draw.rect(window, BORDER_COLOR, border_rect)

    fps_counter(window, clock, font)
    pygame.display.update()


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

    client_connection.close()


def main():
    args = sys.argv[1:]
    run = True
    pygame.font.init()
    n = Network()
    # n.send(game_selection)
    connection_data = (n.getConnectionData())
    show_game_modes(connection_data)
    #
    if len(args):
        game_selection = args[0]
    elif DEFAULT_GAME:
        game_selection = DEFAULT_GAME
    else:
        game_selection = input("What you wanna play?")
    server_response_data = n.sendTextReceivePickle(game_selection)
    if server_response_data == "NO":
        print("Your selection were not implemented")
        # return
    print(server_response_data)
    # server_response_data = connection_data

    font = pygame.font.SysFont("Arial", 18, bold=True)

    pygame.display.set_caption(GAME_CAPTION)
    clock = pygame.time.Clock()
    counter = 0
    players, last_players = 1, 1

    if game_selection == "0" or game_selection == "Box":
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        p = server_response_data
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
            except Exception as e:
                print(f"Unknown error: {e}:")
                break

        pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
