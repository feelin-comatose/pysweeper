import pygame, sys, os, random

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
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
        rectangles.append([pygame.Rect(x, y, w-1, h-1), 0])

# Place exactly mine_target mines on random, distinct cells
for i in random.sample(range(len(rectangles)), mine_target):
    rectangles[i][1] = 1

print(rectangles, mine_target)
pygame.init()
while True:
    pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pygame.mouse.set_pos(pos)

    screen.fill(BG_COLOR)
    for rect, flag in rectangles:
        if flag == 1:
            pygame.draw.rect(screen, COLORS[0], rect)
        else:
            pygame.draw.rect(screen, COLORS[1], rect)
        
    
    pygame.display.flip()
    