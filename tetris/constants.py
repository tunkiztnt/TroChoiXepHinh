"""
Game constants and configuration.
"""

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 620
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Grid position offset
GRID_X_OFFSET = 10
GRID_Y_OFFSET = 10

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino colors
PIECE_COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# Tetromino shapes (I, J, L, O, S, T, Z)
SHAPES = [
    # I
    [[1, 1, 1, 1]],
    # J
    [[1, 0, 0],
     [1, 1, 1]],
    # L
    [[0, 0, 1],
     [1, 1, 1]],
    # O
    [[1, 1],
     [1, 1]],
    # S
    [[0, 1, 1],
     [1, 1, 0]],
    # T
    [[0, 1, 0],
     [1, 1, 1]],
    # Z
    [[1, 1, 0],
     [0, 1, 1]],
]

# Game speed (milliseconds per drop)
INITIAL_SPEED = 500
SPEED_INCREMENT = 25
MIN_SPEED = 100

# Scoring
SCORE_SINGLE = 100
SCORE_DOUBLE = 300
SCORE_TRIPLE = 500
SCORE_TETRIS = 800
SCORE_SOFT_DROP = 1
SCORE_HARD_DROP = 2

# Lines per level
LINES_PER_LEVEL = 10

# FPS
FPS = 60

# Font sizes
FONT_SMALL = 18
FONT_MEDIUM = 24
FONT_LARGE = 36
FONT_XLARGE = 48

# Panel position (right side info panel)
PANEL_X = GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE + 20
PANEL_Y = GRID_Y_OFFSET
