import sys, pygame, random, time
pygame.init()
size = width, height = 1280, 1024
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(size)


while True:
    for event in pygame.event.get():               # Check if any system events have happened
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()