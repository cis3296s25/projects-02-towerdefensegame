import pygame
import os #required for .exe creation
import sys #required for .exe creation
import random
from pygame import(
    image,
    mixer,
)
from EnemyLogic import Enemy, WAYPOINTS, GIANT_PATH
from EnemyData import mob_data
from TowerLogic import Tower, ENEMY_PATHS
from MapLogic import Map
from Button import Button
from UI import *
from os.path import abspath, dirname
from TowerData import towers_base
from Achievements import unlock_achievement, check_achievements


BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + "/images/"

SCORE_FILE = "scores.json"
INSTRUCTIONS_FILE = "instructions.txt"
TOTAL_WAVE_TIME_FILE = "total_wave_time.json"

pygame.init()

#code for background music
mixer.init()

boss_scream_sound = mixer.Sound(BASE_PATH + "/sounds/bossScream.flac")
boss_battle_music = BASE_PATH + "/sounds/bossbattle.wav"

banner_font = pygame.font.Font("fonts/BrickSans.ttf", 14)


SCREEN_WIDTH = 750
SCREEN_HEIGHT = 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FINAL_WAVE = 10

IMG_NAMES = [
    "enemySample40x40",
    "mapSample",
    "witchSample",
    "cancel_button",
    "fastforwardwave",
    "archerSample",
    "bearSample",
    "slime",
]
IMAGES = {
    name: image.load(IMAGE_PATH + "{}.png".format(name)).convert_alpha()
    for name in IMG_NAMES
}


enemyImage = IMAGES["enemySample40x40"] #generate enemy image
witchImage = IMAGES["witchSample"] #generate tower image
mapSample = IMAGES["mapSample"] #generate map image
cancelImage = IMAGES["cancel_button"] #generate cancel button image
fastForwardImage = IMAGES["fastforwardwave"] #generate fast forward button image
archerImage = IMAGES["archerSample"] #generate archer tower image
bearImage = IMAGES["bearSample"] #generate bear tower image
slimeImage = IMAGES["slime"]


modes_played_global = set()
modes_won_global = set()

#Allows us to wrap the game into a .exe file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#wave helper function
def get_wave_data(wave):
    if wave == 1:
        return["Red"] * 3
    elif wave == 2:
        return["Red"] * 7
    elif wave == 3:
        return["Red"] * 3 + ["Blue"] * 3
    elif wave == 4:
        return["Blue"] * 4 + ["Purple"] * 2
    elif wave == 5:
        return["Purple"] * 3 + ["Blue"] * 2 + ["Glowing"] * 2
    elif wave == 6:
        return["Glowing"] * 2 + ["Giant"] * 1
    elif wave == 7:
        return["Blue"] * 8 + ["Purple"] * 4 + ["Glowing"] * 3
    elif wave == 8:
        return["Glowing"] * 3 + ["Purple"] * 2 + ["Glowing"] * 2 + ["Purple"] * 1 + ["Glowing"] * 1 + ["Purple"] * 3
    elif wave == 9:
        return["Giant"] * 3 + ["Red"] * 5 + ["Blue"] * 2
    elif wave == 10:
        return["Boss"] * 1
    else:
        return["Red"] * 5

def select_tower(pixel_x, pixel_y, towers):
    for tower in towers:
        if tower.x == pixel_x and tower.y == pixel_y:
            log_message("found tower")
            return tower
    return None

############################# LOGGING FUNCTIONALITY ###############################
log_messages = []
def draw_logs(screen, log_messages):
    font = pygame.font.SysFont("Arial", 13)  # Font for log messages
    y_offset = 410  # Start drawing logs near the bottom of the screen
    for message in log_messages[-5:]:  # Show only the last 5 messages
        text_surface = font.render(message, True, (255, 255, 255))  # White text
        screen.blit(text_surface, (605, y_offset))
        y_offset += 20  # Move down for the next message
        
