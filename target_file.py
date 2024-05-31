
import pygame
import random
import sys

pygame.init()

size = width, height = 640, 480
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake Game')

snake = [(200, 200), (210, 200), (220, 200)]
apple = (400, 300)

speed = 10

score = 0
direction = 'right'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
            elif event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
            elif event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'

    head = snake[0]
    if direction == 'up':
        new_head = (head[0], head[1] - speed)
    elif direction == 'down':
        new_head = (head[0], head[1] + speed)
    elif direction == 'left':
        new_head = (head[0] - speed, head[1])
    elif direction == 'right':
        new_head = (head[0] + speed, head[1])

    snake.insert(0, new_head)

    if new_head == apple:
        score += 1
        snake.pop()
    else:
        snake.pop()

    screen.fill(black)
    for pos in snake:
        pygame.draw.rect(screen, white, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, (255, 165, 0), pygame.Rect(apple[0], apple[1], 10, 10))

    pygame.display.flip()
