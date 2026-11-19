import pygame, sys, os, random, time
from pygame.locals import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

WIDTH, HEIGHT = 1000, 1000
BG_COLOR = (30, 30, 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
images = {}
for file in os.listdir("assets"):
    if file.endswith(".png"):
        name = file.removesuffix(".png")
        images[name] = pygame.image.load(f"assets/{file}").convert_alpha()


pygame.display.set_caption("Spleen Sweeper")
pygame.display.set_icon(images["icon"])
clock = pygame.time.Clock()

cols = int(input("Columns: "))
rows = int(input("Rows: "))
mine_target = int(input("number of mines: "))
if cols < 1 or rows < 1:
    sys.exit("Columns and rows must be at least 1")

if mine_target < 0 or mine_target > (cols * rows) - 1:
    sys.exit("Mines must be between 0 and the number of cells")

class Tile:

    def __init__(self, column, row, x, y, w, h):
        self.column = column
        self.row = row
        self.rect = pygame.Rect(x, y, w, h)
        self.is_flagged = False
        self.is_mine = False
        self.is_open = False
        self.neighbors = []
        self.neighbor_mines = 0
        

    def resize(self, tile, xoffset, yoffset):
        x = xoffset + self.column * tile
        y = yoffset + self.row * tile
        self.rect = pygame.Rect(x, y, tile, tile)

    def display(self, state):
        scaled = pygame.transform.scale(state, (self.rect.width, self.rect.height))
        screen.blit(scaled, self.rect)
    
    def neighbor_count(self, tile_grid):
        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                if d_col == 0 and d_row == 0:
                    continue
                pos = (self.column + d_col, self.row + d_row)
                if pos in tile_grid:
                    self.neighbors.append(pos)
    
    def minenumber(self, tile_grid):
        count = 0

        for i in self.neighbors:
            neighbor = tile_grid[i]
            if neighbor.is_mine:
                count += 1

        self.neighbor_mines = count

def restart():
    global game_over, tile_list, tile_grid, first_click
    first_click = True
    tile_grid = {}
    tile_list = []
    game_over = False
    for row in range(rows):
        for column in range(cols):
            x = column * w
            y = row * h
            tile = Tile(column, row, x, y, w, h)
            tile_grid[(column, row)] = tile
            tile_list.append(tile)
    for t in tile_list:
        t.neighbor_count(tile_grid)
    resize_board()

def place_mines(safe_tile):
    tiles = tile_list.copy()
    tiles.remove(safe_tile)
    for i in random.sample(tiles, mine_target):
        i.is_mine = True
    for t in tile_list:
        t.minenumber(tile_grid)
            

def resize_board():
    (win_w, win_h) = pygame.display.get_window_size()
    w, h = win_w // cols, win_h // rows
    tile = min(w,h)
    grid_width, grid_height = tile*cols, tile*rows
    xoffset = (win_w - grid_width) // 2
    yoffset = (win_h - grid_height) // 2
    for i in tile_list:
        i.resize(tile, xoffset, yoffset)

def flood_fill(tile):
    tile.is_open = True
    todo = []
    if tile.neighbor_mines != 0:
        pass
    else:
        todo.append(tile)
    while len(todo) > 0:
        current = todo.pop()
        for i in current.neighbors:
            if tile_grid[i].is_open == True:
                pass
            elif tile_grid[i].is_flagged == True:
                pass
            else:
                tile_grid[i].is_open = True
                if tile_grid[i].neighbor_mines == 0:
                    todo.append(tile_grid[i])
                else:
                    pass

def chording():
    pass # todo
    
w = WIDTH // cols
h = HEIGHT // rows
tile_grid = {}
tile_list = []

alive = True
game_over = False
first_click = True
restart()

while alive:
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if event.button == 1 and game_over == False:  # Left mouse button
                for i in tile_list: 
                    if i.rect.collidepoint(mouse_pos):
                        if first_click == True:
                            place_mines(i)
                            first_click = False
                        if i.is_open:
                            break
                        elif i.is_flagged:
                            break
                        elif i.is_mine:
                            game_over = True
                            break
                        else:
                            flood_fill(i)
                            break

            elif event.button == 3 and game_over == False:  # Right mouse button
                for i in tile_list:
                    if i.rect.collidepoint(mouse_pos) and i.is_flagged == False and i.is_open == False:
                        i.is_flagged = not i.is_flagged
                    elif i.rect.collidepoint(mouse_pos) and i.is_flagged == True:
                        i.is_flagged = not i.is_flagged
            else: pass

    screen.fill(BG_COLOR)
    for i in tile_list:
        if i.is_flagged == True:
            i.display(images["flag"])
        elif i.is_mine == True and game_over == True:
            i.display(images["mine_exploded"])
        elif i.is_open == True:
            if i.neighbor_mines == 0:
                i.display(images["open_tile"])
            else:
                i.display(images[str(i.neighbor_mines)])
        else:
            i.display(images["closed_tile"])

    # print(screen)
    pygame.display.flip()
    