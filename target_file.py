
import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
score_font = pygame.font.Font(None, 50)

snake_color = (0,255,0)
apple_color = (255,0,0)

class Snake:
    def __init__(self):
        self.position = [(100,100)]
        self.direction = 'right'
        self.length = len(self.position)

    def move_snake(self):
        if self.direction == 'up':
            new_position = (self.position[-1][0], self.position[-1][1] - 10)
        elif self.direction == 'down':
            new_position = (self.position[-1][0], self.position[-1][1] + 10)
        elif self.direction == 'left':
            new_position = (self.position[-1][0] - 10, self.position[-1][1])
        else:
            new_position = (self.position[-1][0] + 10, self.position[-1][1])

        if new_position in self.position[:-1]:
            game_over()
        else:
            self.position.append(new_position)

    def eat_apple(self):
        self.length += 1

snake = Snake()

apple_position = [random.randint(0, screen_width), random.randint(0, screen_height)]

def initialize_game():
    pygame.init()
    pygame.display.set_caption("Snake Game")

def create_snake():
    global snake
    snake = Snake()

def generate_apple():
    global apple_position
    apple_position = [random.randint(0, screen_width), random.randint(0, screen_height)]

def handle_input(event):
    if event.key == pygame.K_UP and snake.direction != 'down':
        snake.direction = 'up'
    elif event.key == pygame.K_DOWN and snake.direction != 'up':
        snake.direction = 'down'
    elif event.key == pygame.K_LEFT and snake.direction != 'right':
        snake.direction = 'left'
    elif event.key == pygame.K_RIGHT and snake.direction != 'left':
        snake.direction = 'right'

def update_score():
    score_font.render(f"Score: {snake.length}", True, (0,0,0))

def check_collisions():
    if snake.position[-1] in apple_position:
        generate_apple()
        snake.eat_apple()

    for position in snake.position[:-1]:
        if position == snake.position[-1]:
            game_over()

    if snake.position[-1][0] < 0 or snake.position[-1][0] >= screen_width or \
       snake.position[-1][1] < 0 or snake.position[-1][1] >= screen_height:
        game_over()

def game_over():
    pygame.quit()
    sys.exit()

initialize_game()

create_snake()

generate_apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            handle_input(event)

    screen.fill((255,255,255))

    for position in snake.position:
        pygame.draw.rect(screen, snake_color, (position[0], position[1], 10, 10))

    apple_rect = pygame.Rect(*apple_position, 10, 10)
    pygame.draw.rect(screen, apple_color, apple_rect)

    update_score()

    check_collisions()

    if snake.direction == 'up':
        snake.move_snake()
    elif snake.direction == 'down':
        snake.position.reverse()
        snake.move_snake()
        snake.position.reverse()
    elif snake.direction == 'left':
        for i in range(len(snake.position) - 1, -1, -1):
            snake.position[i] = (snake.position[i][0] - 10, snake.position[i][1])
    else:
        for i in range(len(snake.position) - 1, -1, -1):
            snake.position[i] = (snake.position[i][0] + 10, snake.position[i][1])

    pygame.display.flip()

    clock.tick(10)
