import pygame
import time
import math
from random import choice
from math import inf as infinity

window_title = "Gomoku"
font = (size, style) = (16, "comicsansms")
FPS = 5
screen_size = (width, height) = (450, 450)
(rows, columns) = (15, 15)

# init color
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

# init status x an o
x_turn = True
o_turn = False

HUMAN = -1
COMP = 1

input = []

array_squares = [["." for _ in range(columns)] for _ in range(rows)]
matrix_squares = []

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption(window_title)

keys = pygame.key.get_pressed()
clock = pygame.time.Clock()
ox_style = pygame.font.SysFont(style, size)
msg_style = pygame.font.SysFont(style, 40)


def board():
    screen.fill(white)
    padding = width // rows
    for i in range(rows):
        x = i * padding
        if x > 0:
            pygame.draw.line(screen, black, (0, x), (width, x))
            pygame.draw.line(screen, black, (x, 0), (x, height))
    pygame.display.update()


def init_grid():
    global matrix_squares
    dis_to_cen = width // rows // 2
    for row in range(rows):
        for col in range(len(array_squares[row])):
            x = dis_to_cen * (2 * col + 1)
            y = dis_to_cen * (2 * row + 1)
            array_squares[row][col] = (x, y, ".", True)
    matrix_squares = array_squares


def click_square(board):
    global x_turn, o_turn, matrix_squares
    # mouse_position
    m_x, m_y = pygame.mouse.get_pos()
    for row in range(rows):
        for col in range(len(board[row])):
            x, y, sign, can_play = board[row][col]
            dis_mouse_cen = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
            if dis_mouse_cen < width // rows // 2 and can_play == True:
                if x_turn:
                    input.append((x, y, "x"))
                    board[row][col] = (x, y, "x", False)
                    x_turn = False
                    o_turn = True
                elif o_turn:
                    input.append((x, y, "o"))
                    board[row][col] = (x, y, "o", False)
                    o_turn = False
                    x_turn = True
                    depth = len(empty_cells(board))
                    if depth == 0 or check_won(board):
                        return
                    print(depth)
                    # if depth == 9:
                    # x = choice([0, 1, 2])
                    # y = choice([0, 1, 2])
                    # else:
                    move = minimax(board, depth, COMP)

                    print(move)


def ox_show(val, x, y):
    value = ox_style.render(val, True, black)
    screen.blit(value, (x - size // 3, y - size))


def evaluate(board):
    if check_won(board) == ("o", True):
        score = 1

    elif check_won(board) == ("x", True):
        score = -1

    elif check_draw(board):
        score = 0

    return score


def check_won(board):
    # vertical
    for col in range(len(board[0])):
        for row in range(len(board)):
            try:
                if board[row][col][2] == "x" and board[row + 1][col][2] == "x" and board[row + 2][col][2] == "x" and \
                        board[row + 3][col][2] == "x" and board[row + 4][col][2] == "x":
                    return ("x", True)
                elif board[row][col][2] == "o" and board[row + 1][col][2] == "o" and board[row + 2][col][2] == "o" and \
                        board[row + 3][col][2] == "o" and board[row + 4][col][2] == "o":
                    return ("o", True)
            except Exception as e:
                pass

    # horizontal
    for row in range(len(board)):
        for col in range(len(board[0])):
            try:
                if board[row][col][2] == "x" and board[row][col + 1][2] == "x" and board[row][col + 2][2] == "x" and \
                        board[row][col + 3][2] == "x" and board[row][col + 4][2] == "x":
                    return ("x", True)
                elif board[row][col][2] == "o" and board[row][col + 1][2] == "o" and board[row][col + 2][2] == "o" and \
                        board[row][col + 3][2] == "o" and board[row][col + 4][2] == "o":
                    return ("o", True)

                # diagonal
                # /
                if board[row][col][2] == "x" and board[row + 1][col + 1][2] == "x" and board[row + 2][col + 2][
                    2] == "x" and board[row + 3][col + 3][2] == "x" and board[row + 4][col + 4][2] == "x":
                    return ("x", True)
                elif board[row][col][2] == "o" and board[row + 1][col + 1][2] == "o" and board[row + 2][col + 2][
                    2] == "o" and board[row + 3][col + 3][2] == "o" and board[row + 4][col + 4][2] == "o":
                    return ("o", True)
                # \
                elif board[row][col + 4][2] == "x" and board[row + 1][col + 3][2] == "x" and board[row + 2][col + 2][
                    2] == "x" and board[row + 3][col + 1][2] == "x" and board[row + 4][col][2] == "x":
                    return ("x", True)
                elif board[row][col + 4][2] == "o" and board[row + 1][col + 3][2] == "o" and board[row + 2][col + 2][
                    2] == "o" and board[row + 3][col + 1][2] == "o" and board[row + 4][col][2] == "o":
                    return ("o", True)
            except Exception as e:
                pass


def check_draw(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col][2] == "":
                return False
    return True


def empty_cells(board):
    cells = []

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell[2] == ".":
                cells.append([x, y])
    return cells


def minimax(board, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or check_won(board):
        score = evaluate(board)
        return [-1, -1, score]
    for cell in empty_cells(board):
        x, y = cell[0], cell[1]
        board[x][y] = player
        score = minimax(board, depth - 1, -player)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # maxvalue
        else:
            if score[2] < best[2]:
                best = score  # minvalue
    return best


def display_message(message):
    screen.fill(black)
    message = msg_style.render(message, 1, white)
    screen.blit(message, ((width - message.get_width()) //
                          2, (height - message.get_height()) // 2))


def ai_turn(board):
    global x_turn, o_turn, matrix_squares
    depth = len(empty_cells(board))
    if depth == 0 or check_won(board):
        return
    if depth == 225:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]
    print(x, y)
    o_turn = False
    x_turn = True
    # print(move[0], move[1])


def human_turn(board):
    global x_turn, o_turn, matrix_squares
    # mouse_position
    m_x, m_y = pygame.mouse.get_pos()
    for row in range(rows):
        for col in range(len(board[row])):
            x, y, sign, can_play = board[row][col]
            dis_mouse_cen = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
            if dis_mouse_cen < width // rows // 2 and can_play == True:
                if x_turn:
                    input.append((x, y, "x"))
                    board[row][col] = (x, y, "x", False)
                    x_turn = False
                    o_turn = True


def game_loop():
    game_over = False
    game_close = False
    init_grid()
    global matrix_squares
    while not game_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_close = True
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    input.clear()
                    game_loop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                human_turn(matrix_squares)
        # print(matrix_squares)
        board()
        ai_turn(matrix_squares)
        for i in input:
            x, y, val = i
            ox_show(val, x, y)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == "__main__":
    game_loop()
