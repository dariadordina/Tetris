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

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_tetromino(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_tetromino(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_tetromino(0, 1)


            self.screen.fill((0, 0, 0))
            self.tetromino.draw(self.screen)
            pygame.display.flip()
    
    def move_tetromino(self, dx, dy):
        new_x = self.tetromino.x + dx
        new_y = self.tetromino.y + dy

        # Spielfeldgrenzen prüfen
        if 0 <= new_x <= config.COLS - 4 and 0 <= new_y <= config.ROWS - 4:
            self.tetromino.x = new_x
            self.tetromino.y = new_y