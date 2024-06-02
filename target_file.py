import pygame
import time
import random
pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

block_size = 20
font_style = pygame.font.SysFont("bahnschrift", 25)

def Your_snake_game():
    game_over = False
    snake_list = []
    length_of_snake = 1

    lead_x = display_width / 2
    lead_y = display_height / 2
    x_change = 0
    y_change = 20

    new_food = True
    foodx = round(display_width * random.random()) * block_size
    foody = round(display_height * random.random()) * block_size

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change != 20:
                    x_change = -20
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change != -20:
                    x_change = 20
                    y_change = 0
                elif event.key == pygame.K_UP and y_change != -20:
                    y_change = -20
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change != 20:
                    y_change = 20
                    x_change = 0

        if new_food is False:
            lead_x += x_change
            lead_y += y_change

            if lead_x < 0 or lead_x > display_width - block_size or lead_y < 0 or lead_y > display_height - block_size:
                game_over = True

            snake_head = []
            snake_head.append(lead_x)
            snake_head.append(lead_y)

            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for each_segment in snake_list[:-1]:
                if each_segment == list(snake_head):
                    game_over = True

        else:
            lead_x = foodx
            lead_y = foody

            new_food = False

        screen.fill(black)

        for x_n, y_n in snake_list:
            pygame.draw.rect(screen, white, [x_n, y_n, block_size, block_size])

        pygame.draw.rect(screen, red, [foodx, foody, block_size, block_size])

        font = font_style.render("Score: " + str(len(snake_list)), True, white)
        screen.blit(font, [0, 20])

        pygame.display.update()

        clock.tick(10)

        if lead_x == foodx and lead_y == foody:
            new_food = True
            length_of_snake += 1

    pygame.quit()
    quit()

screen = pygame.display.set_mode((display_width, display_height))
Your_snake_game()