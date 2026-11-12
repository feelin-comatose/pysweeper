import pygame, sys, random, os


WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# icon = pygame.image.load(os.path.join('icon.png'))
# pygame.display.set_caption("Draw Rectangles from List")
# pygame.display.set_icon(icon)
# clock = pygame.time.Clock()

# Ask BEFORE the loop, and validate the input
cols = int(input("Columns: "))
rows = int(input("Rows: "))
mine_target = int(input("number of mines: "))
if cols < 1 or rows < 1:
    sys.exit("Columns and rows must be at least 1")

w = WIDTH // cols
h = HEIGHT // rows

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
BG_COLOR = (30, 30, 30)

# Build the grid once, each cell with its own fixed colour
rectangles = []
minecoordinates = []
for y in range(0, rows * h, h):
    for x in range(0, cols * w, w):
        rectangles.append([pygame.Rect(x, y, w - 2, h - 2), 0])

# Place exactly mine_target mines on random, distinct cells
for i in random.sample(range(len(rectangles)), mine_target):
    rectangles[i][1] = 1
    minecoordinates.append([rectangles[i][0].x, rectangles[i][0].x+w, rectangles[i][0].y, rectangles[i][0].y+h])

print(minecoordinates)

# print(rectangles, mine_target)