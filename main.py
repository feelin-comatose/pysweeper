import pygame
import sys
import random


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Rectangles from List")
clock = pygame.time.Clock()

# Ask BEFORE the loop, and validate the input
cols = int(input("Columns: "))
rows = int(input("Rows: "))
if cols < 1 or rows < 1:
    sys.exit("Columns and rows must be at least 1")

w = WIDTH // cols
h = HEIGHT // rows

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
BG_COLOR = (30, 30, 30)

# Build the grid once, each cell with its own fixed colour
rectangles = []
mines = []
for y in range(0, rows * h, h):
    for x in range(0, cols * w, w):
        rectangles.append((pygame.Rect(x, y, w - 2, h - 2), random.choice(COLORS)))

for i in rectangles:
    r = random.randint(0, 1)
    if r == 0:
        mines.append(False)
    else:
        mines.append(True)
print(mines)
pygame.init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)
    for rect, color in rectangles:
        pygame.draw.rect(screen, color, rect)

    pygame.display.flip()
    clock.tick(60)