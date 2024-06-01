
import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

class Snake:
    def __init__(self):
        self.body = [(200, 250), (190, 250), (180, 250)]
        self.direction = (-10, 0)

    def move(self):
        head = [x + self.direction[0] for x in self.body[-1]]
        if head not in self.body[:-1]:
            self.body.append(head)
        else:
            return False
        return True

    def grow(self):
        head = [x + self.direction[0] for x in self.body[-1]]
        self.body.append(head)

class Apple:
    def __init__(self):
        self.position = (random.randint(0, 78) * 10, random.randint(0, 58) * 10)

    def display(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.position[0], self.position[1], 10, 10))

def game_loop(snake, apple):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != (0, -10):
                    snake.direction = (-10, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (0, 10):
                    snake.direction = (0, 10)
                elif event.key == pygame.K_UP and snake.direction != (10, 0):
                    snake.direction = (-10, 0)
                elif event.key == pygame.K_DOWN and snake.direction != (-10, 0):
                    snake.direction = (0, -10)

        if not snake.move():
            game_over()

        screen.fill((0, 0, 0))
        for position in snake.body:
            pygame.draw.rect(screen, (0, 255, 0), (position[0], position[1], 10, 10))

        apple.display()

        pygame.display.update()
        pygame.time.Clock().tick(10)

def game_over():
    print("Game Over!")
    pygame.quit()
    sys.exit()

snake = Snake()
apple = Apple()

game_loop(snake, apple)
