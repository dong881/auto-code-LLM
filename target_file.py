
import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600
snake_speed = 10

size = width, height = 640, 480
black = 0, 0, 0
white = 255, 255, 255
snake_color = 100, 50, 30
apple_color = 200, 100, 50

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

class Snake:
    def __init__(self):
        self.length = 1
        self.body = [[width/2, height/2]]
        self.direction = 'right'

    def move(self):
        if self.direction == 'right':
            new_head = [self.body[-1][0] + 10, self.body[-1][1]]
        elif self.direction == 'left':
            new_head = [self.body[-1][0] - 10, self.body[-1][1]]
        elif self.direction == 'up':
            new_head = [self.body[-1][0], self.body[-1][1] - 10]
        elif self.direction == 'down':
            new_head = [self.body[-1][0], self.body[-1][1] + 10]

        if new_head in self.body[:-1]:
            pygame.quit()
            sys.exit()

        self.body.append(new_head)

    def eat_apple(self, apple):
        if self.body[-1] == apple:
            return True
        else:
            return False

def generate_apple():
    return [random.randint(0, width-10), random.randint(0, height-10)]

def main_game_loop(snake, apple):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        if not snake.eat_apple(apple):
            apple = generate_apple()

        screen.fill(black)
        for part in snake.body:
            pygame.draw.rect(screen, snake_color, pygame.Rect(part[0], part[1], 10, 10))
        pygame.draw.rect(screen, apple_color, pygame.Rect(apple[0], apple[1], 10, 10))

        pygame.display.flip()

snake = Snake()
apple = generate_apple()

main_game_loop(snake, apple)
