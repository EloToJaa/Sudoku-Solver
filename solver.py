from random import sample as random
from copy import deepcopy


class SudokuSolver:
    SIZE = 9

    def __init__(self):
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.solve_moves = []
        self.remove_vals = []

    def is_valid(self):
        for x in range(0, self.SIZE, 3):
            for y in range(0, self.SIZE, 3):
                unique = []
                for row in self.board[x:x+3]:
                    for num in row[y:y+3]:
                        unique.append(num)
                unique = list(dict.fromkeys(unique))
                if len(unique) != 9 or 0 in unique:
                    return False

        for i in range(self.SIZE):
            unique = []
            for j in range(self.SIZE):
                unique.append(self.board[i][j])
            unique = list(dict.fromkeys(unique))
            if len(unique) != 9 or 0 in unique:
                return False

        for i in range(self.SIZE):
            unique = []
            for j in range(self.SIZE):
                unique.append(self.board[j][i])
            unique = list(dict.fromkeys(unique))
            if len(unique) != 9 or 0 in unique:
                return False

        return True

    def add_num(self, num, pos):
        y, x = pos
        prev_num = self.board[y][x]
        self.board[y][x] = num
        self.solve_moves.append((y, x, num))

        nums = [self.board[y][i] for i in range(self.SIZE)]
        nums.remove(num)
        if num in nums:
            self.board[y][x] = prev_num
            return False

        nums = [self.board[i][x] for i in range(self.SIZE)]
        nums.remove(num)
        if num in nums:
            self.board[y][x] = prev_num
            return False

        bx = x // 3 * 3
        by = y // 3 * 3
        nums = []
        for row in self.board[by:by+3]:
            for val in row[bx:bx+3]:
                nums.append(val)
        nums.remove(num)
        if num in nums:
            self.board[y][x] = prev_num
            return False

        return True

    def find_next(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] == 0:
                    return (i, j)

    def solve(self):
        pos = self.find_next()
        if pos:
            y, x = pos
        else:
            return True

        for num in range(1, 10):
            if self.add_num(num, pos):
                if self.solve():
                    return True
                self.board[y][x] = 0
                self.solve_moves.append((y, x, 0))

    def generate_board(self, blanks):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                self.board[i][j] = 0

        for i in range(0, self.SIZE, 3):
            nums = random(range(1, 10), 3)
            for j in range(3):
                self.board[i+j][i+j] = nums[j]

        self.solve()
        # self.print_board()

        positions = random(range(81), blanks)
        for pos in positions:
            y, x = pos // 9, pos % 9
            self.board[y][x] = 0

        self.solve_moves = []
        prev_board = deepcopy(self.board)
        self.solve()
        self.board = deepcopy(prev_board)
        if len(self.solve_moves) < 1000 or len(self.solve_moves) > 3000:
            self.generate_board(blanks)

    def print_board(self):
        for i in range(self.SIZE):
            if i % 3 == 0:
                print('-' * 25)
            for j in range(self.SIZE):
                if j % 3 == 0:
                    print('|', end=' ')
                print(self.board[i][j], end=' ')
                if j == self.SIZE - 1:
                    print('|', end=' ')
            print()
            if i == self.SIZE - 1:
                print('-' * 25)

    def count_blanks(self):
        blanks = 0
        for col in self.board:
            for num in col:
                if num == 0:
                    blanks += 1
        return blanks
