import random
import time
import os

class SnakeGame:
    def __init__(self):
        self.board = [[' ' for _ in range(20)] for _ in range(15)]
        self.snake = [(5, 5), (6, 5), (7, 5)]
        self.food = None
        self.direction = (-1, 0)

    def print_board(self):
        os.system('clear')
        for row in self.board:
            print(' '.join(row))
        print(f"Score: {len(self.snake) - 3}")

    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= len(self.board) or head[1] < 0 or head[1] >= len(self.board[0]):
            return True
        for part in self.snake[1:]:
            if head == part:
                return True
        if self.food and self.food == head:
            return False
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if (i, j) in self.snake[1:] and (i, j) == head:
                    return True
        return False

    def move_snake(self):
        new_head = ((self.snake[0][0] + self.direction[0]), (self.snake[0][1] + self.direction[1]))
        if not self.check_collision():
            self.snake.insert(0, new_head)
            if self.food and self.food == new_head:
                self.food = None
            else:
                self.snake.pop()
        else:
            print("Game Over!")
            exit()

    def generate_food(self):
        while True:
            x = random.randint(0, len(self.board) - 1)
            y = random.randint(0, len(self.board[0]) - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def play_game(self):
        self.generate_food()
        while True:
            self.print_board()
            new_head = ((self.snake[0][0] + (-1, 0)[self.snake[0][1] % 2 == 0]), (self.snake[0][1] + 1))
            if not self.check_collision():
                self.snake.insert(0, new_head)
                if self.food and self.food == new_head:
                    self.food = None
                else:
                    self.snake.pop()
            else:
                print("Game Over!")
                exit()
            time.sleep(0.5)

game = SnakeGame()
game.play_game()
