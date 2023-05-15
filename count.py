import pygame
from module import *

pygame.init()


# Function for countdown before starting gmae
def countdown(t, level):
    while t:
        bg_color = (255, 255, 255)
        screen.fill(bg_color)
        count = pygame.font.SysFont("Arial", 50, bold=True).render(
            "{}".format(int(t)), True, text_color)
        count_pos = screen_width/2, screen_height/2
        text_rect = count.get_rect(center=(count_pos))
        screen.blit(count, text_rect)
        pygame.display.update()
        time.sleep(1)
        t -= 1

    if level == 1:
        run(level=1)
    elif level == 2:
        run(level=2)
    elif level == 3:
        run(level=3)
    elif level == 4:
        run(level=4)
