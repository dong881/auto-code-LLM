
import os
import random
import time

class Snake:
    def __init__(self):
        self.board = [[' ' for _ in range(20)] for _ in range(20)]
        self.snake_positions = [(10, 10), (9, 10), (8, 10)]
        self.direction = 'right'
        self.score = 0
        self.food_position = None

    def draw_board(self):
        os.system('clear')
        for i in range(20):
            for j in range(20):
                if (i, j) in self.snake_positions:
                    print('S', end=' ')
                elif (i, j) == self.food_position:
                    print('F', end=' ')
                else:
                    print(self.board[i][j], end=' ')
            print()

    def move_snake(self):
        head = self.snake_positions[0]
        if self.direction == 'right':
            new_head = (head[0], head[1] + 1)
        elif self.direction == 'left':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'up':
            new_head = (head[0] - 1, head[1])
        elif self.direction == 'down':
            new_head = (head[0] + 1, head[1])

        if new_head in self.snake_positions or new_head[0] < 0 or new_head[0] >= 20 or new_head[1] < 0 or new_head[1] >= 20:
            return False

        self.snake_positions.insert(0, new_head)
        if new_head == self.food_position:
            self.score += 1
            self.food_position = None
        else:
            self.snake_positions.pop()

    def run_game(self):
        while True:
            self.draw_board()
            user_input = input('Press Enter to move the snake... (type quit to quit) ')
            if user_input.lower() == 'quit':
                break

            if random.random() < 0.2:
                self.direction = random.choice(['right', 'left', 'up', 'down'])

            if not self.move_snake():
                print('Game Over! Your score is:', self.score)
                return

        self.draw_board()

if __name__ == '__main__':
    game = Snake()
    while True:
        game.run_game()
