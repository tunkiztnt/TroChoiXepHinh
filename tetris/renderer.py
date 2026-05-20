"""
Rendering module - handles all drawing operations.
"""
import pygame
from tetris.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE,
    GRID_X_OFFSET, GRID_Y_OFFSET, PANEL_X, PANEL_Y,
    BLACK, WHITE, GRAY, DARK_GRAY, RED, GREEN, CYAN,
    FONT_SMALL, FONT_MEDIUM, FONT_LARGE, FONT_XLARGE
)


class Renderer:
    """Handles all game rendering."""

    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_xlarge = pygame.font.Font(None, FONT_XLARGE)

    def draw_block(self, x, y, color, alpha=255):
        """Draw a single block at grid position."""
        px = GRID_X_OFFSET + x * BLOCK_SIZE
        py = GRID_Y_OFFSET + y * BLOCK_SIZE

        if alpha < 255:
            surface = pygame.Surface((BLOCK_SIZE - 1, BLOCK_SIZE - 1), pygame.SRCALPHA)
            surface.fill((*color, alpha))
            self.screen.blit(surface, (px, py))
        else:
            rect = pygame.Rect(px, py, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
            pygame.draw.rect(self.screen, color, rect)
            # Highlight effect
            highlight = tuple(min(c + 40, 255) for c in color)
            pygame.draw.line(self.screen, highlight, (px, py), (px + BLOCK_SIZE - 2, py))
            pygame.draw.line(self.screen, highlight, (px, py), (px, py + BLOCK_SIZE - 2))
            # Shadow effect
            shadow = tuple(max(c - 40, 0) for c in color)
            pygame.draw.line(self.screen, shadow,
                            (px + BLOCK_SIZE - 2, py),
                            (px + BLOCK_SIZE - 2, py + BLOCK_SIZE - 2))
            pygame.draw.line(self.screen, shadow,
                            (px, py + BLOCK_SIZE - 2),
                            (px + BLOCK_SIZE - 2, py + BLOCK_SIZE - 2))

    def draw_grid(self, board):
        """Draw the game grid and locked pieces."""
        # Draw background
        grid_rect = pygame.Rect(
            GRID_X_OFFSET, GRID_Y_OFFSET,
            GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE
        )
        pygame.draw.rect(self.screen, BLACK, grid_rect)

        # Draw grid lines
        for x in range(GRID_WIDTH + 1):
            px = GRID_X_OFFSET + x * BLOCK_SIZE
            pygame.draw.line(self.screen, DARK_GRAY,
                            (px, GRID_Y_OFFSET),
                            (px, GRID_Y_OFFSET + GRID_HEIGHT * BLOCK_SIZE))
        for y in range(GRID_HEIGHT + 1):
            py = GRID_Y_OFFSET + y * BLOCK_SIZE
            pygame.draw.line(self.screen, DARK_GRAY,
                            (GRID_X_OFFSET, py),
                            (GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE, py))

        # Draw locked pieces
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if board.grid[y][x] is not None:
                    self.draw_block(x, y, board.grid[y][x])

        # Draw border
        pygame.draw.rect(self.screen, WHITE, grid_rect, 2)

    def draw_piece(self, piece):
        """Draw the current falling piece."""
        if piece is None:
            return
        for x, y in piece.get_cells():
            if y >= 0:
                self.draw_block(x, y, piece.color)

    def draw_ghost(self, ghost_piece):
        """Draw the ghost piece (landing preview)."""
        if ghost_piece is None:
            return
        for x, y in ghost_piece.get_cells():
            if y >= 0:
                self.draw_block(x, y, ghost_piece.color, alpha=60)

    def draw_next_piece(self, piece):
        """Draw the next piece preview."""
        if piece is None:
            return

        label = self.font_medium.render("NEXT", True, WHITE)
        self.screen.blit(label, (PANEL_X, PANEL_Y))

        # Draw preview box
        preview_rect = pygame.Rect(PANEL_X, PANEL_Y + 25, 120, 80)
        pygame.draw.rect(self.screen, DARK_GRAY, preview_rect)
        pygame.draw.rect(self.screen, GRAY, preview_rect, 1)

        # Center the piece in preview
        piece_width = len(piece.shape[0]) * BLOCK_SIZE
        piece_height = len(piece.shape) * BLOCK_SIZE
        offset_x = PANEL_X + (120 - piece_width) // 2
        offset_y = PANEL_Y + 25 + (80 - piece_height) // 2

        for row_idx, row in enumerate(piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    px = offset_x + col_idx * BLOCK_SIZE
                    py = offset_y + row_idx * BLOCK_SIZE
                    rect = pygame.Rect(px, py, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
                    pygame.draw.rect(self.screen, piece.color, rect)

    def draw_info_panel(self, score, level, lines, high_score):
        """Draw the information panel (score, level, lines)."""
        y_offset = PANEL_Y + 120

        # Score
        score_label = self.font_medium.render("SCORE", True, WHITE)
        score_value = self.font_large.render(str(score), True, GREEN)
        self.screen.blit(score_label, (PANEL_X, y_offset))
        self.screen.blit(score_value, (PANEL_X, y_offset + 25))

        # High Score
        y_offset += 70
        hs_label = self.font_medium.render("HIGH SCORE", True, WHITE)
        hs_value = self.font_medium.render(str(high_score), True, CYAN)
        self.screen.blit(hs_label, (PANEL_X, y_offset))
        self.screen.blit(hs_value, (PANEL_X, y_offset + 25))

        # Level
        y_offset += 60
        level_label = self.font_medium.render("LEVEL", True, WHITE)
        level_value = self.font_large.render(str(level), True, GREEN)
        self.screen.blit(level_label, (PANEL_X, y_offset))
        self.screen.blit(level_value, (PANEL_X, y_offset + 25))

        # Lines
        y_offset += 70
        lines_label = self.font_medium.render("LINES", True, WHITE)
        lines_value = self.font_large.render(str(lines), True, GREEN)
        self.screen.blit(lines_label, (PANEL_X, y_offset))
        self.screen.blit(lines_value, (PANEL_X, y_offset + 25))

    def draw_controls(self):
        """Draw control hints at the bottom of the panel."""
        y_offset = PANEL_Y + 430
        controls = [
            "CONTROLS:",
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "Space : Hard Drop",
            "P : Pause",
            "M : Mute SFX",
            "N : Mute Music",
            "R : Restart",
            "ESC : Quit",
        ]
        for i, text in enumerate(controls):
            color = CYAN if i == 0 else GRAY
            label = self.font_small.render(text, True, color)
            self.screen.blit(label, (PANEL_X, y_offset + i * 19))

    def draw_game_over(self, score, high_score):
        """Draw game over overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        go_text = self.font_xlarge.render("GAME OVER", True, RED)
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(go_text, go_rect)

        # Score
        score_text = self.font_large.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        # High score
        if score >= high_score:
            hs_text = self.font_medium.render("NEW HIGH SCORE!", True, CYAN)
        else:
            hs_text = self.font_medium.render(f"High Score: {high_score}", True, GRAY)
        hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(hs_text, hs_rect)

        # Restart hint
        restart_text = self.font_medium.render("Press R to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)

    def draw_pause(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font_xlarge.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(pause_text, pause_rect)

        hint_text = self.font_medium.render("Press P to Resume", True, GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(hint_text, hint_rect)

    def draw_start_screen(self):
        """Draw the start/title screen."""
        self.screen.fill(BLACK)

        # Title
        title_text = self.font_xlarge.render("TETRIS", True, CYAN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)

        # Subtitle
        sub_text = self.font_medium.render("A Classic Puzzle Game", True, GRAY)
        sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, 170))
        self.screen.blit(sub_text, sub_rect)

        # Instructions
        instructions = [
            "HOW TO PLAY:",
            "",
            "Fill complete horizontal lines",
            "to clear them and earn points.",
            "",
            "The game ends when pieces",
            "stack to the top of the board.",
            "",
            "CONTROLS:",
            "Arrow Keys - Move & Rotate",
            "Space - Hard Drop",
            "P - Pause | M - Mute SFX",
            "N - Mute Music",
            "",
            "Press ENTER to Start",
        ]

        y_start = 220
        for i, line in enumerate(instructions):
            if i == 0 or i == 8:
                color = GREEN
            elif "Press ENTER" in line:
                color = CYAN
            else:
                color = WHITE
            text = self.font_small.render(line, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_start + i * 25))
            self.screen.blit(text, text_rect)

    def draw_win_screen(self, score, level):
        """Draw win/congratulations screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Congratulations
        win_text = self.font_xlarge.render("YOU WIN!", True, GREEN)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(win_text, win_rect)

        # Stats
        score_text = self.font_large.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)

        level_text = self.font_medium.render(f"Level Reached: {level}", True, CYAN)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(level_text, level_rect)

        congrats_text = self.font_medium.render("Congratulations!", True, CYAN)
        congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(congrats_text, congrats_rect)

        restart_text = self.font_medium.render("Press R to Play Again", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(restart_text, restart_rect)
