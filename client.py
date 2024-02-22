import pygame
from network import Network
from client_settings import *
from utilities import *
from player import Player


def redrawWindow(window, players, clock, font):
    window.fill((255, 255, 255))
    for player in players.__reversed__():
        if hasattr(players[player], "draw"):
            players[player].draw(window)
        else:
            print(player)
    fps_counter(window, clock, font)
    pygame.display.update()


def fps_counter(window, clock, font):
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps, 1, pygame.Color("RED"))
    window.blit(fps_t, (5, 5))


def main():
    run = True
    pygame.font.init()
    n = Network()
    connection_data = (n.getConnectionData())
    new_player_data = decode_new_player_data(connection_data)

    p = Player(new_player_data["pos"], PLAYER_WIDTH, PLAYER_HEIGHT, get_new_player_color())
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 18, bold=True)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)

    players = {"p1": p}

    while run:
        clock.tick(60)
        other_players = n.getPlayers(p)
        for player_name, player in other_players.items():
            players[str(player_name)] = player

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        p.move()
        redrawWindow(win, players, clock, font)

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
