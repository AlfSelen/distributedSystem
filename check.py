import random

BOARD_SIZE = 15


def gen_board(board_size: int):
    board = [[int(random.random() * 100) for _ in range(board_size)] for _ in range(board_size)]
    return board


def corrupt_board(board):
    board_len = len(board)
    a, b = map(int, (random.random() * board_len, random.random() * board_len))
    board[a][b] = int(random.random() * 100)
