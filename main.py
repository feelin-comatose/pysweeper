import pygame, sys, os, random
from pygame.locals import *

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
screen1 = screen.copy()
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
while alive:
    pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    newx, newy = 0, 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.WINDOWRESIZED:
            screen = pygame.display.set_mode((event.x, event.y), HWSURFACE|DOUBLEBUF|RESIZABLE)
            newx, newy = event.x, event.y

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mouse.set_pos(pos)
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if event.button == 1:  # Left mouse button
                for i in rectangles: 
                    if i[0].collidepoint(mouse_pos): # i[0] = pygame.rect
                        if i[2] == 0:
                            if i[1] == 1: #i[1] = mine flag
                                print("Mine clicked!")
                                alive = False
                            else:
                                print("Safe cell clicked!")
                        else:
                            print("field is flagged")
                
            elif event.button == 3:  # Right mouse button
                for i in rectangles:
                    if i[0].collidepoint(mouse_pos) and i[2] == 0:
                        print("flagged")
                        i[2] = not i[2] # i[2] = well... flag for flagging tiles?
                    elif i[0].collidepoint(mouse_pos) and i[2] == 1:
                        print("flag removed")
                        i[2] = not i[2]

    screen.fill(BG_COLOR)
    for i in rectangles:
        if i[2] == 1:
            if i[1] == 1:
                pygame.draw.rect(screen1, COLORS[2], i[0])
            else:
                pygame.draw.rect(screen1, COLORS[2], i[0])
        else:
            if i[1] == 1:
                pygame.draw.rect(screen1, COLORS[0], i[0])
            else:
                pygame.draw.rect(screen1, COLORS[1], i[0])

    # print(screen)
    screen.blit(pygame.transform.scale(screen1, screen.get_rect().size), (0, 0))
    pygame.display.flip()
    