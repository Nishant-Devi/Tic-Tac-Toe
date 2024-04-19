import sys
import pygame
import numpy as np

pygame.init()

# colors
WHITE = (255, 255, 255) # DEFAULT COLOR
GRAY = (180, 180, 180) # Tie color
RED = (255, 0, 0)  # Loose color
GREEN = (0, 255, 0) # Win color
BLACK = (0, 0, 0) # Background

# Proportions and Sizes
WIDTH = 300 # width of the window
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 300 pixels * 300 pixels screen
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK) # we have an empty black screen now

board = np.zeros((BOARD_ROWS, BOARD_COLS)) # we define a board. Zero basically means that this field has no player on it


def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, start_pos=(0, SQUARE_SIZE*i), end_pos=(WIDTH, SQUARE_SIZE*i),width=LINE_WIDTH)
        pygame.draw.line(screen, color, start_pos=(SQUARE_SIZE*i,0), end_pos=(SQUARE_SIZE*i, HEIGHT), width=LINE_WIDTH)

def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, center=(int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), radius=CIRCLE_RADIUS, width=CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, start_pos=(col * SQUARE_SIZE + SQUARE_SIZE//4, row * SQUARE_SIZE + SQUARE_SIZE //4), end_pos=(col * SQUARE_SIZE + 3 * SQUARE_SIZE //4, row * SQUARE_SIZE + 3 * SQUARE_SIZE//4), width=CROSS_WIDTH)
                pygame.draw.line(screen, color, start_pos=(col * SQUARE_SIZE + SQUARE_SIZE//4, row * SQUARE_SIZE + 3 * SQUARE_SIZE //4), end_pos=(col * SQUARE_SIZE + 3 * SQUARE_SIZE //4, row * SQUARE_SIZE + SQUARE_SIZE//4), width=CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
        
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

# Every state of the board can be assigned a value or a score. How good is this position for the AI
def minimax(minimax_board, depth, is_maximizing):
    # if a move gets the AI to win
    if check_win(2, minimax_board):
        return float('inf')
    # if a move gets the AI to loose
    elif check_win(1, minimax_board):
        return float('-inf')
    # if a move results in the board being full without anyone winning
    elif is_board_full(minimax_board):
        return 0
    
    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] =2
                    score = minimax(minimax_board, depth+1, is_maximizing=False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else: 
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth+1, is_maximizing=True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# best move function which uses the minimax function to actually decide what the best move is
def best_move():
    best_score = -1000
    move = (-1,-1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] ==0:
                board[row][col] =2
                score = minimax(board, depth=0, is_maximizing=False)
                board[row][col] =0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1,-1):
        mark_square(move[0], move[1], player=2)
        return True
    return False


def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] =0
    

draw_lines()

player =1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # print("mouse clicked")
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE
           # print("Mouse clicked at:", mouseX, mouseY)

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over=True
                        player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over =True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player =1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)

    pygame.display.update()
          