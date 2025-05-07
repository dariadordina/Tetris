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

J_SHAPE = [
    [0, 0, 0, 0],
    [1, 1, 1, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 0],
]

def rotate_cw(matrix):
    return [list(row) for row in zip(*matrix[::-1])]

class Tetromino:
    def __init__(self, x, y, shape, image, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.image = image
        self.color = color

    def rotate(self, grid):
        """Versucht die Figur zu drehen. Wenn nicht möglich, bleibt sie wie sie ist."""
        new_shape = rotate_cw(self.shape)
        new_image = pygame.transform.rotate(self.image, -90)  # -90 Grad = im Uhrzeigersinn

        # Test: passt die neue Form?
        if not self.check_coll(new_shape, grid):
            self.shape = new_shape
            self.image = new_image
        # sonst passiert nichts – Figur bleibt wie sie war

    def check_coll(self, test_shape, grid):
        """Hilfsfunktion für Drehung: testet, ob eine Form ins Raster passt."""
        for row_idx, row in enumerate(test_shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = self.x + col_idx
                    y = self.y + row_idx

                    if x < 0 or x >= config.COLS:
                        return True
                    if y >= config.ROWS:
                        return True
                    if y >= 0 and grid[y][x] is not None:
                        return True
        return False
    
    def draw(self, surface):
        px = self.x * config.BLOCK_SIZE
        py = self.y * config.BLOCK_SIZE
        surface.blit(self.image, (px, py))