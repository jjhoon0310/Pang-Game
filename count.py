import pygame
from module import *

pygame.init()


# Function for countdown before starting gmae
def countdown(t, level):
    while t:

        time.sleep(1)
        t -= 1

    if level == 1:
        run(level=1)
    elif level == 2:
        run(level=2)
