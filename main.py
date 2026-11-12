import pygame, sys, os, random, time
from pygame.locals import *

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
icon = pygame.image.load(os.path.join('icon.png'))
pygame.display.set_caption("Draw Rectangles from List")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

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

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
BG_COLOR = (30, 30, 30)

# Build the grid once, each cell with its own fixed colour
rectangles = []
for y in range(0, rows * h, h):
    for x in range(0, cols * w, w):
        rectangles.append([pygame.Rect(x, y, w-1, h-1), 0, 0])

# Place exactly mine_target mines on random, distinct cells
for i in random.sample(range(len(rectangles)), mine_target):
    rectangles[i][1] = 1

# print(rectangles[1][0])

# print(rectangles, mine_target)
pygame.init()
alive = True
game_over = False

if game_over == True:
    for i in rectangles:
        if i[1] == 1:
            pygame.draw.rect(screen, COLORS[0], i[0])
    pygame.display.set_caption("Game Over !")
    time.sleep(5)
    sys.exit()

while alive:
    clock.tick(60)
    
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
            for n, cell in enumerate(rectangles):
                column = n % cols
                row    = n // cols
                x = xoffset + column * tile
                y = yoffset + row * tile
                cell[0] = pygame.Rect(x, y, tile-1, tile-1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if event.button == 1:  # Left mouse button
                for i in rectangles: 
                    if game_over == True:
                        pass
                    else:
                        if i[0].collidepoint(mouse_pos): # i[0] = pygame.rect
                            if i[2] == 0:
                                if i[1] == 1: #i[1] = mine flag
                                    print("Mine clicked!")
                                    game_over = True
                                else:
                                    print("Safe cell clicked!")
                            else:
                                print("field is flagged")
                
            elif event.button == 3:  # Right mouse button
                for i in rectangles:
                    if game_over == True:
                        pass
                    else:
                        if i[0].collidepoint(mouse_pos) and i[2] == 0:
                            print("flagged")
                            i[2] = not i[2] # i[2] = well... flag for flagging tiles?
                        elif i[0].collidepoint(mouse_pos) and i[2] == 1:
                            print("flag removed")
                            i[2] = not i[2]

    screen.fill(BG_COLOR)
    for i in rectangles:
        if i[2] == 1:
            pygame.draw.rect(screen, COLORS[2], i[0])
        elif i[1] == 1 and game_over == True:
            pygame.draw.rect(screen, COLORS[0], i[0])
        else:
            pygame.draw.rect(screen, COLORS[1], i[0])

    # print(screen)
    pygame.display.flip()
    