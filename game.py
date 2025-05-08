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
        self.fall_interval = 400  # ms = 0.5 Sekunden pro Schritt
        self.landed = False

        self.score       = 0          # aktuelle Punkte
        self.lines_total = 0          # insgesamt gelöschte Zeilen
        self.level       = 1          # Startlevel

    def run(self):
        running = True
        while running:
    
            self.clock.tick(config.FPS)
            self.screen.fill((100, 100, 100))  # ⬅️ HINTERGRUND zuerst!
            self.draw_grid(self.screen)
            
            font = pygame.font.SysFont(None, 24)
            score_surf = font.render(f"Score: {self.score}", True, (255,255,255))
            level_surf = font.render(f"Level: {self.level}", True, (255,255,255))
            self.screen.blit(score_surf, (5, 5))
            self.screen.blit(level_surf, (5, 25))
            
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
                        self.mark_lines_for_removal()
                        self.clear_marked_lines()
                        self.tetromino = self.spawn_new_tetromino()
                        self.landed = False
                        if self.check_collision(0, 0):
                            self.game_over()
                            running = False          # Loop in `run()` beenden

            # Tasteneingaben
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN and not self.landed:
                    # LINKS
                    if event.key == pygame.K_LEFT:
                        self.move_tetromino(-1, 0)

                    # RECHTS
                    elif event.key == pygame.K_RIGHT:
                        self.move_tetromino(1, 0)

                    # SCHNELL NACH UNTEN
                    elif event.key == pygame.K_DOWN:
                        self.move_tetromino(0, 1)

                    # DREHEN
                    elif event.key == pygame.K_UP:
                        self.tetromino.rotate(self.grid)

            # Aktive Figur zeichnen
            self.tetromino.draw(self.screen)

            # Anzeige aktualisieren
            pygame.display.flip()

    def draw_grid(self, surface):
        bs = config.BLOCK_SIZE
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if not cell:
                    continue

                typ = cell["type"]
                if typ == "row_leader":
                    px = (x - cell["offset"]) * bs
                    py = y * bs
                    surface.blit(cell["image"], (px, py))

                elif typ == "color":
                    pygame.draw.rect(surface, cell["color"],
                                    (x * bs, y * bs, bs, bs))

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

    def clear_marked_lines(self):
        # 1 ▸ Zeilen herausfiltern, die gelöscht werden
        new_grid = [
            row for row in self.grid
            if not all(cell and cell["type"] == "color" for cell in row)
        ]
        removed = config.ROWS - len(new_grid)          # Anzahl gelöschter Zeilen

        # 2 ▸ Raster auffüllen
        for _ in range(removed):
            new_grid.insert(0, [None for _ in range(config.COLS)])
        self.grid = new_grid

        # 3 ▸ Punkte & Gesamtzähler
        if removed:
            self.lines_total += removed
            self.score += {1: 40, 2: 100, 3: 300, 4: 1200}[removed] * self.level

        # 4 ▸ Level-Logik ***HIER kommt dein Code***
        old_level = self.level
        self.level = 1 + self.lines_total // 10        # alle 10 Zeilen ein Level

        if self.level != old_level:
            # Fallgeschwindigkeit anpassen: Basis 500 ms − 40 ms pro Level,
            # aber nie schneller als 100 ms
            self.fall_interval = max(100, 500 - 40 * (self.level - 1))


    def mark_lines_for_removal(self):
        for y, row in enumerate(self.grid):
            if all(cell is not None for cell in row):
                base_color = next(
                    (cell.get("color") for cell in row if "color" in cell),
                    (180, 180, 180)
                )
                for cell in row:
                    cell["type"]  = "color"
                    cell["color"] = base_color
                    cell.pop("image", None)


    def spawn_new_tetromino(self):
        choice = random.choice(SHAPES)
        image = pygame.image.load(choice["image"]).convert_alpha()
        return Tetromino(3, 0, choice["matrix"], image, choice["color"])
    
    def lock_tetromino(self):
        bs   = config.BLOCK_SIZE          # 32 px
        full = self.tetromino.image       # 128 × 128

        for r, row in enumerate(self.tetromino.shape):
            # prüfe, ob die Matrix-Zeile Blöcke enthält
            if not any(row):
                continue

            # Zeilen-Sprite (128 × 32) ausschneiden
            strip = pygame.Surface((bs * 4, bs), pygame.SRCALPHA)
            strip.blit(full, (0, 0), (0, r * bs, bs * 4, bs))

            # linkeste belegte Spalte dieser Matrix-Zeile
            lead_c = row.index(1)

            for c, cell in enumerate(row):
                if not cell:
                    continue

                gx = self.tetromino.x + c
                gy = self.tetromino.y + r
                if gx < 0 or gx >= config.COLS or gy < 0 or gy >= config.ROWS:
                    continue

                if c == lead_c:                          # Row-Leader
                    self.grid[gy][gx] = {
                        "type":  "row_leader",
                        "image": strip,
                        "offset": lead_c,                # wie weit nach rechts blitten?
                        "color": self.tetromino.color
                    }
                else:                                    # reine Füllzelle
                    self.grid[gy][gx] = {"type": "filled"}


    def move_tetromino(self, dx, dy):
        # Prüfe: würde die Figur nach dx,dy kollidieren?
        if not self.check_collision(dx, dy):
            self.tetromino.x += dx
            self.tetromino.y += dy

    def game_over(self):
        print("GAME OVER! Score:", self.score)
        # optional: Highscore speichern, Meldung zeigen oder ins Hauptmenü

