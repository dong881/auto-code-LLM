
import pygame
import sys
import random
import time

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)

dis_width = 800
dis_height = 600

snake_block_size = 20
apple_diameter = 10

snake_list = []
length = 1

score = 0

game_over = False

font_style = pygame.font.SysFont("bahnschrift", 25)
font_score = pygame.font.SysFont("bahnschrift", 30)

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

def snake(snake_list):
    for xny in snake_list:
        pygame.draw.rect(dis, black, [xny[0], xny[1], snake_block_size, snake_block_size])

def message_to_screen(text_color, text):
    screen_text = font_style.render(text, True, text_color)
    dis.blit(screen_text, [(dis_width//6), (dis_height//3)])

def score_message_to_screen(text_color, text):
    screen_text = font_score.render(text, True, text_color)
    dis.blit(screen_text, [0, 0])

snake_head = [400, 300]
apple_pos = [random.randrange(1, (dis_width-apple_diameter)//20)*20, random.randrange(1, (dis_height-apple_diameter)//15)*20]

def check_game_over(snake_list):
    for each_segment in snake_list[:-1]:
        if each_segment == snake_head:
            return True
    return False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and snake_head[1] != 0:
        snake_head[1] -= snake_block_size
    elif keys[pygame.K_DOWN] and snake_head[1] != dis_height-apple_diameter:
        snake_head[1] += snake_block_size
    elif keys[pygame.K_LEFT] and snake_head[0] != 0:
        snake_head[0] -= snake_block_size
    elif keys[pygame.K_RIGHT] and snake_head[0] != dis_width-apple_diameter:
        snake_head[0] += snake_block_size

    if len(snake_list) > length:
        del snake_list[0]

    for each_segment in snake_list[:-1]:
        if each_segment == snake_head:
            game_over = True
            break

    dis.fill(white)

    snake(snake_list)
    pygame.draw.rect(dis, red, [apple_pos[0], apple_pos[1], apple_diameter, apple_diameter])

    score_text = f"Score: {score}"
    score_message_to_screen(yellow, score_text)

    if snake_head[0] == apple_pos[0] and snake_head[1] == apple_pos[1]:
        score += 1
        length += 1
        apple_pos = [random.randrange(1, (dis_width-apple_diameter)//20)*20, random.randrange(1, (dis_height-apple_diameter)//15)*20]
    else:
        for each_segment in snake_list[:-1]:
            if each_segment == snake_head:
                game_over = True

    pygame.display.update()

    clock.tick(10)

if check_game_over(snake_list):
    message_to_screen(red, "Game Over! Press Enter to play again.")
    pygame.time.wait(2000)
