# tetromino.py
import pygame
import config

L_SHAPE = [
    [1, 0, 0, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

O_SHAPE = [
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

I_SHAPE = [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

S_SHAPE = [
    [0, 1, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

Z_SHAPE = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

T_SHAPE = [
    [0, 1, 0, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]


class Tetromino:
    def __init__(self, x, y, shape, image, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.image = image
        self.color = color
        #self.bottom_offset = self._calc_bottom_offset()   # ⬅︎ hier merken

    '''
    def _calc_bottom_offset(self):
        empty = 0
        for row in reversed(self.shape):
            if any(row):
                break
            empty += 1        # 0, 1 oder 2 leere Zeilen
        return empty
    '''
    def draw(self, surface):
        px = self.x * config.BLOCK_SIZE
        py = self.y * config.BLOCK_SIZE
        surface.blit(self.image, (px, py))
