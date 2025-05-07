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
    def __init__(self, x, y, shape_matrix, image, color):
        self.x = x  # in Block-Einheiten
        self.y = y
        self.shape = shape_matrix  # bleibt für Kollision etc. erhalten
        self.image = image  # ganzes Sprite (128x128 px)
        self.color = color

    def draw(self, surface):
        px = self.x * config.BLOCK_SIZE
        py = self.y * config.BLOCK_SIZE
        surface.blit(self.image, (px, py))
