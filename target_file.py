import pygame
import random
import sys

# Set up the game environment
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Define constants
snake_size = 10
apple_size = 10
speed = 5

class Snake:
    def __init__(self):
        self.position = [(200, 200), (190, 200), (180, 200)]
        self.length = len(self.position)
        self.direction = 'Right'

    def move_snake(self):
        if self.direction == 'Right':
            new_head = ((self.position[0][0] + snake_size), self.position[0][1])
        elif self.direction == 'Left':
            new_head = (self.position[0][0] - snake_size, self.position[0][1])
        elif self.direction == 'Up':
            new_head = (self.position[0][0], self.position[0][1] - snake_size)
        elif self.direction == 'Down':
            new_head = (self.position[0][0], self.position[0][1] + snake_size)

        if new_head not in self.position:
            self.position.insert(0, new_head)
        else:
            self.length -= 1
            for i in range(len(self.position) - 1):
                self.position[i] = self.position[i + 1]

    def check_collision(self):
        head = self.position[0]
        if (head[0] < 0 or head[0] >= screen_width or
            head[1] < 0 or head[1] >= screen_height):
            return 'Collision with wall'
        for segment in range(1, len(self.position)):
            if head == self.position[segment]:
                return 'Self collision'

    def draw_snake(self):
        for position in self.position:
            pygame.draw.rect(screen, (0, 255, 0), (position[0], position[1], snake_size, snake_size))

class Apple:
    def __init__(self):
        self.position = (random.randint(0, screen_width - apple_size),
                          random.randint(0, screen_height - apple_size))

    def draw_apple(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.position[0], self.position[1], apple_size, apple_size))

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
                if event.key == pygame.K_LEFT and snake.direction != 'Right':
                    snake.direction = 'Left'
                elif event.key == pygame.K_RIGHT and snake.direction != 'Left':
                    snake.direction = 'Right'
                elif event.key == pygame.K_UP and snake.direction != 'Down':
                    snake.direction = 'Up'
                elif event.key == pygame.K_DOWN and snake.direction != 'Up':
                    snake.direction = 'Down'

        snake.move_snake()
        collision_result = snake.check_collision()

        if collision_result:
            print(collision_result)
            break

        screen.fill((0, 0, 0))
        snake.draw_snake()
        apple.draw_apple()

        pygame.display.flip()
        clock.tick(speed)

if __name__ == '__main__':
    main()