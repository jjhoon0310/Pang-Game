import pygame
from module import *

pygame.init()


# Function for countdown before starting gmae
def countdown(t, level):
    while t:

        time.sleep(1)
        t -= 1

    if level == 1:
        run(weapon_count=100, weapon_number=100)
