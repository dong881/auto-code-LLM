import pygame
import random

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
SNAKE_SIZE = 20
INITIAL_SPEED = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'

    def move(self):
        head = self.body[0]
        x, y = head
        if self.direction == 'UP':
            y -= GRID_SIZE
        elif self.direction == 'DOWN':
            y += GRID_SIZE
        elif self.direction == 'LEFT':
            x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            x += GRID_SIZE
        self.body.insert(0, (x, y))
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        x, y = tail
        if self.direction == 'UP':
            y += GRID_SIZE
        elif self.direction == 'DOWN':
            y -= GRID_SIZE
        elif self.direction == 'LEFT':
            x += GRID_SIZE
        elif self.direction == 'RIGHT':
            x -= GRID_SIZE
        self.body.append((x, y))

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*segment, SNAKE_SIZE, SNAKE_SIZE))

class Apple:
    def __init__(self):
        self.position = (random.randint(0, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (*self.position, SNAKE_SIZE, SNAKE_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            snake.direction = 'UP'
        elif keys[pygame.K_DOWN]:
            snake.direction = 'DOWN'
        elif keys[pygame.K_LEFT]:
            snake.direction = 'LEFT'
        elif keys[pygame.K_RIGHT]:
            snake.direction = 'RIGHT'

        snake.move()

        if snake.body[0] == apple.position:
            snake.grow()
            apple = Apple()

        screen.fill(WHITE)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(INITIAL_SPEED)

    pygame.quit()

if __name__ == "__main__":
    main()
