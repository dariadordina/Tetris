import pygame
import sys
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
        pygame.display.set_caption("Tetris for Oti")
        self.clock = pygame.time.Clock()

        self.grid = [[None for _ in range(config.COLS)] for _ in range(config.ROWS)]
        # ganzes 128x128-Bild laden

        # Figur an Blockposition x=3, y=0
        self.tetromino = self.spawn_new_tetromino()

        # schwerkraft
        self.fall_timer = 0
        self.fall_interval = 500  # ms = 0.5 Sekunden pro Schritt
        self.landed = False

        self.score       = 0          # aktuelle Punkte
        self.lines_total = 0          # insgesamt gelöschte Zeilen
        self.level       = 1          # Startlevel

        self.state = "play"        # "play" oder "gameover"
        self.font  = pygame.font.SysFont(None, 36)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(config.FPS)

            # ---------- 1. Ereignisse verarbeiten ----------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # zustands­abhängige Eingaben
                if self.state == "play":
                    self.handle_play_event(event)
                elif self.state == "gameover":
                    self.handle_gameover_event(event)

            # ---------- 2. Spiellogik aktualisieren ----------
            if self.state == "play":
                self.update_play()          # Schwerkraft, Landen, Punkte …

            # ---------- 3. Rendern ----------
            if self.state == "play":
                self.render_play()
            else:                           # "gameover"
                self.render_gameover()


            
            

    def update_play(self):
        # Schwerkraft & Landen
        if not self.landed:
            self.fall_timer += self.clock.get_time()
            if self.fall_timer > self.fall_interval:
                self.fall_timer = 0
                if not self.check_collision(0, 1):
                    self.tetromino.y += 1
                else:
                    self.landed = True
                    self.lock_tetromino()
                    self.mark_lines_for_removal()
                    self.clear_marked_lines()
                    self.tetromino = self.spawn_new_tetromino()
                    self.landed = False
                    if self.check_collision(0, 0):
                        self.state = "gameover"

    
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

    def render_play(self):
        self.screen.fill((100, 100, 100))

        # -- Score-Leiste -------------------------------------------------
        bar_h = 60
        pygame.draw.rect(self.screen, (40, 40, 40),
                        (0, 0, config.SCREEN_WIDTH, bar_h))          # fester Balken

        score_s = self.font.render(f"Score: {self.score}", True, (255,255,255))
        level_s = self.font.render(f"Level: {self.level}", True, (255,255,255))
        self.screen.blit(score_s, (10, 10))
        self.screen.blit(level_s, (10, 30))
        # ----------------------------------------------------------------

        # Raster + aktive Figur
        self.draw_grid(self.screen)
        self.tetromino.draw(self.screen)

        pygame.display.flip()

    def render_gameover(self):
        self.screen.fill((30, 30, 30))

        # Titel-Text
        text  = self.font.render("GAME OVER", True, (240, 50, 50))
        text2 = self.font.render(f"Your score: {self.score}", True, (200, 200, 200))
        rect  = text.get_rect(center=(config.SCREEN_WIDTH//2, 150))
        rect2 = text2.get_rect(center=(config.SCREEN_WIDTH//2, 200))
        self.screen.blit(text, rect)
        self.screen.blit(text2, rect2)

        # Restart-Button
        self.button_rect = pygame.Rect(0, 0, 180, 50)
        self.button_rect.center = (config.SCREEN_WIDTH//2, 300)
        pygame.draw.rect(self.screen, (70, 180, 70), self.button_rect, border_radius=8)
        btn_text = self.font.render("Neu starten", True, (0, 0, 0))
        self.screen.blit(btn_text, btn_text.get_rect(center=self.button_rect.center))

        pygame.display.flip()

    def handle_play_event(self, event):
        if event.type == pygame.KEYDOWN and not self.landed:
            if event.key == pygame.K_LEFT:
                self.move_tetromino(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.move_tetromino(1, 0)
            elif event.key == pygame.K_DOWN:
                self.move_tetromino(0, 1)
            elif event.key == pygame.K_UP:
                self.tetromino.rotate(self.grid)

    def handle_gameover_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.restart_game()

    def restart_game(self):
        self.grid        = [[None for _ in range(config.COLS)] for _ in range(config.ROWS)]
        self.tetromino   = self.spawn_new_tetromino()
        self.fall_timer  = 0
        self.fall_interval = 500
        self.landed      = False
        self.score       = 0
        self.lines_total = 0
        self.level       = 1
        self.state       = "play"

