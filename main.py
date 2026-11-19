import os
import random
import sys

import pygame

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 1000, 1000
BG_COLOR = (30, 30, 30)
MAX_SIZE = 200  # upper bound for columns/rows so tiles stay clickable
TITLE = "Spleen Sweeper"


def ask_int(prompt, low, high):
    """Ask for an integer in [low, high] until the user gives a valid one."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue
        except EOFError:
            sys.exit("No input given")
        if low <= value <= high:
            return value
        print(f"Please enter a number between {low} and {high}.")


# Ask for the board settings BEFORE opening the window, otherwise the window
# sits there unresponsive while the terminal waits for input.
cols = ask_int("Columns: ", 1, MAX_SIZE)
rows = ask_int("Rows: ", 1, MAX_SIZE)
mine_target = ask_int("Number of mines: ", 0, cols * rows - 1)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
images = {}
for file in os.listdir("assets"):
    if file.endswith(".png"):
        name = file.removesuffix(".png")
        images[name] = pygame.image.load(f"assets/{file}").convert_alpha()

pygame.display.set_icon(images["icon"])
clock = pygame.time.Clock()

# Scaled copies of the images, rebuilt only when the tile size changes.
scaled_images = {}


class Tile:

    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.is_flagged = False
        self.is_mine = False
        self.is_open = False
        self.neighbors = []
        self.neighbor_mines = 0

    def resize(self, tile, xoffset, yoffset):
        x = xoffset + self.column * tile
        y = yoffset + self.row * tile
        self.rect = pygame.Rect(x, y, tile, tile)

    def display(self, name):
        screen.blit(scaled_images[name], self.rect)

    def find_neighbors(self, tile_grid):
        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                if d_col == 0 and d_row == 0:
                    continue
                pos = (self.column + d_col, self.row + d_row)
                if pos in tile_grid:
                    self.neighbors.append(tile_grid[pos])

    def count_mines(self):
        self.neighbor_mines = sum(n.is_mine for n in self.neighbors)

    def image_name(self):
        if state == "lost":
            if self is exploded_tile:
                return "mine_exploded"
            if self.is_mine and not self.is_flagged:
                return "mine"
        if self.is_flagged:
            return "flag"
        if not self.is_open:
            return "closed_tile"
        if self.neighbor_mines == 0:
            return "open_tile"
        return str(self.neighbor_mines)


def restart():
    global state, tile_list, tile_grid, first_click, exploded_tile, opened
    first_click = True
    state = "playing"
    exploded_tile = None
    opened = 0
    tile_grid = {}
    tile_list = []
    for row in range(rows):
        for column in range(cols):
            tile = Tile(column, row)
            tile_grid[(column, row)] = tile
            tile_list.append(tile)
    for t in tile_list:
        t.find_neighbors(tile_grid)
    resize_board()
    update_caption()


def place_mines(safe_tile):
    # Keep the first clicked tile safe, and its neighbours too when there is
    # enough room, so the first click usually opens an area.
    safe = {safe_tile}
    if cols * rows - 1 - len(safe_tile.neighbors) >= mine_target:
        safe.update(safe_tile.neighbors)
    candidates = [t for t in tile_list if t not in safe]
    for t in random.sample(candidates, mine_target):
        t.is_mine = True
    for t in tile_list:
        t.count_mines()


def resize_board():
    win_w, win_h = pygame.display.get_window_size()
    tile = max(1, min(win_w // cols, win_h // rows))
    xoffset = (win_w - tile * cols) // 2
    yoffset = (win_h - tile * rows) // 2
    for t in tile_list:
        t.resize(tile, xoffset, yoffset)
    scaled_images.clear()
    for name, image in images.items():
        scaled_images[name] = pygame.transform.scale(image, (tile, tile))


def tile_at(pos):
    for t in tile_list:
        if t.rect.collidepoint(pos):
            return t
    return None


def flood_fill(tile):
    """Open a tile; if it has no neighbouring mines, open the area around it."""
    global opened
    todo = [tile]
    while todo:
        current = todo.pop()
        if current.is_open or current.is_flagged:
            continue
        current.is_open = True
        opened += 1
        if current.neighbor_mines == 0:
            todo.extend(current.neighbors)


def open_tile(tile):
    global state, exploded_tile
    if tile.is_open or tile.is_flagged:
        return
    if tile.is_mine:
        state = "lost"
        exploded_tile = tile
        return
    flood_fill(tile)


def chording(tile):
    """Clicking an open number with enough flags around opens the other neighbours."""
    if not tile.is_open or tile.neighbor_mines == 0:
        return
    flags = sum(n.is_flagged for n in tile.neighbors)
    if flags != tile.neighbor_mines:
        return
    for n in tile.neighbors:
        open_tile(n)
        if state == "lost":
            return


def check_win():
    global state
    if state == "playing" and opened == cols * rows - mine_target:
        state = "won"
        for t in tile_list:
            if t.is_mine:
                t.is_flagged = True


def update_caption():
    if state == "won":
        text = "You win! Press R to restart"
    elif state == "lost":
        text = "Boom! Press R to restart"
    else:
        flags = sum(t.is_flagged for t in tile_list)
        text = f"Mines left: {mine_target - flags}"
    pygame.display.set_caption(f"{TITLE} - {text}")


def draw_wrong_flags():
    """After losing, cross out flags that were not on a mine."""
    for t in tile_list:
        if t.is_flagged and not t.is_mine:
            width = max(1, t.rect.width // 10)
            pygame.draw.line(screen, (220, 30, 30), t.rect.topleft, t.rect.bottomright, width)
            pygame.draw.line(screen, (220, 30, 30), t.rect.topright, t.rect.bottomleft, width)


tile_grid = {}
tile_list = []
state = "playing"
first_click = True
exploded_tile = None
opened = 0
restart()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.WINDOWRESIZED:
            resize_board()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                restart()
        elif event.type == pygame.MOUSEBUTTONDOWN and state == "playing":
            tile = tile_at(event.pos)
            if tile is None:
                continue
            if event.button == 1:  # Left mouse button
                if tile.is_open:
                    chording(tile)
                elif not tile.is_flagged:
                    if first_click:
                        place_mines(tile)
                        first_click = False
                    open_tile(tile)
            elif event.button == 2:  # Middle mouse button
                chording(tile)
            elif event.button == 3:  # Right mouse button
                if not tile.is_open:
                    tile.is_flagged = not tile.is_flagged
            check_win()
            update_caption()

    screen.fill(BG_COLOR)
    for t in tile_list:
        t.display(t.image_name())
    if state == "lost":
        draw_wrong_flags()
    pygame.display.flip()
