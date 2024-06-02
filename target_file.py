import pygame
import random
import time

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

block_size = 20
snake_speed = 10

clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.length = 1
        self.body = [(0, 0)]
        self.direction = 'right'

    def move(self):
        x, y = self.body[0]
        if self.direction == 'right':
            new_head = (x + block_size, y)
        elif self.direction == 'left':
            new_head = (x - block_size, y)
        elif self.direction == 'up':
            new_head = (x, y - block_size)
        elif self.direction == 'down':
            new_head = (x, y + block_size)

        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        x, y = self.body[0]
        if self.length < 10:
            self.length += 1
        else:
            self.body.pop()
        return

    def check_collision(self):
        for i in range(len(self.body) - 1):
            if self.body[i] == self.body[-1]:
                return True
        return False

    def reset(self):
        self.length = 1
        self.body = [(0, 0)]
        self.direction = 'right'
        return

def generate_food():
    x = random.randint(0, (display_width / block_size) - 1)
    y = random.randint(0, (display_height / block_size) - 1)
    return ((x * block_size), (y * block_size))

snake = Snake()
food = generate_food()

game_over = False
score = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.direction != 'right':
                snake.direction = 'left'
            elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                snake.direction = 'right'
            elif event.key == pygame.K_UP and snake.direction != 'down':
                snake.direction = 'up'
            elif event.key == pygame.K_DOWN and snake.direction != 'up':
                snake.direction = 'down'

    snake.move()

    if (snake.body[0][0] > display_width or snake.body[0][1] > display_height or
        snake.body[0][0] < 0 or snake.body[0][1] < 0):
        game_over = True

    for i in range(len(snake.body) - 1):
        if snake.body[i] == snake.body[-1]:
            game_over = True

    if snake.body[0] == food:
        snake.grow()
        score += 10
        food = generate_food()

    gameDisplay.fill(black)
    for x, y in snake.body:
        pygame.draw.rect(gameDisplay, white, (x, y, block_size, block_size))
    pygame.draw.rect(gameDisplay, white, (food[0], food[1], block_size, block_size))

    pygame.display.update()
    clock.tick(snake_speed)
    
pygame.quit()