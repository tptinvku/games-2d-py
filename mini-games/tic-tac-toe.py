import pygame
import math

font_size = 30
width, height, rows, fps = 300, 300, 3, 30
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-tac-toe")
black = [0, 0, 0]
white = [255, 255, 255]
keys = pygame.key.get_pressed()
x_turn = True
o_turn = False
clock = pygame.time.Clock()
input = []
ox_style = pygame.font.SysFont("comicsansms", font_size)
msg_style = pygame.font.SysFont('courier', 40)


def squares():
    padding = width // rows
    for i in range(rows):
        x = i * padding
        if x > 0:
            pygame.draw.line(screen, white, (0, x), (width, x))
            pygame.draw.line(screen, white, (x, 0), (x, height))


def initialize_grid():
    dis_to_cen = width // rows // 2
    game_array = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    for row in range(rows):
        for column in range(len(game_array[row])):
            x = dis_to_cen * (2 * column + 1)
            y = dis_to_cen * (2 * row + 1)
            game_array[row][column] = (x, y, "", True)
    return game_array


def click_square(game_array):
    global x_turn, o_turn
    # mouse position
    m_x, m_y = pygame.mouse.get_pos()
    for row in range(rows):
        for column in range(len(game_array[row])):
            x, y, sign, can_play = game_array[row][column]
            dis_mouse_cen = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
            if dis_mouse_cen < width // rows // 2 and can_play == True:
                if x_turn:
                    input.append((x, y, "X"))
                    game_array[row][column] = (x, y, "x", False)
                    x_turn = False
                    o_turn = True
                elif o_turn:
                    input.append((x, y, "O"))
                    game_array[row][column] = (x, y, "o", False)
                    x_turn = True
                    o_turn = False


def ox_show(val, x, y):
    value = ox_style.render(val, True, white)
    screen.blit(value, (x - font_size//2, y - font_size // 2))


def check_won(game_array):
    for i in range(rows):
        # rows
        row = game_array[i]
        if (row[0][2] == row[1][2] == row[2][2]) and row[0][2]:
            return True
        # colums
        if (game_array[0][i][2] == game_array[1][i][2] == game_array[2][i][2]) and game_array[0][i][2]:
            return True
        if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2]:
            return True
        if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2]:
            return True

    return False


def check_draw(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    screen.fill(white)
    end_text = msg_style.render(content, 1, black)
    screen.blit(end_text, ((width - end_text.get_width()) //
                           2, (width - end_text.get_height()) // 2))
    pygame.display.update()


def game_loop():
    game_over = False
    game_close = False
    game_array = initialize_grid()

    while not game_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_square(game_array)
        print(game_array)
        squares()
        for i in input:
            x, y, val = i
            ox_show(val, x, y)
        if check_won(game_array):
            display_message(f"Won!")
        if check_draw(game_array):
            display_message("Draw!")
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


game_loop()
