
import pygame
import sys
import random
import time

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake Game')

class Snake:
    def __init__(self):
        self.body = [(width / 2, height / 2)]
        self.direction = 'right'

    def move(self):
        if self.direction == 'right':
            head = (self.body[-1][0] + 10, self.body[-1][1])
        elif self.direction == 'left':
            head = (self.body[-1][0] - 10, self.body[-1][1])
        elif self.direction == 'up':
            head = (self.body[-1][0], self.body[-1][1] - 10)
        elif self.direction == 'down':
            head = (self.body[-1][0], self.body[-1][1] + 10)

        if head in self.body[:-1]:
            return False

        self.body.append(head)
        return True

    def grow(self):
        self.body.append(self.body[-1])

class Food:
    def __init__(self):
        self.pos = (random.randint(0, width - 10), random.randint(0, height - 10))

def main():
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'down':
                    snake.direction = 'up'
                elif event.key == pygame.K_DOWN and snake.direction != 'up':
                    snake.direction = 'down'
                elif event.key == pygame.K_LEFT and snake.direction != 'right':
                    snake.direction = 'left'
                elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                    snake.direction = 'right'

        screen.fill(black)

        if not snake.move():
            game_over()
            return

        if snake.body[-1] == food.pos:
            snake.grow()
            food = Food()

        for pos in snake.body:
            pygame.draw.rect(screen, yellow, (pos[0], pos[1], 10, 10))

        pygame.draw.rect(screen, white, (food.pos[0], food.pos[1], 10, 10))
        pygame.display.update()
        clock.tick(60)

def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render('Game Over', True, white)
    screen.fill(black)
    screen.blit(text, [(width / 2) - (text.get_width() / 2), (height / 2) - (text.get_height() / 2)])
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
