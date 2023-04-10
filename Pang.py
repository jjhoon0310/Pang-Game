###################################################
import os
import pygame
from pygame import time
pygame.init() #Makes reset(Must)

#Screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

#Game title
pygame.display.set_caption("Pang Game")

clock = pygame.time.Clock()

###################################################

# 1. Basic sets (Background, Charater(Location, Speed), Text)
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "Image")

background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

charater = pygame.image.load(os.path.join(image_path, "charater.png"))
charater_size = charater.get_rect().size    
charater_width = charater_size[0]
charater_height = charater_size[1]
charater_x_pos = (screen_width /2) - (charater_width /2)
charater_y_pos = screen_height - charater_height - stage_height
charater_x = 0
charater_speed = 5

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapons = []
weapon_speed = 7

balloon = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

balloon_y_speed = [-18, -15, -12, -9]
balloons = []
balloons.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3,
    "to_y" : -6,
    "init_spd_y" : balloon_y_speed[0]
})

weapon_to_remove = -1
balloon_to_remove = -1

game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()

game_reslut = "Game Over"



# 2. Event lope
running = True
while running:
    dt = clock.tick(40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 2-1. Control : keyboard or mouse
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                charater_x -= charater_speed
            elif event.key == pygame.K_RIGHT:
                charater_x += charater_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = charater_x_pos + (charater_width/2) - (weapon_width/2)
                weapon_y_pos = charater_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                charater_x = 0
        
    # 3. Charater location
    charater_x_pos += charater_x
    
    if charater_x_pos < 0:
        charater_x_pos = 0
    elif charater_x_pos > screen_width - charater_width:
        charater_x_pos = screen_width - charater_width

    # 3-1 Weapon location
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
    weapons = [ [w[0], w[1]]for w in weapons if w[1] > 0]

    # 3-2 Enemy locaton
    for balloon_idx, balloon_val in enumerate(balloons):
        balloon_x_pos = balloon_val["pos_x"]
        balloon_y_pos = balloon_val["pos_y"]
        balloon_img_idx = balloon_val["img_idx"]

        balloon_size = balloon[balloon_img_idx].get_rect().size
        balloon_width = balloon_size[0]
        balloon_height = balloon_size[1]

        if balloon_x_pos < 0 or balloon_x_pos > screen_width - balloon_width:
            balloon_val["to_x"] = balloon_val["to_x"] * -1 

        if balloon_y_pos >= screen_height - stage_height - balloon_height:
            balloon_val["to_y"] = balloon_val["init_spd_y"]
        else:
            balloon_val["to_y"] += 0.5

        balloon_val["pos_x"] += balloon_val["to_x"]
        balloon_val["pos_y"] += balloon_val["to_y"]

    # 4. Crash with enemy
    charater_rect = charater.get_rect()
    charater_rect.left = charater_x_pos
    charater_rect.top = charater_y_pos

    for balloon_idx, balloon_val in enumerate(balloons):
        balloon_x_pos = balloon_val["pos_x"]
        balloon_y_pos = balloon_val["pos_y"]
        balloon_img_idx = balloon_val["img_idx"]

        balloon_rect = balloon[balloon_img_idx].get_rect()
        balloon_rect.left = balloon_x_pos
        balloon_rect.top = balloon_y_pos

        if charater_rect.colliderect(balloon_rect):
            running = False
            break

        # 4-1 Chrash with enemy and weapon
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos

            if weapon_rect.colliderect(balloon_rect):
                weapon_to_remove = weapon_idx
                balloon_to_remove = balloon_idx

                if balloon_img_idx < 3:
                    # Current balloon size
                    balloon_width = balloon_rect.size[0]
                    balloon_height = balloon_rect.size[1]
                     
                    # Divided ballon size
                    small_balloon_rect = balloon[balloon_img_idx + 1].get_rect()
                    small_balloon_width = small_balloon_rect.size[0]
                    small_balloon_height = small_balloon_rect.size[1]

                    balloons.append({
                        "pos_x" : balloon_x_pos + (balloon_width / 2) - (small_balloon_width / 2),
                        "pos_y" : balloon_y_pos + (balloon_height / 2) - (small_balloon_height / 2),
                        "img_idx" : balloon_img_idx + 1,
                        "to_x" : -3,
                        "to_y" : -6,
                        "init_spd_y" : balloon_y_speed[balloon_img_idx + 1]})

                    balloons.append({
                        "pos_x" : balloon_x_pos + (balloon_width/2) - (small_balloon_width/2),
                        "pos_y" : balloon_y_pos + (balloon_height/2) - (small_balloon_height/2),
                        "img_idx" : balloon_img_idx + 1,
                        "to_x" : 3,
                        "to_y" : -6,
                        "init_spd_y" : balloon_y_speed[balloon_img_idx + 1]})
                
                break
        else:
            continue
        break  
    
    if balloon_to_remove > -1:
        del balloons[balloon_to_remove]
        balloon_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    if len(balloons) == 0:
        game_reslut = "Game Completed!"
        running = False
    
    # 5. Make it visible
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos)) 
    
    for idx, val in enumerate(balloons):
        balloon_x_pos = val["pos_x"]
        balloon_y_pos = val["pos_y"]
        balloon_img_idx = val["img_idx"]
        screen.blit(balloon[balloon_img_idx], (balloon_x_pos, balloon_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(charater, (charater_x_pos, charater_y_pos))
    
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))
    if total_time - elapsed_time <= 0:
        game_reslut = "Time Over"
        running = False

    pygame.display.update() #Putting the game screen again

msg = game_font.render(game_reslut, True, (255, 255, 0))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(3000)

pygame.quit()