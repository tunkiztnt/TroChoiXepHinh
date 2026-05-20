"""
Main game logic module.
"""
import pygame
import os
import json
from tetris.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    INITIAL_SPEED, SPEED_INCREMENT, MIN_SPEED,
    SCORE_SINGLE, SCORE_DOUBLE, SCORE_TRIPLE, SCORE_TETRIS,
    SCORE_SOFT_DROP, SCORE_HARD_DROP,
    LINES_PER_LEVEL, BLACK
)
from tetris.board import Board
from tetris.piece import Piece
from tetris.renderer import Renderer
from tetris.sound_manager import SoundManager

# Win condition: reach this level
WIN_LEVEL = 15
HIGH_SCORE_FILE = "highscore.json"


class Game:
    """Main Tetris game class."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Xep Hinh")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.sound = SoundManager()
        self.high_score = self._load_high_score()
        self.state = "start"  # start, playing, paused, game_over, win
        self._reset_game()
        # Start music on the title screen
        self.sound.start_music()

    def _reset_game(self):
        """Reset game state for a new game."""
        self.board = Board()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.drop_speed = INITIAL_SPEED
        self.drop_timer = 0
        self.soft_dropping = False
        self.game_over = False
        self.won = False

    def _load_high_score(self):
        """Load high score from file."""
        try:
            if os.path.exists(HIGH_SCORE_FILE):
                with open(HIGH_SCORE_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except (json.JSONDecodeError, IOError):
            pass
        return 0

    def _save_high_score(self):
        """Save high score to file."""
        try:
            with open(HIGH_SCORE_FILE, "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except IOError:
            pass

    def _calculate_score(self, lines):
        """Calculate score based on lines cleared."""
        scores = {
            1: SCORE_SINGLE,
            2: SCORE_DOUBLE,
            3: SCORE_TRIPLE,
            4: SCORE_TETRIS,
        }
        return scores.get(lines, 0) * self.level

    def _update_level(self):
        """Update level based on lines cleared."""
        new_level = self.lines_cleared // LINES_PER_LEVEL + 1
        if new_level > self.level:
            self.level = new_level
            self.drop_speed = max(MIN_SPEED, INITIAL_SPEED - (self.level - 1) * SPEED_INCREMENT)
            self.sound.play("level_up")

            # Win condition
            if self.level >= WIN_LEVEL:
                self.state = "win"
                self.won = True
                self.sound.stop_music()
                self.sound.play("win")
                self._update_high_score()

    def _update_high_score(self):
        """Update high score if current score is higher."""
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()

    def _spawn_piece(self):
        """Spawn a new piece."""
        self.current_piece = self.next_piece
        self.next_piece = Piece()

        if self.board.is_game_over(self.current_piece):
            self.state = "game_over"
            self.game_over = True
            self.sound.stop_music()
            self.sound.play("game_over")
            self._update_high_score()

    def _move_piece(self, dx, dy):
        """Try to move the current piece."""
        self.current_piece.x += dx
        self.current_piece.y += dy

        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False

        if dx != 0:
            self.sound.play("move")
        return True

    def _rotate_piece(self):
        """Try to rotate the current piece with wall kick."""
        original_shape = [row[:] for row in self.current_piece.shape]
        original_x = self.current_piece.x

        self.current_piece.rotate_clockwise()

        # Wall kick attempts
        kicks = [0, -1, 1, -2, 2]
        for kick in kicks:
            self.current_piece.x = original_x + kick
            if self.board.is_valid_position(self.current_piece):
                self.sound.play("rotate")
                return True

        # Revert if no valid position found
        self.current_piece.shape = original_shape
        self.current_piece.x = original_x
        return False

    def _hard_drop(self):
        """Hard drop the current piece to the bottom."""
        drop_distance = 0
        while self.board.is_valid_position(self.current_piece):
            self.current_piece.y += 1
            drop_distance += 1
        self.current_piece.y -= 1
        drop_distance -= 1

        self.score += drop_distance * SCORE_HARD_DROP
        self.sound.play("hard_drop")
        self._lock_and_clear()

    def _lock_and_clear(self):
        """Lock piece and clear lines."""
        self.board.lock_piece(self.current_piece)
        lines = self.board.clear_lines()

        if lines > 0:
            self.lines_cleared += lines
            self.score += self._calculate_score(lines)

            if lines >= 4:
                self.sound.play("tetris")
            else:
                self.sound.play("line_clear")

            self._update_level()

        self._spawn_piece()

    def _handle_input(self, event):
        """Handle keyboard input."""
        if event.type == pygame.KEYDOWN:
            if self.state == "start":
                if event.key == pygame.K_RETURN:
                    self.state = "playing"
                    self._reset_game()
                    self.sound.start_music()
                elif event.key == pygame.K_n:
                    self.sound.toggle_music()
                elif event.key == pygame.K_m:
                    self.sound.toggle_sound()
                elif event.key == pygame.K_ESCAPE:
                    return False

            elif self.state == "playing":
                if event.key == pygame.K_LEFT:
                    self._move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self._move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.soft_dropping = True
                elif event.key == pygame.K_UP:
                    self._rotate_piece()
                elif event.key == pygame.K_SPACE:
                    self._hard_drop()
                elif event.key == pygame.K_p:
                    self.state = "paused"
                    self.sound.pause_music()
                    self.sound.play("pause")
                elif event.key == pygame.K_m:
                    self.sound.toggle_sound()
                elif event.key == pygame.K_n:
                    self.sound.toggle_music()
                elif event.key == pygame.K_r:
                    self._reset_game()
                    self.state = "playing"
                    self.sound.start_music()
                elif event.key == pygame.K_ESCAPE:
                    return False

            elif self.state == "paused":
                if event.key == pygame.K_p:
                    self.state = "playing"
                    self.sound.resume_music()
                    self.sound.play("pause")
                elif event.key == pygame.K_n:
                    self.sound.toggle_music()
                elif event.key == pygame.K_m:
                    self.sound.toggle_sound()
                elif event.key == pygame.K_ESCAPE:
                    return False

            elif self.state in ("game_over", "win"):
                if event.key == pygame.K_r:
                    self._reset_game()
                    self.state = "playing"
                    self.sound.start_music()
                elif event.key == pygame.K_n:
                    self.sound.toggle_music()
                elif event.key == pygame.K_m:
                    self.sound.toggle_sound()
                elif event.key == pygame.K_ESCAPE:
                    return False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.soft_dropping = False

        return True

    def _update(self, dt):
        """Update game state."""
        if self.state != "playing":
            return

        # Drop timer
        speed = self.drop_speed // 3 if self.soft_dropping else self.drop_speed
        self.drop_timer += dt

        if self.drop_timer >= speed:
            self.drop_timer = 0
            if not self._move_piece(0, 1):
                # Piece can't move down, lock it
                self._lock_and_clear()
            elif self.soft_dropping:
                self.score += SCORE_SOFT_DROP

    def _render(self):
        """Render the current frame."""
        self.screen.fill(BLACK)

        if self.state == "start":
            self.renderer.draw_start_screen()
        else:
            # Draw game elements
            self.renderer.draw_grid(self.board)

            if self.state == "playing":
                # Draw ghost piece
                ghost = self.board.get_ghost_position(self.current_piece)
                self.renderer.draw_ghost(ghost)
                # Draw current piece
                self.renderer.draw_piece(self.current_piece)

            elif self.state in ("game_over", "paused", "win"):
                # Still draw the last piece position
                self.renderer.draw_piece(self.current_piece)

            # Draw UI elements
            self.renderer.draw_next_piece(self.next_piece)
            self.renderer.draw_info_panel(
                self.score, self.level, self.lines_cleared, self.high_score
            )
            self.renderer.draw_controls()

            # Draw overlays
            if self.state == "game_over":
                self.renderer.draw_game_over(self.score, self.high_score)
            elif self.state == "paused":
                self.renderer.draw_pause()
            elif self.state == "win":
                self.renderer.draw_win_screen(self.score, self.level)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True

        while running:
            dt = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if not self._handle_input(event):
                        running = False

            self._update(dt)
            self._render()

        self._update_high_score()
        self.sound.cleanup()
        pygame.quit()
