import pygame
import config
import random
from tetromino import Tetromino, L_SHAPE, O_SHAPE, I_SHAPE, S_SHAPE, Z_SHAPE, T_SHAPE, J_SHAPE

SHAPES = [
    {"matrix": Z_SHAPE, "image": "assets/Z-block.png", "color": (100, 200, 100)}, #...,...
    {"matrix": L_SHAPE, "image": "assets/L-block.png", "color": (200, 100, 100)}, #kater, grün
    {"matrix": O_SHAPE, "image": "assets/O-block.png", "color": (100, 100, 200)}, #..., ...
    {"matrix": T_SHAPE, "image": "assets/T-block.png", "color": (10, 10, 200)}, #..., ...
    {"matrix": S_SHAPE, "image": "assets/S-block.png", "color": (100, 150, 20)}, #..., ...
    {"matrix": I_SHAPE, "image": "assets/I-block.png", "color": (10, 150, 200)}, #..., ...
    {"matrix": J_SHAPE, "image": "assets/J-block.png", "color": (70, 220, 160)}, #..., ...


]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris-Geschenk")
        self.clock = pygame.time.Clock()

        self.grid = [[None for _ in range(config.COLS)] for _ in range(config.ROWS)]
        # ganzes 128x128-Bild laden
        #self.l_sprite = pygame.image.load("assets/L-block.png").convert_alpha()

        # Figur an Blockposition x=3, y=0
        self.tetromino = self.spawn_new_tetromino()
        #self.tetromino = Tetromino(3, 0, L_SHAPE, self.l_sprite)

        # schwerkraft
        self.fall_timer = 0
        self.fall_interval = 500  # ms = 0.5 Sekunden pro Schritt
        self.landed = False

    def run(self):
        running = True
        while running:
            self.clock.tick(config.FPS)
            self.screen.fill((100, 100, 100))  # ⬅️ HINTERGRUND zuerst!

            # Raster zeichnen (gelandete Blöcke)
            for y, row in enumerate(self.grid):
                for x, color in enumerate(row):
                    if color:
                        pygame.draw.rect(
                            self.screen,
                            color,
                            (x * config.BLOCK_SIZE, y * config.BLOCK_SIZE, config.BLOCK_SIZE, config.BLOCK_SIZE)
                        )

            # Fallbewegung
            if not self.landed:
                self.fall_timer += self.clock.get_time()
                if self.fall_timer > self.fall_interval:
                    self.fall_timer = 0
                    #print("→ Prüfe Kollision nach unten")  # Debug!
                    if not self.check_collision(0, 1):
                        self.tetromino.y += 1
                    else:
                        #print("Landed!")
                        self.landed = True
                        self.lock_tetromino()
                        self.clear_lines()
                        self.tetromino = self.spawn_new_tetromino()
                        self.landed = False

            # Tasteneingaben
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not self.landed:
                    if event.key == pygame.K_LEFT:
                        self.move_tetromino(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_tetromino(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_tetromino(0, 1)
                    elif event.key == pygame.K_UP:
                        self.tetromino.rotate(self.grid)

            # Aktive Figur zeichnen
            self.tetromino.draw(self.screen)

            # Anzeige aktualisieren
            pygame.display.flip()


    def check_collision(self, dx, dy):
        new_x = self.tetromino.x + dx
        new_y = self.tetromino.y + dy

        for row_idx, row in enumerate(self.tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    abs_x = new_x + col_idx
                    abs_y = new_y + row_idx

                    # Kollision mit Boden
                    if abs_y >= config.ROWS:
                        return True

                    # Kollision mit Seiten
                    if abs_x < 0 or abs_x >= config.COLS:
                        return True

                    if 0 <= abs_y < config.ROWS and 0 <= abs_x < config.COLS:
                        content = self.grid[abs_y][abs_x]
                        #print(f"Rastercheck an x={abs_x}, y={abs_y}: {content=}")
                        if content is not None:
                            #print("→ Kollision mit Raster erkannt!")
                            return True

        return False

    def clear_lines(self):
        new_grid = []
        lines_cleared = 0

        for row in self.grid:
            if all(cell is not None for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)

        # Leere Zeilen oben hinzufügen
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(config.COLS)])

        self.grid = new_grid

    def spawn_new_tetromino(self):
        choice = random.choice(SHAPES)
        image = pygame.image.load(choice["image"]).convert_alpha()
        return Tetromino(3, 0, choice["matrix"], image, choice["color"])
    
    def lock_tetromino(self):
        #print("LOCK: Figur wird ins Raster geschrieben")
        for row_idx, row in enumerate(self.tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.tetromino.x + col_idx
                    grid_y = self.tetromino.y + row_idx
                    if 0 <= grid_x < config.COLS and 0 <= grid_y < config.ROWS:
                        self.grid[grid_y][grid_x] = self.tetromino.color

    def move_tetromino(self, dx, dy):
        new_x = self.tetromino.x + dx
        new_y = self.tetromino.y + dy

        # Spielfeldgrenzen prüfen
        if 0 <= new_x <= config.COLS - 4 and 0 <= new_y <= config.ROWS - 4:
            self.tetromino.x = new_x
            self.tetromino.y = new_y
