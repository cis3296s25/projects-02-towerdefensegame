import pygame
import os #required for .exe creation
import sys #required for .exe creation
import random
from pygame import(
    image,
    mixer,
)
from EnemyLogic import Enemy, WAYPOINTS, GIANT_PATH
from TowerLogic import Tower, ENEMY_PATHS
from MapLogic import Map
from Button import Button
from UI import homescreen, pause_screen, draw_sidebar, draw_grid, gameover_screen, draw_tower_stat, number_wave, gameclear_screen, draw_boss_health_bar
from os.path import abspath, dirname
from TowerData import towers_base

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + "/images/"

pygame.init()

#code for background music
mixer.init()
mixer.music.load(BASE_PATH + "/sounds/backgroundmusic.mp3")
mixer.music.set_volume(0.5)

boss_scream_sound = mixer.Sound(BASE_PATH + "/sounds/bossScream.flac")
boss_battle_music = BASE_PATH + "/sounds/bossbattle.wav"



SCREEN_WIDTH = 750
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FINAL_WAVE = 10

IMG_NAMES = [
    "enemySample40x40",
    "mapSample",
    "witchSample",
    "cancel_button",
    "fastForward",
    "archerSample",
    "bearSample",
]
IMAGES = {
    name: image.load(IMAGE_PATH + "{}.png".format(name)).convert_alpha()
    for name in IMG_NAMES
}


enemyImage = IMAGES["enemySample40x40"] #generate enemy image
witchImage = IMAGES["witchSample"] #generate tower image
mapSample = IMAGES["mapSample"] #generate map image
cancelImage = IMAGES["cancel_button"] #generate cancel button image
fastForwardImage = IMAGES["fastForward"] #generate fast forward button image
archerImage = IMAGES["archerSample"] #generate archer tower image
bearImage = IMAGES["bearSample"] #generate bear tower image

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
            print("found tower")
            return tower
    return None

