import pygame, sys, random, threading, math, os
from PIL import Image
import numpy as np
from collections import Counter
from typing import Callable, Iterable
from pygame.locals import *

class Color:
    WHITE = (255, 255, 255)
    GRAY = (192, 192, 192)
    DARK_GREY = (128, 128, 128)
    VERY_DARK_GRAY = (64, 64, 64)
    RED = (255, 0, 0)
    DARK_RED = (128, 0, 0)
    VERY_DARK_RED = (64, 0, 0)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (128, 128, 0)
    VERY_DARK_YELLOW = (64, 64, 0)
    ORANGE = (255, 165)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 128, 0)
    VERY_DARK_GREEN = (0, 64, 0)
    CYAN = (0, 255, 255)
    DARK_CYAN = (0, 128, 128)
    VERY_DARK_CYAN = (0, 64, 64)
    BLUE = (0, 0, 255)
    DARK_BLUE = (0, 0, 128)
    VERY_DARK_BLUE = (0, 0, 64)
    MAGENTA = (255, 0, 255)
    DARK_MAGENTA = (128, 0, 128)
    VERY_DARK_MAGENTA = (64, 0, 64)
    BLACK = (0, 0, 0)
    BLANK = (0, 0, 0, 0)

    def fromHex(hex: "RRGGBB(AA)"):
        pass
        

class Sprite:
    def __init__(self, width, height):
        self.surf = pygame.Surface((width, height))

    def setPixel(self, pos, color):
        self.surf.fill(color, (pos, (1, 1)))

