import pygame
import random
from pygame import *
import os

fps = 15
width = 500
height = 500
snake_size = 10
food_size = 10
x, y, size = int(width/2 - snake_size), int(height/2 - snake_size), snake_size
food_x = round(random.randrange(food_size, width - food_size) / 10.0) * 10
food_y = round(random.randrange(food_size, height - food_size) / 10.0) * 10
x2, y2 = 0, 0
black = [0, 0, 0]
white = [255, 255, 255]
green = [34, 177, 76]
yellow = [255, 201, 14]
list_block_snake = []
lenght_of_snake = 1

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


def snake():
    global x, y

    if x < 0:
        x = width
    elif x > width:
        x = 0
    elif y < 0:
        y = height
    elif y > height:
        y = 0
    block = [x, y]
    list_block_snake.append(block)
    if len(list_block_snake) > lenght_of_snake:
        del list_block_snake[0]
    for i in list_block_snake:
        pygame.draw.rect(screen, green, [i[0], i[1], size, size])


def food():
    global food_x, food_y, lenght_of_snake
    if x == food_x and y == food_y:
        food_x = round(random.randrange(
            food_size, width - food_size) / 10.0) * 10
        food_y = round(random.randrange(
            food_size, height - food_size) / 10.0) * 10
        lenght_of_snake += 1
    pygame.draw.rect(screen, yellow, [food_x, food_y, food_size, food_size])
    print(lenght_of_snake)


def render():
    snake()
    food()


def game_loop():
    global x, y, x2, y2
    game_close = False
    game_over = False
    while not game_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_close = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y2 = -size
            x2 = 0
        elif keys[pygame.K_DOWN]:
            y2 = size
            x2 = 0
        elif keys[pygame.K_LEFT]:
            x2 = -size
            y2 = 0
        elif keys[pygame.K_RIGHT]:
            x2 = size
            y2 = 0
        y = y + y2
        x = x + x2
        screen.fill(white)
        render()
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


if __name__ == "__main__":
    game_loop()
