import pygame
import time
import random

pygame.init()

# Set up the display
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
display = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Game")

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the snake and food
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_position = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
food_spawn = True

# Set up the game variables
direction = 'RIGHT'
change_to = direction
score = 0

# Game over function
def game_over():
    font_style = pygame.font.SysFont(None, 50)
    message = font_style.render("Game Over!", True, red)
    display.blit(message, [width / 6, height / 3])
    pygame.display.flip()
    time.sleep(2)
    # Add some funny screen
    funny_message = font_style.render("You lost, but you're still awesome!", True, green)
    display.blit(funny_message, [width / 6, height / 2])
    pygame.display.flip()
    time.sleep(2)
    quit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'

    # Validate the direction
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'

    # Update the snake position
    step_size = 20
    if direction == 'RIGHT':
        snake_position[0] += step_size
    if direction == 'LEFT':
        snake_position[0] -= step_size
    if direction == 'UP':
        snake_position[1] -= step_size
    if direction == 'DOWN':
        snake_position[1] += step_size

    # Snake body mechanism
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawn new food
    if not food_spawn:
        food_position = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
    food_spawn = True

    # Draw the snake and food
    display.fill(black)
    for pos in snake_body:
        pygame.draw.rect(display, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(display, white, pygame.Rect(food_position[0], food_position[1], 10, 10))
    # Update the display
    pygame.display.update()
    clock.tick(15)

    # Game over conditions
    if snake_position[0] < 0 or snake_position[0] > width - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > height - 10:
        game_over()
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Update the display
    pygame.display.update()
    clock.tick(15)