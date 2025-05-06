import pygame
import config
from tetromino import Tetromino, L_SHAPE, O_SHAPE, I_SHAPE, S_SHAPE, Z_SHAPE, T_SHAPE

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris-Geschenk")
        self.clock = pygame.time.Clock()

        # ganzes 128x128-Bild laden
        self.l_sprite = pygame.image.load("assets/L-block.png").convert_alpha()

        # Figur an Blockposition x=3, y=0
        self.tetromino = Tetromino(3, 0, L_SHAPE, self.l_sprite)

    def run(self):
        running = True
        while running:
            self.clock.tick(config.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            self.tetromino.draw(self.screen)
            pygame.display.flip()