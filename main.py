import pygame, sys, os, random, time
from pygame.locals import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
images = {}
for file in os.listdir("assets"):
    if file.endswith(".png"):
        name = file.removesuffix(".png")
        images[name] = pygame.image.load(f"assets/{file}")

pygame.display.set_caption("Spleen Sweeper")
pygame.display.set_icon(images["icon"])
clock = pygame.time.Clock()

class Tile:

    def __init__(self, column, row, x, y, w, h):
        self.column = column
        self.row = row
        self.image = images["closed_tile"]
        self.rect = pygame.Rect(x, y, w-1, h-1)
        self.is_flagged = False
        self.is_mine = False
        self.is_open = False

    def resize(self, tile, xoffset, yoffset):
        x = xoffset + self.column * tile
        y = yoffset + self.row * tile
        self.rect = pygame.Rect(x, y, tile - 1, tile - 1)

    def display(self, state):
        scaled = pygame.transform.scale(state, (self.rect.width, self.rect.height))
        screen.blit(scaled, self.rect)

    def minenumber(self):
        count = 0

# Ask BEFORE the loop, and validate the input
cols = int(input("Columns: "))
rows = int(input("Rows: "))
mine_target = int(input("number of mines: "))
if cols < 1 or rows < 1:
    sys.exit("Columns and rows must be at least 1")

if mine_target < 0 or mine_target > cols * rows:
    sys.exit("Mines must be between 0 and the number of cells")

w = WIDTH // cols
h = HEIGHT // rows

BG_COLOR = (30, 30, 30)

# Build the grid once, each cell with its own fixed colour
tile_list = []
for row in range(rows):
    for column in range(cols):
        x = column * w
        y = row * h
        tile_list.append(Tile(column, row, x, y, w, h))

# Place exactly mine_target mines on random, distinct cells
for i in random.sample(range(len(tile_list)), mine_target):
    tile_list[i].is_mine = True

pygame.init()
alive = True
game_over = False

while alive:
    clock.tick(60)
    
    if game_over == True:
        for i in tile_list:
            if i.is_mine == True:
                i.display(images["mine"])
        pygame.display.set_caption("Game Over !")
        time.sleep(3)
        sys.exit()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.WINDOWRESIZED:
            screen = pygame.display.set_mode((event.x, event.y), HWSURFACE|DOUBLEBUF|RESIZABLE)
            w, h = event.x // cols, event.y // rows
            tile = min(w,h)
            grid_width, grid_height = tile*cols, tile*rows
            xoffset = (event.x - grid_width) // 2
            yoffset = (event.y - grid_height) // 2
            for i in tile_list:
                i.resize(tile, xoffset, yoffset)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if event.button == 1:  # Left mouse button
                for i in tile_list: 
                    if i.rect.collidepoint(mouse_pos): # i[0] = pygame.rect
                        i.minenumber()
                        if i.is_flagged == 0:
                            if i.is_mine == True: #i[1] = mine flag
                                print("Mine clicked!")
                                game_over = True
                            else:
                                print("Safe cell clicked!")
                                i.is_open = True
                        else:
                            print("field is flagged")
                
            elif event.button == 3:  # Right mouse button
                for i in tile_list:
                    if i.rect.collidepoint(mouse_pos) and i.is_flagged == 0 and i.is_open == False:
                        print("flagged")
                        i.is_flagged = not i.is_flagged # i[2] = well... flag for flagging tiles?
                    elif i.rect.collidepoint(mouse_pos) and i.is_flagged == 1:
                        print("flag removed")
                        i.is_flagged = not i.is_flagged
                    elif i.rect.collidepoint(mouse_pos) and i.is_flagged == 0 and i.is_open == True:
                        pass

    screen.fill(BG_COLOR)
    for i in tile_list:
        if i.is_flagged == True:
            i.display(images["flag"])
        elif i.is_mine == True and game_over == True:
            i.display(images["mine"])
        elif i.is_open == True:
            i.display(images["open_tile"])
        else:
            i.display(images["closed_tile"])

    # print(screen)
    pygame.display.flip()
    