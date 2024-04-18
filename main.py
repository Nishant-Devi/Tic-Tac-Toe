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
        pygame.draw.line(screen, color, start_pos=(0, SQUARE_SIZE*i), end_pos=(WIDTH, SQUARE_SIZE*i), width=LINE_WIDTH)
        pygame.draw.line(screen, color, start_pos=(SQUARE_SIZE*i,0), end_pos=(SQUARE_SIZE*i, HEIGHT), width=LINE_WIDTH)

def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, center=(int(col*SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE //2)), radius=CIRCLE_RADIUS, width=CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, start_pos=(col * SQUARE_SIZE + SQUARE_SIZE//4, row * SQUARE_SIZE + SQUARE_SIZE //4), end_pos=(col * SQUARE_SIZE + 3 * SQUARE_SIZE //4, row * SQUARE_SIZE + 3 * SQUARE_SIZE//4))
                pygame.draw.line(screen, color, start_pos=(col * SQUARE_SIZE + SQUARE_SIZE//4, row * SQUARE_SIZE + 3 * SQUARE_SIZE //4), end_pos=(col * SQUARE_SIZE + 3 * SQUARE_SIZE //4, row * SQUARE_SIZE + SQUARE_SIZE//4))

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col]

def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return True
    return False

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















