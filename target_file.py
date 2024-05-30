
import pygame
import random
import sys

pygame.init()

# Setup game environment
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Define constants
snake_length = 50
food_size = 20
delay = 0.1

class Snake:
    def __init__(self):
        self.position = [(400, 300)]
        self.direction = (10, 0)
        self.length = len(self.position)

    def move_snake(self):
        new_head = ((self.position[0][0] + self.direction[0]) % screen_width,
                    (self.position[0][1] + self.direction[1]) % screen_height)
        if new_head not in self.position:
            self.position.insert(0, new_head)
        else:
            self.length -= 1
            while len(self.position) > self.length:
                self.position.pop()

    def grow_snake(self):
        self.length += 1

    def check_collisions(self):
        if (self.position[0][0] < 0 or self.position[0][0] >= screen_width or
                self.position[0][1] < 0 or self.position[0][1] >= screen_height or
                self.position[0] in self.position[1:]):
            return True
        return False

class Food:
    def __init__(self):
        self.position = (random.randint(0, screen_width - food_size),
                         random.randint(0, screen_height - food_size))

    def generate_food(self, snake):
        if self.position not in snake.position:
            return self.position
        else:
            return self.generate_food(snake)

def main():
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        for pos in snake.position:
            pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], snake_length, snake_length))

        if snake.length > 10 and random.random() < 0.01:
            food.generate_food(snake)
        elif snake.position[0] == food.position:
            snake.grow_snake()
            food = Food()

        screen.fill((255, 255, 255), (food.position[0], food.position[1], food_size, food_size))
        pygame.draw.rect(screen, (255, 0, 0), (food.position[0], food.position[1], food_size, food_size))

        if snake.check_collisions():
            font = pygame.font.Font(None, 72)
            text = font.render('Game Over!', True, (0, 0, 0))
            screen.blit(text, (screen_width / 2 - text.get_width() / 2,
                                screen_height / 2 - text.get_height() / 2))
        else:
            pygame.display.update()
            time.sleep(delay)

        snake.move_snake()

if __name__ == '__main__':
    main()
