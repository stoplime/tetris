import pygame
from pygame.locals import *
import sys
import numpy as np
import json
import os

class keyAugment:
    def __init__(self):
        self.KEY_HISTORY = []
        self.PATH = os.getcwd()
        self.BASE_EVENT = None
        self.ONCE = False

    def intercept_keys(self):
        events = []
        for event in pygame.event.get():
            events.append(event)
            if event.type == KEYDOWN:
                if not self.ONCE:
                    self.ONCE = True
                    self.BASE_EVENT = event
                self.KEY_HISTORY.append([pygame.time.get_ticks(), event.key])
        if self.ONCE:
            # Intercept events
            self.BASE_EVENT.key = K_SPACE
            # events.append(self.BASE_EVENT)
        return events

    def save_keys(self):
        print(self.KEY_HISTORY)
        with open(os.path.join(self.PATH, "saved_keys", "key_history.json"), 'w') as f:
            json.dump(self.KEY_HISTORY, f)