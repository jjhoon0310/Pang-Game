import pygame
from module import *
from count import countdown

pygame.init()

title = title_font.render("Emotional Game", True, text_color)
title_pos = screen_width/2, screen_height/2 - 130
text_rect = title.get_rect(center=(title_pos))
screen.blit(title, text_rect)

# Buttons
button_font = pygame.font.SysFont("Arial", 23, bold=False, italic=False)
button_easy = button_font.render("Easy", True, text_color)
button_easy_pos = screen_width/2, screen_height/2 - 50
button_easy_rect = button_easy.get_rect(center=(button_easy_pos))
button_easy_back = pygame.draw.rect(screen, (240, 240, 240),
                                    pygame.Rect(screen_width/2 - 140, screen_height/2 - 70, 280, 40))

button_mid = button_font.render("Medium", True, text_color)
button_mid_pos = screen_width/2, screen_height/2 + 10
button_mid_rect = button_mid.get_rect(center=(button_mid_pos))
button_mid_back = pygame.draw.rect(screen, (240, 240, 240),
                                   pygame.Rect(screen_width/2 - 140, screen_height/2 - 10, 280, 40))

button_hard = button_font.render("Hard", True, text_color)
button_hard_pos = screen_width/2, screen_height/2 + 70
button_hard_rect = button_hard.get_rect(center=(button_hard_pos))
button_hard_back = pygame.draw.rect(screen, (240, 240, 240),
                                    pygame.Rect(screen_width/2 - 140, screen_height/2 + 50, 280, 40))

button_asian = button_font.render("Asian", True, (255, 0, 0))
button_asian_pos = screen_width/2, screen_height/2 + 130
button_asian_rect = button_asian.get_rect(center=(button_asian_pos))
button_asian_back = pygame.draw.rect(screen, (240, 240, 240),
                                     pygame.Rect(screen_width/2 - 140, screen_height/2 + 110, 280, 40))

screen.blit(button_easy, button_easy_rect)
screen.blit(button_mid, button_mid_rect)
screen.blit(button_hard, button_hard_rect)
screen.blit(button_asian, button_asian_rect)
pygame.display.update()


def main():
    main_running = True
    while main_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_easy_back.collidepoint(event.pos):
                    countdown(3, level=1)

                if button_mid_back.collidepoint(event.pos):
                    countdown(3, level=2)

                if button_hard_back.collidepoint(event.pos):
                    countdown(3, level=3)

                if button_asian_back.collidepoint(event.pos):
                    countdown(3, level=4)


main()
