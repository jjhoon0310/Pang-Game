import os
import pygame
from pygame import time

pygame.init() 

# Background
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
bg_color = (255, 255, 255)
screen.fill(bg_color)

# Game title
pygame.display.set_caption("Emotional Game")

clock = pygame.time.Clock()
button_clicked = False

###################################################
# Title
text_color = (0, 0, 0)

title_font = pygame.font.SysFont("Arial", 35, bold=True, italic=False)
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

button_mid = button_font.render("Hard", True, text_color)
button_mid_pos = screen_width/2, screen_height/2 + 70
button_mid_rect = button_mid.get_rect(center=(button_mid_pos))
button_mid_back = pygame.draw.rect(screen, (240, 240, 240), 
                    pygame.Rect(screen_width/2 - 140, screen_height/2 - 10, 280, 40))

button_hard = button_font.render("Medium", True, text_color)
button_hard_pos = screen_width/2, screen_height/2 + 10
button_hard_rect = button_hard.get_rect(center=(button_hard_pos))
button_hard_back = pygame.draw.rect(screen, (240, 240, 240), 
                    pygame.Rect(screen_width/2 - 140, screen_height/2 + 50, 280, 40))

screen.blit(button_easy, button_easy_rect)
screen.blit(button_hard, button_hard_rect)
screen.blit(button_mid, button_mid_rect)
pygame.display.update()

def main(): 
    main_running = True
    while main_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_easy_back.collidepoint(event.pos):
                    return
                                        
                if button_mid_back.collidepoint(event.pos):
                    return

                if button_hard_back.collidepoint(event.pos):
                    return
            
main()