def game():
    mixer.music.play(-1) #plays music after leaving homescreen

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
    current_wave_enemies = get_wave_data(wave_number) #what to spawn from current wave
    spawned_count = 0         #how many have spawned from this wave

    gameMap = Map(screen, mapSample)
    
    # Create buttons
    witchButton = Button(620, 95, IMAGES["witchSample"], True, "Witch", tooltip_text="Witch\n cost: 100\n atk: 10") # (x, y, image, single_click, tower_name, tool_tip)
    archerButton = Button(680, 95, IMAGES["archerSample"], True, "Archer", tooltip_text="Archer\n cost: 80\n atk: 8")
    bearButton = Button(620, 140, IMAGES["bearSample"], True, "Bear", tooltip_text="Bear\n cost: 100\n atk: 50")
    cancelButtonScale = pygame.transform.scale(cancelImage, (60, 39.9))
    cancelButton = Button(620, 300, cancelButtonScale, True) # (x, y, image, single_click)
    
    buttons = [archerButton, bearButton, witchButton]

    def find_button(x, y):
        for button in buttons:
            if button.rect.collidepoint(x, y):
                return button
        return None

    fastForwardScale =  pygame.transform.scale(IMAGES["fastForward"], (40, 40))
    fastForwardButton = Button(700, 300, fastForwardScale, True) # (x, y, image, single_click)
    

    #wave button logic
    start_wave_btn_img = pygame.image.load(IMAGE_PATH + "startwave.png").convert_alpha()
    start_wave_btn_img = pygame.transform.scale(start_wave_btn_img, (40, 40))  # Adjust size as needed
    start_wave_button = Button(700, 350, start_wave_btn_img, True)

    wave_started = False
    

    # Load and scale speaker icons
    speaker_img_muted = pygame.transform.scale(
        pygame.image.load(IMAGE_PATH + "mute.png").convert_alpha(), (24, 24)
    )
    speaker_img_low = pygame.transform.scale(
        pygame.image.load(IMAGE_PATH + "low-volume.png").convert_alpha(), (24, 24)
    )
    speaker_img_medium = pygame.transform.scale(
        pygame.image.load(IMAGE_PATH + "medium-volume.png").convert_alpha(), (24, 24)
    )
    speaker_img_high = pygame.transform.scale(
        pygame.image.load(IMAGE_PATH + "high-volume.png").convert_alpha(), (24, 24)
    )

    # Volume/mute state
    muted = False
    volume = 0.1
    mixer.music.set_volume(volume)

    # Volume slider setup (placed inside sidebar area)
    slider_rect = pygame.Rect(20, screen.get_height() - 40, 100, 10)
    handle_rect = pygame.Rect(slider_rect.x + int(slider_rect.width * volume) - 5, slider_rect.y - 5, 10, 20)
    dragging_volume = False

    # Placeholder for speaker icon rect (will be updated dynamically)
    speaker_rect = pygame.Rect(0, 0, 24, 24)  # placeholder; will update dynamically below

    running = True
    show_stats = False
    show_wave = True
    towerButton = None
    fps = 60
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press 'ESC' to pause
                    pause_screen(screen, mixer)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_rect.collidepoint(event.pos):
                    dragging_volume = True
                elif speaker_rect.collidepoint(event.pos):
                    muted = not muted
                    mixer.music.set_volume(0 if muted else volume)
                elif show_stats and selected_tower and upgrade_button_rect.collidepoint(event.pos):
                    print("Upgrade button clicked!")
                    if selected_tower.upgrade == 3:
                        print("Tower is already at max upgrade!")
                    elif money >= towers_base[selected_tower.tower_name]["upgrades"][selected_tower.upgrade + 1]["cost"] and selected_tower.upgrade < 3:
                        money -= towers_base[selected_tower.tower_name]["upgrades"][selected_tower.upgrade + 1]["cost"]
                        selected_tower.do_upgrade()
                    elif money <= towers_base[selected_tower.tower_name]["upgrades"][selected_tower.upgrade + 1]["cost"] and selected_tower.upgrade < 3: 
                        print("Not enough money to upgrade tower!")
                    
                elif start_wave_button.draw(screen):
                    if not wave_started:
                        wave_started = True
                        print("Wave started!")
                elif fastForwardButton.draw(screen):
                    if fps == 60:
                        fps = 120
                        print("Fast forward activated!")
                    else:
                        fps = 60
                        print("Fast forward deactivated!")

                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // 40 * 40
                    grid_y = mouse_y // 40 * 40
                    if mouse_x > 600:
                        print("Clicked on sidebar")
                    else:   
                        selected_tower = select_tower(grid_x, grid_y, towers)
                        if selected_tower:
                            print(f"Selected Tower at ({grid_x}, {grid_y})")
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
                    

                    if mouse_x < 600:  # Ensure placement is within the map area
                        if (grid_x, grid_y) not in tower_positions and (grid_x, grid_y) not in ENEMY_PATHS:  # Check if the position is free
                            # check if the player has enough money to place the tower
                            if money >= temporary_tower.cost:
                                money -= temporary_tower.cost  
                                print(f"Placing tower at: ({grid_x}, {grid_y})")
                                
                                towers.append(Tower(grid_x, grid_y, screen, temporary_tower.tower_name))
                                tower_positions.add((grid_x, grid_y))  # Mark the position as occupied
                                placing_tower = False
                                temporary_tower = None
                            else:
                                print("Not enough money to place tower!")
                elif not show_stats and find_button(mouse_x, mouse_y):
                    # Start placing a tower
                    towerButton = find_button(mouse_x, mouse_y)
                    placing_tower = True
                    print(towerButton.name)
                    temporary_tower = Tower(0, 0, screen, towerButton.name)
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

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_volume = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_volume:
                    mouse_x = event.pos[0]
                    new_volume = max(0, min(1, (mouse_x - slider_rect.x) / slider_rect.width))
                    volume = new_volume
                    if not muted:
                        mixer.music.set_volume(volume)
                    handle_rect.x = slider_rect.x + int(slider_rect.width * volume) - 5

        current_time = pygame.time.get_ticks()

        if wave_started and spawned_count < len(current_wave_enemies):
            if current_time - last_spawn_time >= spawn_delay:
                color = current_wave_enemies[spawned_count]
                if color == "Giant":
                    new_enemy = Enemy(
                        GIANT_PATH[0][0], GIANT_PATH[0][1], screen, color, waypoints=GIANT_PATH
                    )
                elif color == "Boss":
                    new_enemy = Enemy(
                        GIANT_PATH[0][0], 
                        GIANT_PATH[0][1], 
                        screen, 
                        color, 
                        waypoints=GIANT_PATH, 
                        scream_sound = boss_scream_sound, 
                        boss_music=boss_battle_music
                    )
                else:
                    new_enemy = Enemy(
                        WAYPOINTS[0][0], WAYPOINTS[0][1], screen, color
            )
                enemies.append(new_enemy)
                spawned_count += 1
                last_spawn_time = current_time

        # DRAWING CODE
        screen.fill((0, 0, 0))
        gameMap.draw()
        draw_grid(screen)

        # Draw all placed towers and call attack
        for tower in towers:
            if show_stats and selected_tower and tower == selected_tower:
                tower.draw(True)
            else:
                tower.draw(False)
            Tower.attack(tower, enemies, fps)
            Tower.update_animation(tower, fps)

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
            else:
                lives -= enemy.dmg
                enemies.remove(enemy)
                money += enemy.money  # increase money if enemy reaches end
                if lives <= 0:
                    if gameover_screen(screen) == "restart":
                        print("Restarting game...")
                        game()
                    else:
                        running = False
                        break

            enemy.draw()

            if getattr(enemy, "is_boss", False):
                draw_boss_health_bar(screen, enemy)
                break  # Only one boss expected at a time
        # end enemy loop
        
        if not enemies and spawned_count == len(current_wave_enemies):
            if wave_number == FINAL_WAVE: # game clear after 5 wave
                gameclear_screen(screen)
                mixer.music.stop()

                main()  # restart from homescreen
                return
            else:
                wave_number += 1
                current_wave_enemies = get_wave_data(wave_number)
                spawned_count = 0
                last_spawn_time = pygame.time.get_ticks()  # Reset spawn timer
                money += 10 * wave_number
                wave_started = False

        draw_sidebar(screen, lives, money) # makes enemy go behind sidebar instead of overtop it

        # Draw buttons
        if not show_stats and towerButton and towerButton.draw(screen): # if tower button is clicked
            placing_tower = True
        if placing_tower == True:
            if cancelButton.draw(screen):
                placing_tower = False
                
        fastForwardButton.draw(screen) # draw fast forward button

        if not wave_started: #only appears when wave hasnt started yet
            start_wave_button.draw(screen)

         # Volume slider bar
        pygame.draw.rect(screen, (200, 200, 200), slider_rect)  # Bar background
        pygame.draw.rect(screen, (100, 100, 255), (slider_rect.x, slider_rect.y, int(slider_rect.width * volume), slider_rect.height))  # Volume fill
        pygame.draw.rect(screen, (255, 255, 255), handle_rect)  # Slider handle

        # Choose which speaker icon to display
        if muted:
            speaker_img = speaker_img_muted
        elif volume <= 0.33:
            speaker_img = speaker_img_low
        elif volume <= 0.66:
            speaker_img = speaker_img_medium
        else:
            speaker_img = speaker_img_high

        # Position speaker icon next to slider
        speaker_rect = speaker_img.get_rect(topleft=(slider_rect.x + slider_rect.width + 10, slider_rect.y - 6))
        screen.blit(speaker_img, speaker_rect)

        for button in buttons:
            button.draw(screen)  

        if show_stats and selected_tower:
            upgrade_button_rect = draw_tower_stat(screen, selected_tower)

        if show_wave:
            number_wave(screen, wave_number)

        if not muted:
            mixer.music.set_volume(volume)
        else:
            mixer.music.set_volume(0)
        
        #Show mouse position on screen (for debugging waypoints)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.SysFont("Arial", 14)
        pos_text = font.render(f"({mouse_x}, {mouse_y})", True, (200, 200, 200))
        screen.blit(pos_text, (10, 10))

        pygame.display.flip()
        clock.tick(fps) # Control the frame rate / speed of the game

    mixer.music.stop()
    pygame.quit()

def main():
    homescreen(screen)  # Show the home screen at the start
    game() # now when play button is clicked, takes you to the game

if __name__ == "__main__":
    main()
