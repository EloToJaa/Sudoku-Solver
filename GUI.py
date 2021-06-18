import pygame
import time
from constants import BLACK, GREY, GREEN, BLUE, RED


class SudokuBoard:
    CUBES = 9

    def save_board(self, board):
        self.board = [[Cube(board[i][j], (i, j), self.cube_size)
                       for j in range(self.CUBES)] for i in range(self.CUBES)]
        self.select((0, 0))

    def __init__(self, draw_size, board):
        self.draw_size = draw_size
        self.cube_size = draw_size // 9
        self.selected = (0, 0)
        self.save_board(board)

    def draw(self, win):
        # rysuj linie
        for i in range(self.CUBES + 1):
            if i % 3 == 0:
                bold = 4
            else:
                bold = 1
            # linia pozioma
            pygame.draw.line(win, BLACK, (0, i * self.cube_size),
                             (self.draw_size, i * self.cube_size), bold)
            # linia pionowa
            pygame.draw.line(win, BLACK, (i * self.cube_size, 0),
                             (i * self.cube_size, self.draw_size), bold)

        # rysuj pola
        for row in self.board:
            for cube in row:
                cube.draw(win)

    def click(self, pos):
        click_x, click_y = pos

        if click_x <= self.draw_size and click_y <= self.draw_size:
            x = click_x // self.cube_size
            y = click_y // self.cube_size

            self.select((y, x))
            return True

        return False

    def select(self, pos):
        y, x = self.selected
        self.board[y][x].selected = False
        y, x = pos
        self.board[y][x].selected = True
        self.selected = (y, x)
        # print(f'Selected {self.selected}, num: {self.board[y][x].num}')

    def clear(self):
        for y in range(self.CUBES):
            for x in range(self.CUBES):
                if self.board[y][x].temp != 0 and self.board[y][x].num == 0:
                    self.board[y][x].temp = 0


class Cube:

    def __init__(self, num, pos, draw_size):
        self.num = num
        self.temp = 0
        self.y, self.x = pos
        self.draw_size = draw_size
        self.selected = False
        self.success = False

    def draw(self, win):
        font = pygame.font.SysFont('comicsans', 50)
        # odleglosc czcionki od brzegow
        x_gap, y_gap = 30, 25

        if self.num != 0:
            # pole niepuste
            text = font.render(str(self.num), 1, BLACK)
            win.blit(text, (self.x * self.draw_size +
                            x_gap, self.y * self.draw_size + y_gap))

        if self.temp != 0:
            text = font.render(str(self.temp), 1, GREY)
            win.blit(text, (self.x * self.draw_size +
                            x_gap, self.y * self.draw_size + y_gap))

        if self.success:
            #pygame.draw.rect( win, GREEN, (self.x * self.draw_size, self.y * self.draw_size, self.draw_size, self.draw_size), 3)
            x_gap, y_gap = 55, 18
            pygame.draw.line(win, GREEN, (self.x * self.draw_size + x_gap, (self.y + 1) * self.draw_size - y_gap),
                             ((self.x + 1) * self.draw_size - x_gap, (self.y + 1) * self.draw_size - y_gap), 5)

        if self.selected:
            pygame.draw.rect(
                win, BLUE, (self.x * self.draw_size, self.y * self.draw_size, self.draw_size, self.draw_size), 5)


class Scoreboard:

    def set_default(self):
        self.start = time.time()
        self.strikes = 0

    def __init__(self, draw_height, draw_width, draw_size):
        self.set_default()
        self.timer = None
        self.draw_height = draw_height
        self.draw_width = draw_width
        self.draw_size = draw_size

    def update_time(self):
        self.timer = round(time.time() - self.start)

    def draw_strikes(self, win, font):
        text = font.render('X ' * self.strikes, 1, RED)
        x_gap, y_gap = 10, 25
        win.blit(text, (x_gap, self.draw_height + y_gap))

    def format_time(self):
        secs = self.timer
        mins = str(secs // 60)
        secs = str(secs % 60)
        if len(secs) < 2:
            secs = f'0{secs}'
        return f'{mins}:{secs}'

    def draw_timer(self, win, font):
        text = font.render(self.format_time(), 1, BLACK)
        x_gap, y_gap = 120, 25
        win.blit(text, (self.draw_width - x_gap, self.draw_height + y_gap))

    def draw(self, win):
        font = pygame.font.SysFont('comicsans', 60)
        self.update_time()
        self.draw_strikes(win, font)
        self.draw_timer(win, font)

    def add_strike(self):
        self.strikes += 1
