import pygame
from pygame.locals import *
import sys
import numpy as np
import json
import os

class imageCapture:
    def __init__(self):
        self.images = []
        self.curentImage = None
        self.compressedImage = np.zeros((20, 30))

    def get_current_image(self):
        size = pygame.display.get_surface().get_size()
        self.curentImage = pygame.Surface(size)
        self.curentImage.blit(pygame.display.get_surface(), (0, 0), ((0, 0), size))
        pygame.image.save(img, "test.png")


