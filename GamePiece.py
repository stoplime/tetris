import pygame
from pygame.locals import *
import sys
import numpy as np
from constants import *
from random import randint

class GamePiece:
    def __init__(self, piece_type, board_width, board_height, grid, next_piece=False, hold_piece=False):
        self.piece_type = piece_type
        self.rotation_frame = 0
        self.piece_grid = np.asarray(Tetraminos[piece_type])
        self.board_width = board_width
        self.board_height = board_height
        self.grid = grid
        self.overlay = np.zeros(grid.shape)
        self.test_overlay = np.zeros(grid.shape)
        self.test2_overlay = np.zeros(grid.shape)
        self.speed = 1

        if next_piece:
            self.x_pos = self.board_width + 6 + 3
            self.y_pos = self.board_height + 3
        elif hold_piece:
            self.x_pos = self.board_width + 6 + 3
            self.y_pos = self.board_height + 3 + 5
        else:
            self.x_pos = ((self.board_width + 6) // 2) - 1
            self.y_pos = 3

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

    def move_down(self):
        if self._check_move(self.x_pos, self.y_pos+self.speed, self.rotation_frame):
            return True
        else:
            return False

    def move_left(self):
        if self._check_move(self.x_pos-self.speed, self.y_pos, self.rotation_frame):
            return True
        else:
            return False

    def move_right(self):
        if self._check_move(self.x_pos+self.speed, self.y_pos, self.rotation_frame):
            return True
        else:
            return False

    def rotate_left(self):
        if self.rotation_frame == 0:
            if self._check_move(self.x_pos, self.y_pos, 3):
                return True
            else:
                return False
        else:
            if self._check_move(self.x_pos, self.y_pos, (self.rotation_frame-1)%4):
                return True
            else:
                return False

    def rotate_right(self):
        if self._check_move(self.x_pos, self.y_pos, (self.rotation_frame+1)%4):
            return True
        else:
            return False

    def drop(self):
        while self._check_move(self.x_pos, self.y_pos+1, self.rotation_frame):
            pass
        return False

    def _check_move(self, x, y, frame):
        self.test_overlay = np.zeros((self.board_width + 6, self.board_height + 6)) # Blank grid
        self.test_overlay[x:x + 4, y:y + 4] += np.asarray(Tetraminos[self.piece_type][frame])  # Add tetris piece at new coords
        if np.sum(self.grid * self.test_overlay) > 0:
            if not self._can_drop():
                return False
            else:
                return True
        else:
            self.x_pos = x
            self.y_pos = y
            self.rotation_frame = frame
            self.overlay = self.test_overlay
            return True

    def _can_drop(self):
        self.test2_overlay = np.zeros((self.board_width + 6, self.board_height + 6)) # Blank grid
        self.test2_overlay[self.x_pos:self.x_pos+4, self.y_pos+1:self.y_pos+5] += np.asarray(Tetraminos[self.piece_type][self.rotation_frame]) # Add tetris piece at new coords
        if np.sum(self.grid * self.test2_overlay) > 0:
            return False
        else:
            return True