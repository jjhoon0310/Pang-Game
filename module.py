import time
import os
import pygame
from pygame import mixer
import random

pygame.init()
mixer.init()

# Set screen title
pygame.display.set_caption("Emotional Game")
clock = pygame.time.Clock()

# Set screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
bg_color = (255, 255, 255)
screen.fill(bg_color)

game_font = pygame.font.Font(None, 40)
text_color = (0, 0, 0)
title_font = pygame.font.SysFont("Arial", 35, bold=True, italic=False)

# Accessing file
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "Image")

# Setting Background
background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]


def run(level):
    # Seting Character
    charater = pygame.image.load(os.path.join(image_path, "charater.png"))
    charater_size = charater.get_rect().size
    charater_width = charater_size[0]
    charater_height = charater_size[1]
    charater_x_pos = (screen_width / 2) - (charater_width / 2)
    charater_y_pos = screen_height - charater_height - stage_height
    charater_x = 0
    charater_speed = 5

    # Setting weapon numbers based on level
    if level == 1:
        weapon_count = 100
        weapon_number = 100
        shot_interval = 0
    elif level == 2 or 3:
        weapon_count = 30
        weapon_number = 30
        shot_interval = 0.3

    # Setting Weapon
    weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
    weapon_size = weapon.get_rect().size
    weapon_width = weapon_size[0]
    weapons = []  # Array of weapons to shoot multiple
    weapon_speed = 7
    weapon_counter = game_font.render("Bullet left: {}".format(
        int(weapon_count)), True, (255, 255, 255))

    # Setting balls in four different sizes
    balloon = [
        pygame.image.load(os.path.join(image_path, "balloon1.png")),
        pygame.image.load(os.path.join(image_path, "balloon2.png")),
        pygame.image.load(os.path.join(image_path, "balloon3.png")),
        pygame.image.load(os.path.join(image_path, "balloon4.png"))
    ]

    balloon_y_speed = [-20, -15, -12, -12]
    balloons = []

    # The first balloon
    balloons.append({
        "pos_x": 50,  # X location
        "pos_y": 50,  # Y location
        "img_idx": 0,  # Which ball (index)
        "to_x": 3,  # X direction
        "to_y": -6,  # Y direction
        "init_spd_y": balloon_y_speed[0]  # Y initial speed
    })

    # Saving weapon & balloon numbers
    weapon_to_remove = -1
    balloon_to_remove = -1

    total_time = 100
    last_shot_time = 0
    start_ticks = pygame.time.get_ticks()
    game_reslut = "Game Over"

    running = True
    while running:
        dt = clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Control character
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    charater_x -= charater_speed
                elif event.key == pygame.K_RIGHT:
                    charater_x += charater_speed
                elif event.key == pygame.K_SPACE and time.time() - last_shot_time > shot_interval:
                    weapon_x_pos = charater_x_pos + \
                        (charater_width/2) - (weapon_width/2)
                    weapon_y_pos = charater_y_pos
                    weapons.append([weapon_x_pos, weapon_y_pos])
                    last_shot_time = time.time()

                    # Counting weapon numbers
                    weapon_count -= 1
                    weapon_counter = game_font.render("Bullet left: {}".format(
                        int(weapon_count)), True, (255, 255, 255))

                    # Random number to quit game
                    rand_num = random.randint(6, 9)
                    if level == 4 and rand_num == 7:
                        mixer.music.load("Pang-Game/emotional.mp3")
                        mixer.music.set_volume(0.7)
                        mixer.music.play()
                        game_reslut = "Emotional Damage!"
                        pygame.time.delay(1500)
                        running = False
                        break

                    pygame.display.update()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    charater_x = 0

        # Charater location
        charater_x_pos += charater_x

        if charater_x_pos < 0:
            charater_x_pos = 0
        elif charater_x_pos > screen_width - charater_width:
            charater_x_pos = screen_width - charater_width

        # Weapon location
        # 100, 200 -> 180, 160, 140, ...
        # 500, 200 -> 180, 160, 140, ...
        weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

        # Remove when it touches the roof
        weapons = [[w[0], w[1]]for w in weapons if w[1] > 0]

        # Balloon locaton
        for balloon_idx, balloon_val in enumerate(balloons):
            balloon_x_pos = balloon_val["pos_x"]
            balloon_y_pos = balloon_val["pos_y"]
            balloon_img_idx = balloon_val["img_idx"]

            balloon_size = balloon[balloon_img_idx].get_rect().size
            balloon_width = balloon_size[0]
            balloon_height = balloon_size[1]

            # Bounce off when it touches the wall
            if balloon_x_pos < 0 or balloon_x_pos > screen_width - balloon_width:
                balloon_val["to_x"] = balloon_val["to_x"] * -1

            # Bounce upwards when it touches the floor
            if balloon_y_pos >= screen_height - stage_height - balloon_height:
                balloon_val["to_y"] = balloon_val["init_spd_y"]
            else:  # Or the ball accelerates
                balloon_val["to_y"] += 0.5

            balloon_val["pos_x"] += balloon_val["to_x"]
            balloon_val["pos_y"] += balloon_val["to_y"]

        # Crash with enemy
        charater_rect = charater.get_rect()
        charater_rect.left = charater_x_pos
        charater_rect.top = charater_y_pos

        for balloon_idx, balloon_val in enumerate(balloons):
            balloon_x_pos = balloon_val["pos_x"]
            balloon_y_pos = balloon_val["pos_y"]
            balloon_img_idx = balloon_val["img_idx"]

            # Rect of the balloon
            balloon_rect = balloon[balloon_img_idx].get_rect()
            balloon_rect.left = balloon_x_pos
            balloon_rect.top = balloon_y_pos

            # Crash character and balloon
            if charater_rect.colliderect(balloon_rect):
                running = False
                break

            # Chrash with enemy and weapon
            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_x_pos = weapon_val[0]
                weapon_y_pos = weapon_val[1]

                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_x_pos
                weapon_rect.top = weapon_y_pos

                # Crash weapon and balloon
                if weapon_rect.colliderect(balloon_rect):
                    weapon_to_remove = weapon_idx
                    balloon_to_remove = balloon_idx

                    # If it is not the smallest ball
                    if balloon_img_idx < 3:
                        # Current balloon size
                        balloon_width = balloon_rect.size[0]
                        balloon_height = balloon_rect.size[1]

                        # Divided ballon size
                        small_balloon_rect = balloon[balloon_img_idx + 1].get_rect()
                        small_balloon_width = small_balloon_rect.size[0]
                        small_balloon_height = small_balloon_rect.size[1]

                        # Divided balloon going left
                        balloons.append({
                            "pos_x": balloon_x_pos + (balloon_width / 2) - (small_balloon_width / 2),
                            "pos_y": balloon_y_pos + (balloon_height / 2) - (small_balloon_height / 2),
                            "img_idx": balloon_img_idx + 1,
                            "to_x": -3,
                            "to_y": -6,
                            "init_spd_y": balloon_y_speed[balloon_img_idx + 1]})

                        # Divided balloon going right
                        balloons.append({
                            "pos_x": balloon_x_pos + (balloon_width/2) - (small_balloon_width/2),
                            "pos_y": balloon_y_pos + (balloon_height/2) - (small_balloon_height/2),
                            "img_idx": balloon_img_idx + 1,
                            "to_x": 3,
                            "to_y": -6,
                            "init_spd_y": balloon_y_speed[balloon_img_idx + 1]})

                        # Another balloon if the level is hard
                        if level == 3 and balloon_img_idx == 1:
                            balloons.append({
                                "pos_x": balloon_x_pos + (balloon_width/2) - (small_balloon_width/2),
                                "pos_y": balloon_y_pos + (balloon_height/2) - (small_balloon_height/2),
                                "img_idx": balloon_img_idx + 1,
                                "to_x": -4,
                                "to_y": -7,
                                "init_spd_y": balloon_y_speed[balloon_img_idx + 1]})

                    break
            else:
                continue
            break

        # Delete crashed weapon and balloon
        if balloon_to_remove > -1:
            del balloons[balloon_to_remove]
            balloon_to_remove = -1

        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1

        if len(balloons) == 0:
            game_reslut = "Game Completed!"
            running = False

        # Make it visible
        screen.blit(background, (0, 0))

        for weapon_x_pos, weapon_y_pos in weapons:
            screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

        for idx, val in enumerate(balloons):
            balloon_x_pos = val["pos_x"]
            balloon_y_pos = val["pos_y"]
            balloon_img_idx = val["img_idx"]
            screen.blit(balloon[balloon_img_idx],
                        (balloon_x_pos, balloon_y_pos))

        screen.blit(stage, (0, screen_height - stage_height))
        screen.blit(charater, (charater_x_pos, charater_y_pos))
        if weapon_number == 100:
            pass
        else:
            screen.blit(weapon_counter, (430, 10))

        if weapon_count <= 0:
            game_reslut = "Out of Bullet!"
            running = False

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        timer = game_font.render("Time : {}".format(
            int(total_time - elapsed_time)), True, (255, 255, 255))
        screen.blit(timer, (10, 10))

        if total_time - elapsed_time <= 0:
            game_reslut = "Time Over"
            running = False

        pygame.display.update()  # Putting the game screen again

    msg = game_font.render(game_reslut, True, (255, 255, 0))
    msg_rect = msg.get_rect(
        center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(msg, msg_rect)
    pygame.display.update()

    pygame.time.delay(3000)

    pygame.quit()
