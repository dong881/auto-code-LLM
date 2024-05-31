
import pygame
import time
import random
pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
red = (0, 0, 0)

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
appleThickness = 10
snake_speed = 10

font_style = pygame.font.SysFont("comicsansms", 25)
def Your_score(score):
    return font_style.render("Your Score: " + str(score), True, yellow)

def our_snake(snake_list):
    for x,n in enumerate(snake_list):
        pygame.draw.rect(dis, black, [x*snake_block, n*snake_block, snake_block, snake_block])
    pygame.display.update()

def message_to_screen(msg, color):
    screen_text = font_style.render(msg,True,color)
    dis.blit(screen_text,(dis_width/6,dis_height/3))
    pygame.display.update()

def gameLoop():
    game_over = False
    game_close = False

    snake_list = []
    length_of_snake = 1

    x1 = dis_width/2
    y1 = dis_height/2

    x1_change = 0
    y1_change = 0

    apple_x = round(random.randrange(0,dis_width - snake_block) / 10.0)*10.0
    apple_y = round(random.randrange(0,dis_height - snake_block) / 10.0)*10.0

    while not game_over:

        while game_close:
            dis.fill(black)
            message_to_screen("You Lost! Press C to play again or Q to quit.", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            message_to_screen("Game Over", red)
            game_close = True
        x1 += x1_change
        y1 += y1_change

        dis.fill(black)

        pygame.draw.rect(dis, red, [apple_x, apple_y, appleThickness, appleThickness])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for eachSegment in snake_list[:-1]:
            if eachSegment == snake_head:
                message_to_screen("You Lose! You hit yourself!", red)
                game_close = True

        our_snake(snake_list)

        pygame.display.update()

        if x1 == apple_x and y1 == apple_y:
            message_to_screen("Snake Ate Apple!", yellow)
            length_of_snake += 1
        clock.tick(snake_speed)

    pygame.quit()
