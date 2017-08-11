import pygame
from pygame.locals import *
import sys
import numpy as np
from constants import *
from random import randint

from GamePiece import *
from Board import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
p1 = Board(1, screen, 0, HEIGHT, WIDTH, BOARD_X, BOARD_Y)
p2 = Board(2, screen, OFFSET, HEIGHT, WIDTH, BOARD_X, BOARD_Y)
p1.run()
p2.run()