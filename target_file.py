
import pygame
import random
import sys

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)

class Snake:
    def __init__(self):
        self.length = 5
        self.body = [[200, 200]]
        self.direction = "right"

    def move(self):
        if self.direction == "right":
            new_head = [self.body[0][0] + 20, self.body[0][1]]
        elif self.direction == "left":
            new_head = [self.body[0][0] - 20, self.body[0][1]]
        elif self.direction == "up":
            new_head = [self.body[0][0], self.body[0][1] - 20]
        elif self.direction == "down":
            new_head = [self.body[0][0], self.body[0][1] + 20]

        if new_head in self.body[:-1]:
            return False
        else:
            self.body.insert(0, new_head)
            return True

    def grow(self):
        self.length += 1
        self.body.append([self.body[-1][0], self.body[-1][1]])

    def display(self):
        for pos in self.body:
            pygame.draw.rect(screen, (255, 0, 0), (pos[0], pos[1], 20, 20))

class Apple:
    def __init__(self):
        self.position = [random.randint(0, 38) * 20, random.randint(0, 29) * 20]

    def display(self):
        pygame.draw.rect(screen, (255, 215, 0), (self.position[0], self.position[1], 20, 20))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "down":
                    snake.direction = "up"
                elif event.key == pygame.K_DOWN and snake.direction != "up":
                    snake.direction = "down"
                elif event.key == pygame.K_LEFT and snake.direction != "right":
                    snake.direction = "left"
                elif event.key == pygame.K_RIGHT and snake.direction != "left":
                    snake.direction = "right"

        if not snake.move():
            break

        screen.fill((0, 0, 0))
        apple.display()
        snake.display()

        pygame.draw.rect(screen, (0, 255, 0), (snake.body[0][0], snake.body[0][1], 20, 20))

        if [snake.body[0][0], snake.body[0][1]] == list(apple.position):
            apple = Apple()
            snake.grow()

        pygame.display.flip()
        clock.tick(10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (snake.body[0][0], snake.body[0][1], 20, 20))

        pygame.display.flip()
