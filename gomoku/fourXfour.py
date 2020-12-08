#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]


def evaluate(state):
    """
    Hàm đánh giá trạng thái
    :param state:  trạng thái hiện tại của bảng
    :return: +1 nếu máy tính thắng ; -1 nếu con người thắng ; 0 hòa
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    Hàm này kiểm tra xem nếu một người chơi cụ thể chiến thắng. Một số khả năng:
    * Three rows    [X X X X] or [O O O O]
    * Three cols    [X X X X] or [O O O O]
    * Two diagonals [X X X X] or [O O O O]
                    [X X X X] or [O O O O]
    :param state: trạng thái hiện tại của bảng
    :param player: con người hay máy tính
    :return: True nếu một trong hai người chơi chiến thắng
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2], state[0][3]],
        [state[1][0], state[1][1], state[1][2], state[1][3]],
        [state[2][0], state[2][1], state[2][2], state[2][3]],
        [state[3][0], state[3][1], state[3][2], state[3][3]],
        [state[0][0], state[1][0], state[2][0], state[3][0]],
        [state[0][1], state[1][1], state[2][1], state[3][1]],
        [state[0][2], state[1][2], state[2][2], state[3][2]],
        [state[0][3], state[1][3], state[2][3], state[3][3]],
        [state[0][0], state[1][1], state[2][2], state[3][3]],
        [state[3][0], state[2][1], state[1][2], state[0][3]],
    ]

    if [player, player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    Kiểm tra nếu con người hoặc máy tính chiến thắng
    :param state: trạng thái hiện tại của bảng
    :return: True nếu con người hoặc máy tính thắng
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Duyệt qua bảng hiện tại, lấy từng ô trống lưu vào Cells
    :param state: trạng thái hiện tại của bảng
    :return: trả về một danh sách các ô trống
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells


def valid_move(x, y):
    """
    Di chuyển là hợp lệ nếu chọn những ô trống
    :param x: tọa độ X
    :param y: tọa độ Y
    :return: True nếu board[x][y] là trống
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    thiết lập di chuyển, nếu tọa đô hợp lệ
    :param x: toa độ X
    :param y: tọa đô Y
    :param player: người chơi hiện tại
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    Hàm này giúp AI chọn được di chuyển tốt nhất
    :param state: trạng thái hiện tại của bảng
    :param depth: số node trên cây (0 <= depth <= 16)
    :param player: lượt của con người hoặc máy tính
    :return: một danh sách với [dòng tốt nhất, cột tốt nhất, điểm cao nhất]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value
    return best


def clean():
    """
    Dọn dẹp console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    in ra bảng trên console
    :param state: trạng thái hiện tại của bảng
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f' {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    # depth = len(empty_cells(board))
    depth = 16
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)
    if depth == 16:
        x = choice([0, 1, 2, 3])
        y = choice([0, 1, 2, 3])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]
    print(x, y)
    if set_move(x, y, COMP):
        return
    else:
        ai_turn(c_choice, h_choice)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    # depth = len(empty_cells(board))
    depth = 16
    if depth == 0 or game_over(board):
        return

    # Từ điển các di chuyển hợp lệ
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3],
        5: [1, 0], 6: [1, 1], 7: [1, 2], 8: [1, 3],
        9: [2, 0], 10: [2, 1], 11: [2, 2], 12: [2, 3],
        13: [3, 0], 14: [3, 1], 15: [3, 2], 16: [3, 3],
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 16:
        try:
            move = int(input('Use numpad (1..16): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop của game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
