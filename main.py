import sys, pygame, random, time, os
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
size = width, height = 1280, 1024
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Minesweeper")
screen = pygame.display.set_mode(size)


while True:
    for event in pygame.event.get():               # Check if any system events have happened
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
    pygame.display.flip()