
import pygame
import time
import random
pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
apple_thickness = 10

font_style = pygame.font.SysFont("comicsansms", 25)
class Snake:
    def __init__(self):
        self.length = 1
        self.body = [[100, 50]]
    def move(self):
        if len(self.body) > 1:
            for i in range(len(self.body)-2, 0, -1):
                self.body[i] = self.body[i-1]
        self.body[0][0] += 10
    def add_block(self):
        self.body.append([self.body[-1][0], self.body[-1][1]])
class Apple:
    def __init__(self):
        self.x = round(random.randrange(0, dis_width - apple_thickness) / 10.0)*10
        self.y = round(random.randrange(0, dis_height - apple_thickness) / 10.0)*10

def plot_snake(some_snake, color):
    for pos in some_snake.body:
        pygame.draw.rect(dis, color, [pos[0], pos[1], snake_block, snake_block])
def plot_apple():
    pygame.draw.rect(dis, yellow, [apple.x, apple.y, apple_thickness, apple_thickness])

snake = Snake()
apple = Apple()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    snake.move()

    head = []
    for pos in snake.body:
        if pos[0] == snake_block * 5 and pos[1] == snake_block * 10:
            head = [pos]
            break
    else:
        head.append([snake_block * 5, snake_block * 10])

    if head[0][0] > dis_width or head[0][0] < 0.0 or head[0][1] > dis_height or head[0][1] < 0.0:
        done = True
    for pos in head:
        if pos in list(map(lambda x: x, snake.body[:-1])):
            done = True

    dis.fill(black)
    plot_snake(snake, white)
    plot_apple()

    pygame.display.update()
    clock.tick(10)
