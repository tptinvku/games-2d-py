import pygame
import time
import math

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

input = []

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption(window_title)

keys = pygame.key.get_pressed()
clock = pygame.time.Clock()
ox_style = pygame.font.SysFont(style, size)
msg_style = pygame.font.SysFont(style, 40)


def squares():
    screen.fill(white)
    padding = width // rows
    for i in range(rows):
        x = i * padding
        if x > 0:
            pygame.draw.line(screen, black, (0, x), (width, x))
            pygame.draw.line(screen, black, (x, 0), (x, height))
    pygame.display.update()


def init_grid():
    array_squares = [[None for _ in range(columns)] for _ in range(rows)]
    dis_to_cen = width // rows // 2
    for row in range(rows):
        for col in range(len(array_squares[row])):
            x = dis_to_cen * (2 * col + 1)
            y = dis_to_cen * (2 * row + 1)
            array_squares[row][col] = (x, y, "", True)
    return array_squares


def click_square(squares):
    global x_turn, o_turn
    # mouse_position
    m_x, m_y = pygame.mouse.get_pos()
    for row in range(rows):
        for col in range(len(squares[row])):
            x, y, sign, can_play = squares[row][col]
            dis_mouse_cen = math.sqrt((x-m_x) ** 2 + (y-m_y) ** 2)
            if dis_mouse_cen < width // rows // 2 and can_play == True:
                if x_turn:
                    input.append((x, y, "x"))
                    squares[row][col] = (x, y, "x", False)
                    x_turn = False
                    o_turn = True
                elif o_turn:
                    input.append((x, y, "o"))
                    squares[row][col] = (x, y, "o", False)
                    o_turn = False
                    x_turn = True


def ox_show(val, x, y):
    value = ox_style.render(val, True, black)
    screen.blit(value, (x - size // 3, y - size))


# vertical
def v_check_won(squares):
    for col in range(len(squares[0])):
        for row in range(len(squares)):
            try:
                if squares[row][col][2] == "x" and squares[row+1][col][2] == "x" and squares[row+2][col][2] == "x" and squares[row+3][col][2] == "x" and squares[row+4][col][2] == "x":
                    return True
                elif squares[row][col][2] == "o" and squares[row+1][col][2] == "o" and squares[row+2][col][2] == "o" and squares[row+3][col][2] == "o" and squares[row+4][col][2] == "o":
                    return True
            except Exception as e:
                pass
    return False


# horizontal
def h_check_won(squares):
    for row in range(len(squares)):
        for col in range(len(squares[0])):
            try:
                if squares[row][col][2] == "x" and squares[row][col+1][2] == "x" and squares[row][col+2][2] == "x" and squares[row][col+3][2] == "x" and squares[row][col+4][2] == "x":
                    return True
                elif squares[row][col][2] == "o" and squares[row][col+1][2] == "o" and squares[row][col+2][2] == "o" and squares[row][col+3][2] == "o" and squares[row][col+4][2] == "o":
                    return True
            except Exception as e:
                pass
    return False


# diagonal
def d_check_won(squares):
    for row in range(len(squares)):
        for col in range(len(squares[0])):
            try:
                # /
                if squares[row][col][2] == "x" and squares[row+1][col+1][2] == "x" and squares[row+2][col+2][2] == "x" and squares[row+3][col+3][2] == "x" and squares[row+4][col+4][2] == "x":
                    return True
                elif squares[row][col][2] == "o" and squares[row+1][col+1][2] == "o" and squares[row+2][col+2][2] == "o" and squares[row+3][col+3][2] == "o" and squares[row+4][col+4][2] == "o":
                    return True
                # \
                elif squares[row][col+4][2] == "x" and squares[row+1][col+3][2] == "x" and squares[row+2][col+2][2] == "x" and squares[row+3][col+1][2] == "x" and squares[row+4][col][2] == "x":
                    return True
                elif squares[row][col+4][2] == "o" and squares[row+1][col+3][2] == "o" and squares[row+2][col+2][2] == "o" and squares[row+3][col+1][2] == "o" and squares[row+4][col][2] == "o":
                    return True
            except Exception as e:
                pass
    return False


def check_draw(squares):
    for row in range(len(squares)):
        for col in range(len(squares[0])):
            if squares[row][col][2] == "":
                return False
    return True


def check_losed():
    pass


def display_message(message):
    screen.fill(black)
    message = msg_style.render(message, 1, white)
    screen.blit(message, ((width - message.get_width()) //
                          2, (height - message.get_height()) // 2))

    pygame.display.update()


def game_loop():
    game_over = False
    game_close = False
    matrix_squares = init_grid()
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
                click_square(matrix_squares)

        # print(matrix_squares)
        squares()

        for i in input:
            x, y, val = i
            ox_show(val, x, y)
        if v_check_won(matrix_squares) or h_check_won(matrix_squares) or d_check_won(matrix_squares):
            display_message("WON!")
        if check_draw(matrix_squares):
            display_message("Draw")
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


game_loop()
