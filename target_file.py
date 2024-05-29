
import pygame
import time
import random
import sys

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 0)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
appleThickness = 5

snake_list = []
length_of_snake = 1

apple_x = round((dis_width - appleThickness) / 10)
apple_y = round((dis_height - appleThickness) / 20)

direction = "right"
change_to = direction

def snake_body(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, yellow, [x[0], x[1], snake_block, snake_block])

def our_snake(apple_x, apple_y, snake_list):
    head = [0, 0]
    snake_list.append(head)

    direction_changer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_UP] and direction != "down"):
                change_to = "up"
            if (keys[pygame.K_DOWN] and direction != "up"):
                change_to = "down"
            if (keys[pygame.K_LEFT] and direction != "right"):
                change_to = "left"
            if (keys[pygame.K_RIGHT] and direction != "left"):
                change_to = "right"

        if direction == "up":
            new_head = [apple_x, apple_y - snake_block]
        if direction == "down":
            new_head = [apple_x, apple_y + snake_block]
        if direction == "left":
            new_head = [apple_x - snake_block, apple_y]
        if direction == "right":
            new_head = [apple_x + snake_block, apple_y]

        snake_list.append(new_head)

        if (new_head[0] >= dis_width or
                new_head[0] < 0 or
                new_head[1] >= dis_height or
                new_head[1] < 0):
            pygame.quit()
            quit()

        if new_head in snake_list[:-1]:
            pygame.quit()
            quit()

        dis.fill(white)

        snake_body(snake_list)
        pygame.draw.rect(dis, red, [apple_x, apple_y, appleThickness, appleThickness])

        list_of_snake = snake_list.copy()
        if (new_head[0] == apple_x and
                new_head[1] == apple_y):
            length_of_snake += 1

        else:
            for x in range(len(list_of_snake) - 1):
                if list_of_snake[x+1] != new_head:
                    del list_of_snake[-1]

        pygame.display.update()

        clock.tick(10)

        if (length_of_snake >= 5 or
                len(snake_list) > dis_width / snake_block * 2):
            up_score = 0

            while True:
                pygame.time.wait(2000)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                return

        time.sleep(0.1)

our_snake(apple_x, apple_y, snake_list)
