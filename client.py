import pygame
from network import Network
from client_settings import *
from utilities import *
from player import Player


def redrawWindow(window, players, clock, font):
    window.fill((255, 255, 255))
    for key in players.__reversed__():
        if hasattr(players[key], "draw"):
            players[key].draw(window)
        else:
            print(key)
    fps_counter(window, clock, font)
    pygame.display.update()


def fps_counter(window, clock, font):
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps, 1, pygame.Color("RED"))
    window.blit(fps_t, (5, 5))


def update_players(player_data_from_server, player_one):
    player_data_from_server["p1"] = player_one
    return player_data_from_server


def show_game_modes(game_list):
    print("The games you can select are:")
    for i, game in enumerate(game_list):
        print(f"{i}:{game}")


def main():
    run = True
    pygame.font.init()
    n = Network()
    # n.send(game_selection)
    connection_data = (n.getConnectionData())
    show_game_modes(connection_data)
    game_selection = input("What you wanna play?")
    new_player_data = n.sendTextReceivePickle(game_selection)
    if new_player_data == "NO":
        print("Your selection were not implemented")
        return
    print(new_player_data)
    # new_player_data = connection_data

    p = new_player_data
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 18, bold=True)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)

    players = {"p1": p}

    while run:
        clock.tick(60)
        other_players = n.getPlayers(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for player_name, player in other_players.items():
            players[player_name] = player
        p.move()
        redrawWindow(win, players, clock, font)

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
