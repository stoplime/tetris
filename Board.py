import pygame
from pygame.locals import *
import sys
import numpy as np
from constants import *
from random import randint

from GamePiece import *

class Board:
    def __init__(self, player, screen, offset, width, height, board_width, board_height):
        self.player = player
        self.screen = screen
        self.offset = offset
        self.board_width = board_width
        self.board_height = board_height
        self.grid = np.zeros((board_width, board_height))
        self.grid = np.pad(self.grid, pad_width=1, mode='constant', constant_values=8)
        self.grid = np.pad(self.grid, pad_width=2, mode='constant', constant_values=10)
        self.score = 0
        self.level = 1
        self.hold_piece = GamePiece(randint(0,6), self.board_width, self.board_height, self.grid, hold_piece=True)
        self.active_piece = GamePiece(randint(0,6), self.board_width, self.board_height, self.grid)
        self.next_piece = GamePiece(randint(0,6), self.board_width, self.board_height, self.grid, next_piece=True)
        self.colors = [BLACK, CYAN, ORANGE, BLUE, RED, GREEN, YELLOW, MAGENTA, GREY, WHITE, BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK]
        self.pixels = PIXELS
        self.clock = pygame.time.Clock()
        self.running = True
        self.active_piece.move_right()
        self.last_down = pygame.time.get_ticks()
        self.since_down = pygame.time.get_ticks()
        self.last_movement = pygame.time.get_ticks()
        self.since_movement = pygame.time.get_ticks()
        self.textfont = pygame.font.SysFont("monospace", 25)
        self.overfont = pygame.font.SysFont("monospace", 40)
        self.game_over = False
        self.can_hold = True

    def pause(self):
        self.running = not self.running

    def key_handler(self, key):
        if self.player == 1:
            if key == K_DOWN:
                if not self.active_piece.move_down():
                    self.integrate()
            elif key == K_LEFT:
                if not self.active_piece.move_left():
                    self.integrate()
            elif key == K_RIGHT:
                if not self.active_piece.move_right():
                    self.integrate()
            elif key == K_UP:
                if not self.active_piece.rotate_left():
                    self.integrate()
            elif key == K_a:
                if not self.active_piece.rotate_left():
                    self.integrate()
            elif key == K_s:
                if not self.active_piece.rotate_right():
                    self.integrate()
            elif key == K_SPACE:
                if not self.active_piece.drop():
                    self.integrate()
            elif key == K_c:
                self.swap_hold()
            elif key == K_p:
                self.pause()
            elif key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif self.player == 2:
            if key == K_DOWN:
                if not self.active_piece.move_down():
                    self.integrate()
            elif key == K_LEFT:
                if not self.active_piece.move_left():
                    self.integrate()
            elif key == K_RIGHT:
                if not self.active_piece.move_right():
                    self.integrate()
            elif key == K_UP:
                if not self.active_piece.rotate_left():
                    self.integrate()
            elif key == K_a:
                if not self.active_piece.rotate_left():
                    self.integrate()
            elif key == K_s:
                if not self.active_piece.rotate_right():
                    self.integrate()
            elif key == K_SPACE:
                if not self.active_piece.drop():
                    self.integrate()
            elif key == K_c:
                self.swap_hold()
            elif key == K_p:
                self.pause()
            elif key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_game()

            if not self.game_over:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        self.key_handler(event.key)
                        self.since_movement = pygame.time.get_ticks() - self.last_movement
                        self.last_movement = pygame.time.get_ticks()

                self.check_game()

                if self.running:
                    self.screen.fill(BLACK)

                    self.since_movement = pygame.time.get_ticks() - self.last_movement
                    self.since_down = pygame.time.get_ticks() - self.last_down

                    if self.since_down > 1000/(self.level):
                        if not self.active_piece.move_down():
                            self.integrate()
                            self.last_movement = pygame.time.get_ticks()
                            self.since_movement = 0
                        else:
                            self.last_down = pygame.time.get_ticks()
                            self.since_down = 0
                            self.check_lines()

                self.draw()
                pygame.display.update()
                self.clock.tick(60)

            else:
                self.draw()
                game_over_title = self.overfont.render("Game Over", 2, RED)
                self.screen.blit(game_over_title, (130, 300))
                pygame.display.update()
                self.clock.tick(60)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def check_game(self):
        if self.game_over:
            self.game_over = True

    def integrate(self):
        # Slice in current rotation/position tetramino into the grid (including border) while keeping the rest the same
        self.grid += self.active_piece.overlay
        self.check_lines()
        if self.active_piece.y_pos == 3:
            self.game_over = True
        self.spawn()

    def check_lines(self):
        line_totals = np.sum(self.grid > 0, axis=0)
        counter = 0
        for idx, i in enumerate(line_totals.tolist()[3:-3]):
            if i == self.board_width+6:
                self.grid[3:-3, idx+3] = 9
                self.grid[3:-3, 4:idx+4] = self.grid[3:-3, 3:idx+3]
                self.grid[3:-3, 3] = 0
                counter += 1

        if counter == 1:
            self.score += 100
        elif counter == 2:
            self.score += 250
        elif counter == 3:
            self.score += 500
        elif counter == 4:
            self.score += 1000

        self.level = (1000 + self.score) // 1000

    def spawn(self):
        rand_type = randint(0,6)
        self.can_hold = True
        self.active_piece.reset_active(self.next_piece.piece_type, self.grid) # Copy Next attributes into Active
        self.next_piece.reset_next(rand_type) # Change Next piece to random Tetramino
        self.active_piece.move_right()


    def reset_next(self, piece_type):
        self.piece_type = piece_type
        self.piece_grid = np.asarray(Tetraminos[piece_type])

    def reset_active(self, piece_type, grid):
        self.piece_type = piece_type
        self.piece_grid = np.asarray(Tetraminos[piece_type])
        self.x_pos = ((self.board_width + 6) // 2) - 1
        self.y_pos = 3
        self.grid = grid
        self.overlay = np.zeros(grid.shape)

    def swap_hold(self):
        if self.can_hold:
            hold = self.hold_piece.piece_type
            self.hold_piece.reset_next(self.active_piece.piece_type)
            self.active_piece.reset_active(hold, self.grid)
            self.can_hold = False

    def draw(self):
        self.brd = (self.grid + self.active_piece.overlay)

        # Draw Board Section
        for i in range(self.board_width+6):
            for j in range(self.board_height+6):
                pygame.draw.rect(self.screen, self.colors[int(self.brd[i,j])], (i*self.pixels, j*self.pixels, self.pixels, self.pixels), 5)
                pygame.draw.rect(self.screen, self.colors[int(self.brd[i, j])+11],(i * self.pixels, j * self.pixels, self.pixels, self.pixels), 1)

        # Draw NEXT/HOLD
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.screen, self.colors[int(self.next_piece.piece_grid[1, i, j])], ((i+16) * self.pixels, (j+3) * self.pixels, self.pixels, self.pixels), 5)
                pygame.draw.rect(self.screen, self.colors[int(self.next_piece.piece_grid[1, i, j])+11], ((i+16) * self.pixels, (j+3) * self.pixels, self.pixels, self.pixels), 1)
                pygame.draw.rect(self.screen, self.colors[int(self.hold_piece.piece_grid[1, i, j])], ((i + 16) * self.pixels, (j + 10) * self.pixels, self.pixels, self.pixels), 5)
                pygame.draw.rect(self.screen, self.colors[int(self.hold_piece.piece_grid[1, i, j])+11], ((i + 16) * self.pixels, (j + 10) * self.pixels, self.pixels, self.pixels), 1)

        # Draw Text Section
        next_title = self.textfont.render("Next", 2, BLUE)
        hold_title = self.textfont.render("Hold", 2, BLUE)
        score_title = self.textfont.render("Score", 2, BLUE)
        score_text = self.textfont.render(str(self.score), 2 , BLUE)
        level_title = self.textfont.render("Level", 2, BLUE)
        level_text = self.textfont.render(str(self.level), 2, BLUE)

        self.screen.blit(next_title, (16*PIXELS, 2*PIXELS))
        self.screen.blit(hold_title, (16*PIXELS, 9*PIXELS))
        self.screen.blit(score_title, (16*PIXELS, 16*PIXELS))
        self.screen.blit(score_text, (16*PIXELS, 17*PIXELS))
        self.screen.blit(level_title, (16 * PIXELS, 20 * PIXELS))
        self.screen.blit(level_text, (16 * PIXELS, 21 * PIXELS))