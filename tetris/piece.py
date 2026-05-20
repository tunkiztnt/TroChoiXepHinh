"""
Tetromino piece logic.
"""
import random
from tetris.constants import SHAPES, PIECE_COLORS, GRID_WIDTH


class Piece:
    """Represents a Tetris piece (tetromino)."""

    def __init__(self, shape_index=None):
        if shape_index is None:
            shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape_index = shape_index
        self.shape = [row[:] for row in SHAPES[shape_index]]
        self.color = PIECE_COLORS[shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation = 0

    def rotate_clockwise(self):
        """Rotate the piece 90 degrees clockwise."""
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[self.shape[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]
        self.shape = rotated
        self.rotation = (self.rotation + 1) % 4

    def rotate_counterclockwise(self):
        """Rotate the piece 90 degrees counter-clockwise."""
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[self.shape[j][cols - 1 - i] for j in range(rows)] for i in range(cols)]
        self.shape = rotated
        self.rotation = (self.rotation - 1) % 4

    def get_cells(self):
        """Get all occupied cell positions of this piece."""
        cells = []
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    cells.append((self.x + col_idx, self.y + row_idx))
        return cells

    def clone(self):
        """Create a copy of this piece."""
        new_piece = Piece(self.shape_index)
        new_piece.shape = [row[:] for row in self.shape]
        new_piece.x = self.x
        new_piece.y = self.y
        new_piece.rotation = self.rotation
        return new_piece
