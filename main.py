import pygame
from solver import SudokuSolver
from GUI import Scoreboard, SudokuBoard
from constants import WHITE, BLACK, FPS, MAX_STRIKES, WIDTH, HEIGHT, ADD_WIDTH, ASCII_0, NUM_0, SIZE


def draw(win, board, scoreboard):
    win.fill(WHITE)
    board.draw(win)
    scoreboard.draw(win)
    pygame.display.update()


def lose_draw(win):
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


def simulation(board, solver, sim_move):
    y, x, num = solver.solve_moves[sim_move]
    board.board[y][x].num = num
    board.select((y, x))
    if num == 0:
        board.board[y][x].success = False
    else:
        board.board[y][x].success = True


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
    sim = False
    sim_move = -1
    while run:
        clock.tick(FPS)

        if sim:
            sim_move += 1
            simulation(board, solver, sim_move)
            if sim_move == len(solver.solve_moves) - 1:
                sim = False
                sim_move = -1
                win_draw(win)
                start_game(solver, board, scoreboard)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    key = event.key - ASCII_0
                    y, x = board.selected
                    if board.board[y][x].num == 0:
                        board.board[y][x].temp = key

                if event.key >= pygame.K_KP1 and event.key <= pygame.K_KP9:
                    key = event.key - NUM_0
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

                if event.key == pygame.K_SPACE:
                    if not sim:
                        sim = True
                    elif sim:
                        sim = False
                        continue
                    sim_move += 1
                    simulation(board, solver, sim_move)
                    if sim_move == len(solver.solve_moves) - 1:
                        sim = False
                        sim_move = -1
                        win_draw(win)
                        start_game(solver, board, scoreboard)

                if event.key == pygame.K_e:
                    for y, x, num in solver.solve_moves:
                        board.board[y][x].num = num
                    draw(win, board, scoreboard)
                    sim = False
                    sim_move = -1
                    win_draw(win)
                    start_game(solver, board, scoreboard)

                if event.key == pygame.K_r:
                    sim = False
                    sim_move = -1
                    start_game(solver, board, scoreboard)

                if event.key in (pygame.K_UP, pygame.K_w):
                    y, x = board.selected
                    if y - 1 >= 0:
                        board.select((y - 1, x))

                if event.key in (pygame.K_DOWN, pygame.K_s):
                    y, x = board.selected
                    if y + 1 < SIZE:
                        board.select((y + 1, x))

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    y, x = board.selected
                    if x - 1 >= 0:
                        board.select((y, x - 1))

                if event.key in (pygame.K_RIGHT, pygame.K_d):
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