def log_message(message):
    print(message)  # Still print to the terminal
    #message_list = message.split("\n")  # Split the message into lines
    if len(message) > 30:  # Limit the length of each line to 50 characters
        extra_message = "   " + message[27:]  # Get the extra part of the message 
        message = message[:27] + "..."  # Truncate long messages
        log_messages.append(message)  # Add the message to the log list
        log_messages.append(extra_message)  # Add the extra message to the log list
    else:
        log_messages.append(message)

    if len(log_messages) > 50:  # Limit the number of stored messages
        log_messages.pop(0)

############################## END OF LOGGING ###############################

def reset_slow_effects(enemies, speed_multiplier):
    for enemy in enemies:
        enemy.slow_effects = 0
        enemy.speed = mob_data[enemy.color]["Speed"] * speed_multiplier


def game(mode="normal"):

    mixer.music.load(BASE_PATH + "/sounds/backgroundmusic.mp3")
    mixer.music.set_volume(Settings.music_volume)
    mixer.music.play(-1) #plays music after leaving homescreen

    # score variables
    high_score = False
    top_five = False
    time_high_score = False
    time_top_five = False
    total_wave_time = 0

    # tower variables
    placing_tower = False
    towers = []  # List to store placed towers
    tower_positions = set()  # Set to store tower positions
    temporary_tower = None  # Temporary tower for placement

    # Enemy variables
    enemies = []
    spawn_delay = 800 #ms
    last_spawn_time = pygame.time.get_ticks()

    #Wave Logic
    wave_number = 1
    lives = 25  # Starting number of lives
    money = 550  # Starting amount of money
    score = 0 # Starting score amount
    current_wave_enemies = get_wave_data(wave_number) #what to spawn from current wave
    spawned_count = 0         #how many have spawned from this wave

    gameMap = Map(screen, mapSample)
    
    # Create buttons
    witchButton = Button(620, 95, IMAGES["witchSample"], True, "Witch", tooltip_text=   "Witch: \"Double, double, toil and trouble!\" The Witch Tower hurls magical fireballs at            \nenemies, making them regret stepping onto your turf. \n- \"A reliable all-rounder tower that does decent damage\"\ncost: 100\natk: 10\n") # (x, y, image, single_click, tower_name, tool_tip)
    archerButton = Button(680, 90, IMAGES["archerSample"], True, "Archer", tooltip_text="Archer: \"Bullseye!\" The Archer Tower is your go-to for precision strikes. With its rapid         \n-fire arrows, it’s perfect for thinning out waves of weaker enemies. \n- \"A fast shooting arrows tower that does less damage\" \ncost: 80 \natk: 8\n")
    bearButton = Button(620, 140, IMAGES["bearSample"], True, "Bear", tooltip_text=     "Bear: \"Rawr!\" The Bear Tower smashes enemies with brute force. It’s slow but devastating, \nperfect for taking down a group of foes. \n- \"A powerful tower that smashes the ground, dealing damage to all enemies in its range.\"\ncost: 120\natk: 25\n")
    slimeButton = Button(680, 145, IMAGES["slime"], True, "Slime", tooltip_text=        "Slime: \"Sticky situation!\" The Slime Tower slows enemies with gooey projectiles, giving    \nyour other towers more time to finish the job. Great for controlling the battlefield \n- \"A tower that slows all enemies in its range.\" \ncost: 120\natk: slow\n")
    cancelButtonScale = pygame.transform.scale(cancelImage, (60, 39.9))
    cancelButton = Button(620, 300, cancelButtonScale, True) # (x, y, image, single_click)
    
    buttons = [archerButton, bearButton, witchButton, slimeButton]

    def find_button(x, y):
        for button in buttons:
            if button.rect.collidepoint(x, y):
                return button
        return None

    fastForwardScale =  pygame.transform.scale(IMAGES["fastforwardwave"], (40, 40))
    fastForwardButton = Button(700, 300, fastForwardScale, True) # (x, y, image, single_click)

    #wave button logic
    start_wave_btn_img = pygame.image.load(IMAGE_PATH + "startwave.png").convert_alpha()
    start_wave_btn_img = pygame.transform.scale(start_wave_btn_img, (40, 40))  # Adjust size as needed
    start_wave_button = Button(700, 350, start_wave_btn_img, True)

    wave_started = False

    running = True
    show_stats = False
    show_wave = True
    towerButton = None
    fps = 60

    game_state = {
        "kills": 0,
        "wave_kills": 0,
        "waves_survived": 0,
        "boss_defeated": False,
        "lives": 25,
        "lives_lost": 0,
        "towers_placed": 0,
        "gold": 0,
        "upgrades_used": 0,
        "towers_sold": 0,
        "towers_sold_this_wave": 0,
        "tower_types": set(),
        "one_life_remaining": False,
        "no_upgrades_wave": True,
        "start_money": 0,  # used to check Last Cent
        "witch_dmg_this_wave": 0,  # used for Witching Hour
        "archer_wave_kills": 0,  # used for Sniper
        "wave_started": False,
        "game_won": False,
        "sold_mid_wave": False,
        "wave_completed": False,
        "wave": 0,
        "maxed_towers": 0,
        "one_tower_challenge": False,
        "tower_type_counts": {"Witch": 0, "Archer": 0, "Bear": 0, "Slime": 0},
        "mode": mode,
        "fast_forward_used": False,
        "paused_game": False,
        "game_over": False,
        "lives_lost_per_wave": [],
        "lives_lost_at_start": 0,
        "tower_positions": [],
        "reverse_sweep_failed": False,
        "pre_wave_4_kills": 0,
        "lives_lost_after_wave3": 0,
        "modes_played": set(),
        "modes_won": set(),

    }

    achievement_notifications = []  # holds (achievement_name, timestamp)

    if mode != "normal":
        game_state["modes_played"].add(mode)
        modes_played_global.add(mode)

    check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)

    if mode == "hardcore_mode":
        lives = 1
        money = 350
        game_state["lives"] = lives

    

    speed_multiplier = 1
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press 'ESC' to pause
                    game_state["paused_game"] = True
                    while True:
                        result = settings_screen(screen, in_game = True) # the homebutton appears during game
                        if result == "achievements":
                            achievements_screen(screen, achievements)
                            continue  # return to settings after closing achievements
                        elif result == "home":
                            return  # exit to home
                        elif result is None:
                            break  # exit settings

            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if show_stats and selected_tower:
                    if upgrade_button_rect.collidepoint(event.pos):
                        log_message("Upgrade button clicked!")

                        if selected_tower.upgrade == 3:
                            log_message("Tower is already at max upgrade!")

                        elif mode == "no_upgrades_mode":
                            log_message("Upgrades are disabled in No Upgrades Mode!")

                        elif money >= int(towers_base[selected_tower.tower_name]["upgrades"][selected_tower.upgrade + 1]["cost"] * (1.5 if mode == "hardcore_mode" else 1)):
                            cost = int(towers_base[selected_tower.tower_name]["upgrades"][selected_tower.upgrade + 1]["cost"] * (1.5 if mode == "hardcore_mode" else 1))
                            money -= cost
                            selected_tower.do_upgrade(game_state)
                            game_state["upgrades_used"] += 1
                            game_state["no_upgrades_wave"] = False
                            check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)

                        else:
                            log_message("Not enough money to upgrade tower!")

                    elif sell_button_rect.collidepoint(event.pos):
                        log_message("Sell button clicked!")
                        
                        total_cost = selected_tower.cost  # Base cost of the tower
                        for i in range(1, selected_tower.upgrade + 1):  # Add the cost of each applied upgrade
                            total_cost += towers_base[selected_tower.tower_name]["upgrades"][i]["cost"]

                        # Refund 50% of the tower's cost
                        money += total_cost // 2  # adjust if you want different refund percentage
                        log_message(f"Refunded: {total_cost // 2}")

                        towers.remove(selected_tower)  # Remove the tower from the list
                        game_state["towers_sold"] += 1
                        game_state["towers_sold_this_wave"] += 1
                        if wave_started:
                            game_state["sold_mid_wave"] = True
                        check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)

                        tower_positions.remove((selected_tower.x, selected_tower.y))  # Free up the position
                        selected_tower = None  # Deselect the tower
                        show_stats = False  # Hide the stats screen
                    elif not (600 <= event.pos[0] <= 750):  # Check if click is outside the sidebar
                        log_message("Clicked outside the sidebar, exiting stats screen.")
                        show_stats = False
                        selected_tower = None
                    
                elif start_wave_button.draw(screen):
                    if not wave_started:
                        wave_started = True
                        
                        log_message("Wave started!")
                        wave_start_time = pygame.time.get_ticks()
                        game_state["wave_completed"] = False
                        game_state["start_money"] = money
                        check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)
                elif fastForwardButton.draw(screen):
                    if fps == 60:
                        fps = 120
                        game_state["fast_forward_used"] = True
                        speed_multiplier = 2
                        spawn_delay = 400  # Reduce spawn delay for fast forward
                        for enemy in enemies:
                            enemy.speed *= speed_multiplier # increase speed
                            #log_message(f"Enemy speed: {enemy.speed}")
                        log_message("Fast forward activated!")
                    else:
                        fps = 60
                        speed_multiplier = 1
                        spawn_delay = 800  # Reset spawn delay
                        for enemy in enemies:
                            enemy.speed /= 2 # normal speed
                            #log_message(f"Enemy speed: {enemy.speed}")
                        log_message("Fast forward deactivated!")

                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // 40 * 40
                    grid_y = mouse_y // 40 * 40
                    if mouse_x > 600 or mouse_y > 400:
                        log_message("Clicked on sidebar")
                        #log_message(f"soundtrack volume: {Settings.music_volume}")
                        #log_message(f"sound effects volume: {Settings.sfx_volume}")
                    else:
                        selected_tower = select_tower(grid_x, grid_y, towers)
                        if selected_tower:
                            log_message(f"Selected Tower at ({grid_x}, {grid_y})")
                            show_stats = True
                            show_range = True
                        else:
                            show_stats = False
                            selected_tower = None

            ############################## HANDLE PLACING TOWERS ##############################
                if placing_tower and temporary_tower:
                    # Place the tower on the map
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // 40 * 40
                    grid_y = mouse_y // 40 * 40
                    

                    if mouse_x < 600 and mouse_y < 400:  # Ensure placement is within the map area
                        if (grid_x, grid_y) not in tower_positions and (grid_x, grid_y) not in ENEMY_PATHS:  # Check if the position is free
                            # check if the player has enough money to place the tower
                            if money >= temporary_tower.cost:
                                money -= temporary_tower.cost  
                                log_message(f"Placing tower at: ({grid_x}, {grid_y})")
                                
                                towers.append(Tower(grid_x, grid_y, screen, temporary_tower.tower_name, game_state))
                                tower_positions.add((grid_x, grid_y))  # Mark the position as occupied
                                game_state["tower_positions"].append((grid_x, grid_y))
                                placing_tower = False
                                temporary_tower = None
                                game_state["towers_placed"] += 1
                                game_state["tower_types"] = {tower.tower_name for tower in towers}
                                game_state["tower_types"].add(towerButton.name)
                                tower_type = towerButton.name
                                game_state["tower_type_counts"][tower_type] += 1
                                check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)

                            else:
                                log_message("Not enough money to place tower!")
                elif not show_stats and find_button(mouse_x, mouse_y):
                    # Start placing a tower
                    towerButton = find_button(mouse_x, mouse_y)
                    placing_tower = True
                    log_message(towerButton.name)
                    temporary_tower = Tower(0, 0, screen, towerButton.name, game_state)
                elif cancelButton.draw(screen):
                    # Cancel tower placement
                    placing_tower = False
                    temporary_tower = None

            elif event.type == pygame.MOUSEMOTION and placing_tower:
                # Update the position of the temporary tower to follow the mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if temporary_tower:
                    temporary_tower.x = mouse_x // 40 * 40
                    temporary_tower.y = mouse_y // 40 * 40
 
            ############################### END OF TOWER PLACEMENT CODE ########################################
            
        current_time = pygame.time.get_ticks()
        if wave_started and spawned_count < len(current_wave_enemies):
            if current_time - last_spawn_time >= spawn_delay:
                color = current_wave_enemies[spawned_count]

                # Determine path based on mode
                if color in ["Giant", "Boss"]:
                    path = list(reversed(GIANT_PATH)) if mode == "reverse_mode" else GIANT_PATH
                else:
                    path = list(reversed(WAYPOINTS)) if mode == "reverse_mode" else WAYPOINTS

                if color == "Giant":
                    new_enemy = Enemy(
                        path[0][0], path[0][1], screen, color, waypoints=path
                    )
                elif color == "Boss":
                    new_enemy = Enemy(
                        path[0][0], path[0][1], screen, color,
                        waypoints=path,
                        scream_sound=boss_scream_sound,
                        boss_music=boss_battle_music
                    )
                else:
                    new_enemy = Enemy(
                        path[0][0], path[0][1], screen, color, waypoints=path
                    )

                enemies.append(new_enemy)
                spawned_count += 1
                last_spawn_time = current_time


        # DRAWING CODE
        screen.fill((0, 0, 0))
        gameMap.draw()
        draw_grid(screen)        

        reset_slow_effects(enemies, speed_multiplier)
        # Draw all placed towers and call attack
        for tower in towers:
            if show_stats and selected_tower and tower == selected_tower:
                tower.draw(True)
            else:
                tower.draw(False)
            Tower.attack(tower, enemies, fps)
            Tower.update_animation(tower, fps)

            for enemy in enemies:
                if enemy.slow_effects > 0:
                    enemy.speed = mob_data[enemy.color]["Speed"] / 2 * speed_multiplier

            #Tower.update(tower)

        # Draw the temporary tower if placing
        if placing_tower and temporary_tower:
            temporary_tower.draw(True)

        # enemy loop
        for enemy in enemies[:]:
            if not enemy.reached_end:
                enemy.update()
                if enemy.hp <= 0 and enemy.death_animation_done:
                    enemies.remove(enemy)
                    money += enemy.money
                    score += enemy.score
                    game_state["kills"] += 1
                    game_state["wave_kills"] += 1

                    if wave_number <= 3:
                        game_state["pre_wave_4_kills"] += 1
                    if enemy.killed_by == "Archer":
                        game_state["archer_wave_kills"] += 1
                    check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)

            else:
                lives -= enemy.dmg
                enemies.remove(enemy)
                game_state["lives"] = lives
                game_state["lives_lost"] += enemy.dmg

                if wave_number > 3:
                    game_state["lives_lost_after_wave3"] += enemy.dmg

                if lives == 1:
                    game_state["one_life_remaining"] = True
                money += enemy.money  # increase money if enemy reaches end
                score -= enemy.score
                if lives <= 0:
                    game_state["game_over"] = True
                    check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)

                    if (get_top_score(SCORE_FILE, "score") < score): 
                        high_score = True
                    elif (is_top_five(SCORE_FILE, score, "score")):
                        top_five = True
                    log_message(f"score updated {update_scores(SCORE_FILE, score, "score")}")
                    result = gameover_screen(screen, score, SCORE_FILE, high_score, top_five)

                    if result == "restart":
                        log_message("Restarting game...")
                        game()
                        return
                    elif result == "home":
                        log_message("Returning home...")
                        mixer.music.stop()
                        main()
                        return
                    else:
                        running = False

            enemy.draw()

            if getattr(enemy, "is_boss", False):
                draw_boss_health_bar(screen, enemy)
                break  # Only one boss expected at a time

        # end enemy loop
        if not enemies and spawned_count == len(current_wave_enemies):
            if wave_number == FINAL_WAVE: # game clear after 10 wave
                # accounting final wave's points and time
                wave_end_time = pygame.time.get_ticks()
                log_message(f"It took {((wave_end_time-wave_start_time)/1000):.3f} seconds to beat the wave")
                log_message(f"Time increases your score by {((wave_number**3) * (200/((wave_end_time-wave_start_time)/1000))):3f}")
                score += int(((wave_number**3) * (200/((wave_end_time-wave_start_time)/1000)))) #The faster you beat the wave the more points you get
                total_wave_time += ((wave_end_time-wave_start_time)/1000) #Add time it took to beat the wave to the total time
                total_wave_time = round(total_wave_time, 2)

                # bonus points
                log_message(f"Money increase score by: {money*2}")
                score += (money*2) # winning with extra money adds to your score
                log_message(f"Lives increases score by: {lives*500}")
                score += (lives*500) # winning with extra lives adds to your score
                # lets you know relative leaderboard positioning
                if (get_top_score(SCORE_FILE, "score") < score): 
                    high_score = True
                elif (is_top_five(SCORE_FILE, score, "score")):
                    top_five = True
                if (get_top_score(TOTAL_WAVE_TIME_FILE, "time") > total_wave_time): 
                    time_high_score = True
                elif (is_top_five(TOTAL_WAVE_TIME_FILE, total_wave_time, "time")):
                    time_top_five = True

                # final score and time messaging
                log_message(f"Final score is {score}")
                log_message(f"Score updated {update_scores(SCORE_FILE, score, "score")}")
                log_message(f"Final win time is {total_wave_time}")
                log_message(f"Time score updated{update_scores(TOTAL_WAVE_TIME_FILE, total_wave_time, "time")}")

                game_state["gold"] = money
                game_state["game_won"] = True

                if mode != "normal":
                    game_state["modes_won"].add(mode)
                    modes_won_global.add(mode)

                game_state["lives"] = lives
                if getattr(enemy, "is_boss", False) and enemy.hp <= 0 and not game_state["boss_defeated"]:
                    game_state["boss_defeated"] = True

                print("[DEBUG] Final Lives:", game_state["lives"])
                print("[DEBUG] Game Won:", game_state["game_won"])

                check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)
                gameclear_screen(screen, score, SCORE_FILE, high_score, top_five, total_wave_time, time_high_score, time_top_five)
                
                mixer.music.stop()
                main()  # restart from homescreen
                return
            else:
                lives_lost_this_wave = game_state["lives_lost"] - game_state["lives_lost_at_start"]
                game_state["lives_lost_per_wave"].append(lives_lost_this_wave)
                game_state["lives_lost_at_start"] = game_state["lives_lost"]
                
                wave_end_time = pygame.time.get_ticks()
                wave_number += 1
                game_state["wave"] = wave_number
                game_state["wave_completed"] = True
                if len(towers) == 1:
                    game_state["one_tower_challenge"] = True
                else:
                    game_state["one_tower_challenge"] = False

                game_state["waves_survived"] += 1
                check_achievements(game_state, achievement_notifications, modes_played_global, modes_won_global)
                game_state["towers_sold_this_wave"] = 0
                game_state["archer_wave_kills"] = 0
                game_state["witch_dmg_this_wave"] = 0
                game_state["tower_types"] = set()
                game_state["no_upgrades_wave"] = True

                current_wave_enemies = get_wave_data(wave_number)
                spawned_count = 0
                last_spawn_time = pygame.time.get_ticks()  # Reset spawn timer
                money += 10 * wave_number
                log_message(f"It took {((wave_end_time-wave_start_time)/1000):.3f} seconds to beat the wave")
                log_message(f"Time increases your score by {((wave_number**3) * (200/((wave_end_time-wave_start_time)/1000))):.3f}")
                score += int(((wave_number**3) * (200/((wave_end_time-wave_start_time)/1000)))) #The faster you beat the wave the more points you get
                total_wave_time += ((wave_end_time-wave_start_time)/1000) #Add time it took to beat the wave to the total time

                wave_started = False
                game_state["wave_kills"] = 0

        draw_sidebar(screen, lives, money) # makes enemy go behind sidebar instead of overtop it
        draw_underbar(screen, SCORE_FILE, score)

        # Wave descripion code
        font = pygame.font.Font("fonts/BrickSans.ttf", 10)
        wave_description_text = wave_description(wave_number)
        lines = wave_description_text.split("\n")
        y_offset = 405  # Starting y position for the text
        for line in lines:
            waveDes = font.render(line, True, (255, 255, 255))
            screen.blit(waveDes, (10, y_offset))  # Draw each line
            y_offset += 15  # Move down for the next line

        draw_logs(screen, log_messages)


        # Draw buttons
        if not show_stats and towerButton and towerButton.draw(screen): # if tower button is clicked
            placing_tower = True
        if placing_tower == True:
            if cancelButton.draw(screen):
                placing_tower = False
                
        fastForwardButton.draw(screen) # draw fast forward button

        if not wave_started: #only appears when wave hasnt started yet
            start_wave_button.draw(screen)
            

         

        for button in buttons:
            button.draw(screen, show_stats)  

        if show_stats and selected_tower:
            upgrade_button_rect, sell_button_rect = draw_tower_stat(screen, selected_tower, mode)

        if show_wave:
            number_wave(screen, wave_number)

        
        #Show mouse position on screen (for debugging waypoints)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.SysFont("Arial", 14)
        pos_text = font.render(f"({mouse_x}, {mouse_y})", True, (200, 200, 200))
        screen.blit(pos_text, (10, 10))

        # Show unlocked achievements for 3 seconds
        # === Styled achievement banner display ===
        banner_height = 40
        banner_width = 400
        padding = 10

        now = pygame.time.get_ticks()
        achievement_notifications = [
            (name, ts) for name, ts in achievement_notifications if now - ts < 3000
        ]

        for i, (name, ts) in enumerate(achievement_notifications):
            banner_x = 10
            banner_y = 10 + i * (banner_height + 10)

            if name == "Master Defender":
                # Unique background and border for the platinum trophy
                bg_color = (180, 145, 255)    # Soft purple glow
                border_color = (255, 255, 255)  # White border
                text_color = (255, 255, 255)
                icon = "👑"
            else:
                # Default style
                bg_color = (255, 68, 58)
                border_color = (61, 43, 36)
                text_color = (239, 176, 125)
                icon = "🏆"

            pygame.draw.rect(screen, bg_color, (banner_x, banner_y, banner_width, banner_height), border_radius=8)
            pygame.draw.rect(screen, border_color, (banner_x, banner_y, banner_width, banner_height), 2, border_radius=8)

            text_surface = banner_font.render(f"{icon} Achievement Unlocked: {name}", True, text_color)
            screen.blit(text_surface, (banner_x + padding, banner_y + padding // 2))

        if mode != "normal":
            mode_font = pygame.font.Font("fonts/BrickSans.ttf", 16)
            mode_text = mode_font.render(f"Mode: {mode.replace('_', ' ').title()}", True, (239, 176, 125))
            pygame.draw.rect(screen, (255, 68, 58), (5, 520, mode_text.get_width() + 16, 30), border_radius=8)
            pygame.draw.rect(screen, (61, 43, 36), (5, 520, mode_text.get_width() + 16, 30), 2, border_radius=8)
            screen.blit(mode_text, (13, 523))




        pygame.display.flip()

        clock.tick(60) # Control the frame rate / speed of the game

    mixer.music.stop()
    pygame.quit()

def main():

    valid_modes = ["normal_mode", "no_upgrades_mode", "hardcore_mode", "reverse_mode"]

    while True:
        result = homescreen(screen)
        if result == "play":
            selected_mode = mode_selection_screen(screen)
            if selected_mode in valid_modes:
                game(selected_mode)
        elif result == "settings":
            setting_result = settings_screen(screen, in_game = False) # home button dissappears in main menu
            if setting_result == "achievements":
                achievements_screen(screen, achievements)
            elif setting_result == "home":
                continue 
        elif result == "leaderboard":
            leaderboard_screen(screen, SCORE_FILE, TOTAL_WAVE_TIME_FILE)
        elif result == "information":
            instructions_screen(screen, INSTRUCTIONS_FILE)
        elif result == "achievements":
            achievements_screen(screen, achievements)
        elif result == "modeSelection":
            mode_selection_screen(screen)


if __name__ == "__main__":
    main()
