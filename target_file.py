
import pygame
import random
import sys
import time

pygame.init()

# Setup game environment
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Define constants
snake_length = 50
snake_speed = 10
food_size = 20
delay = 0.1

class Snake:
    def __init__(self):
        self.position = [(400, 300), (380, 300)]
        self.direction = 'right'
        self.length = len(self.position)

    def move_snake(self):
        new_head = None
        if self.direction == 'right':
            new_head = ((self.position[-1][0] + snake_speed) % screen_width, 
                       self.position[-1][1])
        elif self.direction == 'left':
            new_head = ((self.position[-1][0] - snake_speed) % screen_width, 
                       self.position[-1][1])
        elif self.direction == 'up':
            new_head = (self.position[-1][0], (self.position[-1][1] - snake_speed) % screen_height)
        elif self.direction == 'down':
            new_head = (self.position[-1][0], (self.position[-1][1] + snake_speed) % screen_height)

        if new_head:
            self.position.append(new_head)

    def grow_snake(self):
        self.length += 1

    def check_collisions(self):
        head_position = self.position[0]
        for i in range(1, len(self.position)):
            if head_position == self.position[i]:
                return True
        if (head_position[0] < 0 or 
            head_position[0] >= screen_width or 
            head_position[1] < 0 or 
            head_position[1] >= screen_height):
            return True
        return False

    def reset_snake(self):
        self.position = [(400, 300), (380, 300)]
        self.direction = 'right'
        self.length = len(self.position)

class Food:
    def __init__(self):
        self.position = None

    def generate_food(self):
        while True:
            x = random.randint(0, screen_width - food_size)
            y = random.randint(0, screen_height - food_size)
            self.position = (x, y)
            if all(p != self.position for p in Snake().position):
                break

def main():
    snake = Snake()
    food = Food()
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            snake.direction = 'up'
        elif keys[pygame.K_DOWN]:
            snake.direction = 'down'
        elif keys[pygame.K_LEFT]:
            snake.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            snake.direction = 'right'

        snake.move_snake()

        if snake.position[0] == food.position:
            score += 1
            snake.grow_snake()
            food.generate_food()
        else:
            snake.position.pop()

        screen.fill((255, 255, 255))
        for pos in snake.position:
            pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], snake_length, snake_length))
        pygame.draw.rect(screen, (255, 0, 0), (food.position[0], food.position[1], food_size, food_size))

        if game_over:
            font = pygame.font.Font(None, 72)
            text = font.render('Game Over! Score: ' + str(score), True, (0, 0, 0))
            screen.blit(text, (screen_width / 2 - text.get_width() / 2, 
                                screen_height / 2 - text.get_height() / 2))
        else:
            pygame.display.update()
            time.sleep(delay)

        if snake.check_collisions():
            game_over = True

if __name__ == '__main__':
    main()
