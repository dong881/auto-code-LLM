
import pygame
import sys
import time
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

block_size = 20
font_size = 30

snake_list = []
apple_position = []

for i in range(display_height // block_size):
    snake_list.append([])
    for j in range(display_width // block_size):
        snake_list[i].append(0)

direction = "right"

def create_snake(snake_list, direction):
    snake_head_x = 0
    snake_head_y = 0

    if direction == "up":
        snake_head_x = display_height // block_size - 1
        snake_head_y = display_width // block_size // 2
    elif direction == "down":
        snake_head_x = 0
        snake_head_y = display_width // block_size // 2
    elif direction == "left":
        snake_head_x = display_height // block_size // 2
        snake_head_y = 0
    elif direction == "right":
        snake_head_x = display_height // block_size // 2
        snake_head_y = display_width // block_size - 1

    for i in range(display_height // block_size):
        for j in range(display_width // block_size):
            if (i == snake_head_x) and (j == snake_head_y):
                pygame.draw.rect(gameDisplay, yellow, [j * block_size, i * block_size, block_size, block_size])
    return snake_list

def move_snake(snake_list, direction):
    for i in range(display_height // block_size):
        for j in range(display_width // block_size):
            if (i == 0) and (j == display_width // block_size - 1):
                pygame.draw.rect(gameDisplay, black, [j * block_size, i * block_size, block_size, block_size])
    return snake_list

def generate_food(snake_list, apple_position):
    for i in range(display_height // block_size):
        for j in range(display_width // block_size):
            if (i != 0) and (j != display_width // block_size - 1):
                if random.randint(0, 10) < 2:
                    apple_x = i
                    apple_y = j
                    pygame.draw.rect(gameDisplay, black, [apple_y * block_size, apple_x * block_size, block_size, block_size])
                    return snake_list

def handle_input(direction):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] and direction != "down") or (keys[pygame.K_DOWN] and direction != "up"):
        direction = "up"
    elif (keys[pygame.K_LEFT] and direction != "right") or (keys[pygame.K_RIGHT] and direction != "left"):
        direction = "left"

    return direction

def update_score(snake_list, score):
    font = pygame.font.SysFont(None, font_size)
    text = font.render(f'Score: {score}', 1, black)
    gameDisplay.blit(text, (display_width // block_size - 20, display_height // block_size))

def check_collisions(snake_list):
    for i in range(display_height // block_size):
        for j in range(display_width // block_size):
            if ((i == 0) and (j == display_width // block_size - 1)) or ((i != 0) and (j != display_width // block_size - 1)):
                pygame.draw.rect(gameDisplay, black, [j * block_size, i * block_size, block_size, block_size])
    return snake_list

def game_over(snake_list):
    for i in range(display_height // block_size):
        for j in range(display_width // block_size):
            if (i != 0) and (j != display_width // block_size - 1):
                pygame.draw.rect(gameDisplay, black, [j * block_size, i * block_size, block_size, block_size])
    return snake_list

score = 0
direction = "right"

while True:
    gameDisplay.fill(white)
    create_snake(snake_list, direction)
    move_snake(snake_list, direction)
    generate_food(snake_list, apple_position)
    handle_input(direction)

    if (snake_list[display_height // block_size - 1][display_width // block_size // 2] == 1):
        score += 1
        update_score(snake_list, score)

    pygame.display.update()
    clock.tick(10)
