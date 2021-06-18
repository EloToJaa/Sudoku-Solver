import pygame
from solver import SudokuSolver
from GUI import Scoreboard, SudokuBoard
from constants import WHITE, BLACK, FPS, MAX_STRIKES, WIDTH, HEIGHT, ADD_WIDTH, ASCII_0, SIZE


def draw(win, board, scoreboard):
    win.fill(WHITE)
    board.draw(win)
    scoreboard.draw(win)
    pygame.display.update()


def lose_draw(win):
    # pygame.time.delay(5000)
    win.fill(WHITE)
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render('PRZEGRANA', 1, BLACK)
    x_gap, y_gap = 225, 40
    win.blit(text, (x_gap, HEIGHT / 2 - y_gap))
    text = font.render('RESTARTUJE GRE', 1, BLACK)
    x_gap, y_gap = 175, 40
    win.blit(text, (x_gap, HEIGHT / 2 + y_gap))
    pygame.display.update()
    pygame.time.delay(5000)


def win_draw(win):
    pygame.time.delay(5000)
    win.fill(WHITE)
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render('WYGRANA', 1, BLACK)
    x_gap, y_gap = 240, 40
    win.blit(text, (x_gap, HEIGHT / 2 - y_gap))
    text = font.render('RESTARTUJE GRE', 1, BLACK)
    x_gap, y_gap = 175, 40
    win.blit(text, (x_gap, HEIGHT / 2 + y_gap))
    pygame.display.update()
    pygame.time.delay(5000)


def start_game(solver, board, scoreboard, blanks=51):
    solver.generate_board(blanks)
    #print(f'Moves: {len(solver.solve_moves)}')
    board.save_board(solver.board)
    scoreboard.set_default()


def confirm_move(board, solver, scoreboard, moves, win, pos):
    y, x = pos
    temp = board.board[y][x].temp
    num = board.board[y][x].num
    if num == 0:
        if solver.add_num(temp, pos):
            board.board[y][x].num = temp
            moves.append(pos)
            board.board[y][x].success = True
        else:
            solver.board[y][x] = 0
            scoreboard.add_strike()
            if scoreboard.strikes >= MAX_STRIKES:
                lose_draw(win)
                start_game(solver, board, scoreboard)
        board.board[y][x].temp = 0


def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sudoku')
    pygame.font.init()
    solver = SudokuSolver()
    board = SudokuBoard(WIDTH - ADD_WIDTH, solver.board)
    scoreboard = Scoreboard(WIDTH - ADD_WIDTH, WIDTH, HEIGHT -
                            (WIDTH - ADD_WIDTH))
    start_game(solver, board, scoreboard)
    key = None
    run = True
    clock = pygame.time.Clock()
    moves = []
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    key = event.key - ASCII_0
                    # print(f'Pressed num: {key}')
                    y, x = board.selected
                    if board.board[y][x].num == 0:
                        board.board[y][x].temp = key

                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_BACKSPACE:
                    if len(moves) > 0:
                        y, x = moves[-1]
                        del moves[-1]
                        board.board[y][x].num = 0
                        board.board[y][x].success = False
                        solver.board[y][x] = 0

                if event.key == pygame.K_RETURN:
                    for y in range(SIZE):
                        for x in range(SIZE):
                            if board.board[y][x].temp != 0:
                                confirm_move(
                                    board, solver, scoreboard, moves, win, (y, x))

                if event.key == pygame.K_s:
                    for y, x, num in solver.solve_moves:
                        board.board[y][x].num = num
                        board.select((y, x))
                        if num == 0:
                            board.board[y][x].success = False
                        else:
                            board.board[y][x].success = True
                        draw(win, board, scoreboard)
                    win_draw(win)
                    start_game(solver, board, scoreboard)

                if event.key == pygame.K_SPACE:
                    for y, x, num in solver.solve_moves:
                        board.board[y][x].num = num
                    draw(win, board, scoreboard)
                    win_draw(win)
                    start_game(solver, board, scoreboard)

                if event.key == pygame.K_r:
                    start_game(solver, board, scoreboard)

                if event.key == pygame.K_UP:
                    y, x = board.selected
                    if y - 1 >= 0:
                        board.select((y - 1, x))

                if event.key == pygame.K_DOWN:
                    y, x = board.selected
                    if y + 1 < SIZE:
                        board.select((y + 1, x))

                if event.key == pygame.K_LEFT:
                    y, x = board.selected
                    if x - 1 >= 0:
                        board.select((y, x - 1))

                if event.key == pygame.K_RIGHT:
                    y, x = board.selected
                    if x + 1 < SIZE:
                        board.select((y, x + 1))

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                change_key = board.click(pos)
                if change_key:
                    key = None

        if solver.count_blanks() == 0 and solver.is_valid():
            win_draw(win)
            start_game(solver, board, scoreboard)

        draw(win, board, scoreboard)


if __name__ == '__main__':
    main()
