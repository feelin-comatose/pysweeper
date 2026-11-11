import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Rectangles from List")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Example list of rectangles: each item is (x, y, width, height)
w = int(800/int(input()))
h = int(600/int(input()))

rectangles = [
    
]

mines = []
for j in range(-h, HEIGHT+1, h):
    for i in range(-w, WIDTH-49, w):
        rectangles.append([i+w, j, w, w])
print(rectangles)

# Colors
RECT_COLOR = (255, 0, 0)  # Red
RECT_COLOR2 = (0, 255, 0) # green
RECT_COLOR3 = (0, 0, 255) # blue
BG_COLOR = (30, 30, 30)   # Dark gray

def draw_rectangles(rect_list): # Draw rectangles from a list of tuples.
    for rect in rect_list:
        # Validate that rect is a tuple/list of 4 numbers
        if (isinstance(rect, (tuple, list)) and len(rect) == 4 
            and all(isinstance(v, (int, float)) for v in rect)):
            pygame.draw.rect(screen, RECT_COLOR, pygame.Rect(rect))
        else:
            print(f"Invalid rectangle data skipped: {rect}")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    # Fill background
    screen.fill(BG_COLOR)

    # Draw all rectangles
    draw_rectangles(rectangles)

    # Update display
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)
