"""
Game board logic.
"""
from tetris.constants import GRID_WIDTH, GRID_HEIGHT


class Board:
    """Represents the Tetris game board (grid)."""

    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def is_valid_position(self, piece):
        """Check if a piece is in a valid position on the board."""
        for x, y in piece.get_cells():
            if x < 0 or x >= GRID_WIDTH:
                return False
            if y >= GRID_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True

    def lock_piece(self, piece):
        """Lock a piece into the board grid."""
        for x, y in piece.get_cells():
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                self.grid[y][x] = piece.color

    def clear_lines(self):
        """Clear completed lines and return the number of lines cleared."""
        lines_cleared = 0
        new_grid = []

        for row in self.grid:
            if all(cell is not None for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)

        # Add empty rows at the top
        while len(new_grid) < GRID_HEIGHT:
            new_grid.insert(0, [None for _ in range(GRID_WIDTH)])

        self.grid = new_grid
        return lines_cleared

    def is_game_over(self, piece):
        """Check if placing a new piece results in game over."""
        return not self.is_valid_position(piece)

    def get_ghost_position(self, piece):
        """Get the ghost (shadow) position of a piece (where it would land)."""
        ghost = piece.clone()
        while self.is_valid_position(ghost):
            ghost.y += 1
        ghost.y -= 1
        return ghost

    def reset(self):
        """Reset the board to empty state."""
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
