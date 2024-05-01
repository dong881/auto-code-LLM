
import random
import time
class SnakeGame:
    def __init__(self):
        self.grid_size=(20,20)
        self.snake=[(10,10),(9,10),(8,10)]
        self.food=None
        self.direction='down'
        self.score=0
    def generate_food(self):
        while True:
            x=random.randint(0,self.grid_size[0]-1)
            y=random.randint(0,self.grid_size[1]-1)
            if (x,y) not in self.snake and (x,y)!=(10,10):
                self.food=(x,y)
                break
    def move_snake(self):
        head=self.snake[0]
        if self.direction=='up':
            new_head=(head[0],head[1]-1)
        elif self.direction=='down':
            new_head=(head[0],head[1]+1)
        elif self.direction=='left':
            new_head=(head[0]-1,head[1])
        else:
            new_head=(head[0]+1,head[1])
        if new_head in self.snake or new_head[0]<0 or new_head[0]>=self.grid_size[0] or new_head[1]<0 or new_head[1]>=self.grid_size[1]:
            return False
        self.snake.insert(0,new_head)
        if self.food and self.food==new_head:
            del self.food
        else:
            self.snake.pop()
        return True
    def play_game(self):
        while True:
            for x in range(self.grid_size[0]):
                for y in range(self.grid_size[1]):
                    if (x,y) in self.snake:
                        print('*',end=' ')
                    elif (x,y)==self.food:
                        print('F',end=' ')
                    else:
                        print('~',end=' ')
                print()
            command=input("Enter a direction (up/down/left/right) or 'quit' to exit: ").lower()
            if command=='quit':
                break
            elif command in ['up','down','left','right']:
                self.direction=command
            else:
                continue
            while not self.move_snake():
                print("Game Over! Final score: ",self.score)
                return
game=SnakeGame()
while True:
    game.play_game()