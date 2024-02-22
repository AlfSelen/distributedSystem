import pygame
from client_settings import *
from utilities import *
import check


class Board:
    def __init__(self, board: [], board_size, player_name):
        self.board = board
        self.board_size = board_size
        self.cell_size = int(self.board_size / len(board))
        self.name = player_name

    def draw(self, window, offset_x=0, offset_y=0):
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                rect = (self.cell_size * j + offset_x, self.cell_size * i + offset_y, self.cell_size, self.cell_size)
                color = Board.mapColor(col)
                pygame.draw.rect(window, color, rect)

    def print_board(self):
        for row in self.board:
            print(row)

    @staticmethod
    def mapColor(value: int) -> (int, int, int):
        color = (0, 0, 0)
        if value < 33:
            color = (0, 0, 255)
        elif value < 66:
            color = (0, 255, 0)
        elif value < 100:
            color = (255, 0, 0)
        return color


def redrawWindow(window, board, clock, font):
    window.fill((255, 255, 255))

    board.draw(window)
    fps_counter(window, clock, font)
    pygame.display.update()


def main():
    run = True
    new_board = check.gen_board(10)
    board = Board(new_board, WIDTH)

    clock = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.SysFont("Arial", 18, bold=True)
    win = pygame.display.set_mode((WIDTH * 2, HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)

    (board.print_board())
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        check.corrupt_board(board.board)
        redrawWindow(win, board, clock, font)

    pygame.quit()


if __name__ == "__main__":
    main()
