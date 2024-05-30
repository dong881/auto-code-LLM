
import pygame
import random
import sys

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

snake = [(200, 100), (220, 100), (240, 100)]
direction = 'right'

food = None
score = 0

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

    if food is None:
        food = (random.randint(0, width-10), random.randint(0, height-10))

    head = snake[0]
    if direction == 'up':
        new_head = (head[0], head[1] - 10)
    elif direction == 'down':
        new_head = (head[0], head[1] + 10)
    elif direction == 'left':
        new_head = (head[0] - 10, head[1])
    elif direction == 'right':
        new_head = (head[0] + 10, head[1])

    snake.insert(0, new_head)

    if head == food:
        score += 1
        while True:
            food = (random.randint(0, width-10), random.randint(0, height-10))
            for part in snake:
                if food == part:
                    break
            else:
                break
    else:
        snake.pop()

    screen.fill(black)
    for point in snake:
        pygame.draw.rect(screen, white, pygame.Rect(point[0], point[1], 10, 10))
    pygame.draw.rect(screen, (255,165,0), pygame.Rect(food[0], food[1], 10, 10))

    pygame.display.flip()
