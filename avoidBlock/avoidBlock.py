import random
import pygame
pygame.init() #Makes reset(Must)

#Screen size
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

#Game title
pygame.display.set_caption("Avoid Block")

clock = pygame.time.Clock()

# 1. Basic sets (Background, Charater(Location, Speed), Text)

background = pygame.image.load("avoidblock/background.png")

charater = pygame.image.load("avoidblock/character.png")
charater_size = charater.get_rect().size
charater_width = charater_size[0]
charater_height = charater_size[1]
x_pos = screen_width /2 - 35
y_pos = screen_height - 70
to_x = 0
charater_speed = 3

enemy = pygame.image.load("avoidblock/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0
enemy_speed = 7


# 2. Event lope
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 2-1. Control : keyboard or mouse
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= charater_speed
            elif event.key == pygame.K_RIGHT:
                to_x += charater_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
        
    # 2-2. Charater location
    x_pos += to_x

    if x_pos <= 0:
        x_pos = 0
    elif x_pos > screen_width -charater_width:
        x_pos = screen_width -charater_width

    enemy_y_pos += enemy_speed
    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - enemy_width)
   
    # 2-3. Crash with enemy
    charater_rect = charater.get_rect()
    charater_rect.left = x_pos
    charater_rect.top = y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    if charater_rect.colliderect(enemy_rect):
        running = False
    
    # 4. Make it visible
    screen.blit(background, (0, 0))
    screen.blit(charater, (x_pos, y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    pygame.display.update() #Putting the game screen again
    
pygame.quit()