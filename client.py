import pygame
from network import Network
from client_settings import *
from utilities import *
from player import Player


def redrawWindow(window, players, clock, font):
    window.fill((255, 255, 255))
    for player in players.values():
        player.draw(window)
    fps_counter(window, clock, font)
    pygame.display.update()


def fps_counter(window, clock, font):
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps, 1, pygame.Color("RED"))
    window.blit(fps_t, (5, 5))


def main():
    # Use a breakpoint in the code line below to debug your script. Ctrl+F8 to breakpoint
    run = True
    pygame.font.init()
    n = Network()
    connection_data = (n.getConnectionData())
    new_player_data = decode_new_player_data(connection_data)

    p = Player(new_player_data["pos"], PLAYER_WIDTH, PLAYER_HEIGHT, (0, 255, 0))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 18, bold=True)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)

    players = {"p1": p}

    while run:
        clock.tick(60)

        other_players = decode_new_player_data(n.send(str(p.x) + " " + str(p.y)))
        for player_name, value in other_players.items():
            (x, y) = map(int, value)
            players[str(player_name)] = Player((x, y), PLAYER_WIDTH, PLAYER_HEIGHT)

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
