import pygame
import os #required for .exe creation
import sys #required for .exe creation
import random
from pygame import(
    image,
    mixer,
)
from EnemyLogic import Enemy, WAYPOINTS
from TowerLogic import Tower, ENEMY_PATHS
from MapLogic import Map
from Button import Button
from UI import homescreen, pause_screen, draw_sidebar, draw_grid, gameover_screen, draw_tower_stat, number_wave
from os.path import abspath, dirname

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + "/images/"

pygame.init()

#code for background music
mixer.init()
mixer.music.load(BASE_PATH + "/sounds/backgroundmusic.mp3")
mixer.music.set_volume(0.5)


SCREEN_WIDTH = 750
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

IMG_NAMES = [
    "enemySample40x40",
    "mapSample",
    "towerSample",
    "cancel_button",
]
IMAGES = {
    name: image.load(IMAGE_PATH + "{}.png".format(name)).convert_alpha()
    for name in IMG_NAMES
}
enemyImage = IMAGES["enemySample40x40"] #generate enemy image
towerImage = IMAGES["towerSample"] #generate tower image
mapSample = IMAGES["mapSample"] #generate map image
cancelImage = IMAGES["cancel_button"] #generate cancel button image

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
        return["Red"] * 1
    elif wave == 2:
        return["Red"] * 10
    elif wave == 3:
        return["Red"] * 2 + ["Blue"] * 2 + ["Purple"] * 2 + ["Glowing"] * 2
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

    # Initialize objects
    tower = Tower(160, 160, 100, 10, 2, screen, towerImage) # (x, y, range, damage, cooldown, screen, image)
    enemy = Enemy(WAYPOINTS[0][0], WAYPOINTS[0][1], 50, 10, 5, 3, screen) # (x, y, hp, attack_range, dmg, cooldown, screen, money)

    # Enemy variables
    enemies = []
    spawn_delay = 2000 #ms
    last_spawn_time = pygame.time.get_ticks()

    #Wave Logic
    wave_number = 1
    lives = 100  # Starting number of lives
    money = 0  # Starting amount of money
    current_wave_enemies = get_wave_data(wave_number) #what to spawn from current wave
    spawned_count = 0         #how many have spawned from this wave

    gameMap = Map(screen, mapSample)
    
    # Create buttons
    towerButton = Button(610, 90, IMAGES["towerSample"], True) # (x, y, image, single_click)
    cancelButton = Button(610, 120, IMAGES["cancel_button"], True) # (x, y, image, single_click)
    
    

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
    volume = 0.5
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
                else: 
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // 40 * 40
                    grid_y = mouse_y // 40 * 40
                    selected_tower = select_tower(grid_x, grid_y, towers)  
                    if selected_tower:
                        print(f"Selected Tower at ({grid_x}, {grid_y})")
                        show_stats = True
                        show_range = True
                    
                        
                    
            ############################## HANDLE PLACING TOWERS ##############################
                if placing_tower:
                    # Place the tower on the map
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // 40 * 40
                    grid_y = mouse_y // 40 * 40
                    

                    if mouse_x < 600:  # Ensure placement is within the map area
                        if (grid_x, grid_y) not in tower_positions and (grid_x, grid_y) not in ENEMY_PATHS:  # Check if the position is free
                            print(f"Placing tower at: ({grid_x}, {grid_y})")
                            
                            towers.append(Tower(grid_x, grid_y, 100, 10, 2, screen, towerImage))
                            tower_positions.add((grid_x, grid_y))  # Mark the position as occupied
                            placing_tower = False
                            temporary_tower = None
                elif towerButton.draw(screen):
                    # Start placing a tower
                    placing_tower = True
                    temporary_tower = Tower(0, 0, 100, 10, 2, screen, towerImage)
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

        if spawned_count < len(current_wave_enemies):
            if current_time - last_spawn_time >= spawn_delay:
                color = current_wave_enemies[spawned_count]
                new_enemy = Enemy(WAYPOINTS[0][0], WAYPOINTS[0][1], 50, 10, 5, 3, screen, color)
                enemies.append(new_enemy)
                spawned_count += 1
                last_spawn_time = current_time

        # DRAWING CODE
        screen.fill((0, 0, 0))
        gameMap.draw()
        draw_grid(screen)

        # Draw all placed towers
        for tower in towers:
            tower.draw(False)

        # Draw the temporary tower if placing
        if placing_tower and temporary_tower:
            temporary_tower.draw(True)

        for enemy in enemies[:]:
            if enemy.is_dying:
                print(f"Enemy {enemy} is dying... Frame: {enemy.death_frame_index}/{len(enemy.death_frames)}")
                #play death animation
                enemy.frame_timer += 1
                if enemy.frame_timer % 10 == 0:
                    enemy.death_frame_index += 1
                    if enemy.death_frame_index < len(enemy.death_frames):
                        enemy.image = enemy.death_frames[enemy.death_frame_index]
                    else:
                        print(f"Enemy {enemy} death animation completed. Removing enemy.")
                        enemies.remove(enemy)  # Remove the enemy from the list
                        enemy.death_frame_index = 0  # Reset the death frame index
                        enemy.frame_timer = 0  # Reset the frame timer
                        enemy.death_animation_done = False  # Reset the death animation flag
                        enemy.is_dying = False  # Stop the death animation from looping
                        print(f"Enemy {enemy} removed.")

            elif not enemy.reached_end:
                enemy.move()

            else:
                # Enemy reached the end – reduce lives and remove the enemy
                lives -= enemy.dmg
                enemies.remove(enemy)

                if lives <= 0:
                    if gameover_screen(screen) == "restart":
                        print("Restarting game...")
                        game()
                    else:
                        running = False
                        break


            enemy.draw()
        for enemy in enemies:
            for tower in towers:
                # only attacks if enemy is alive
                if Tower.attack(tower, enemy):
                    enemy.hp -= tower.damage
                    if enemy.hp <= 0:
                        enemy.is_dying = True
                        enemy.frame_timer = 0
                        enemy.death_frame_index = 0
                        money += enemy.money
        
        if not enemies and spawned_count == len(current_wave_enemies):
            wave_number += 1
            current_wave_enemies = get_wave_data(wave_number)
            spawned_count = 0
            last_spawn_time = pygame.time.get_ticks()  # Reset spawn timer
            money += 10 * wave_number
                        

        draw_sidebar(screen, lives, money) # makes enemy go behind sidebar instead of overtop it

        # Draw buttons
        if towerButton.draw(screen): # if tower button is clicked
            placing_tower = True
        if placing_tower == True:
            if cancelButton.draw(screen):
                placing_tower = False

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

        if show_stats and selected_tower:
            draw_tower_stat(screen, tower)
            selected_tower.draw(True)  

        if show_wave: 
            number_wave(screen, wave_number)

    
            
        
        pygame.display.flip()
        clock.tick(60)

    mixer.music.stop()
    pygame.quit()

def main():
    homescreen(screen)  # Show the home screen at the start
    waiting_for_input = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Wait for SPACE key press to start the game
                    waiting_for_input = False
                    game()  # Start the game loop

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Wait for mouse click to start the game (optional)
                    waiting_for_input = False
                    game()  # Start the game loop

if __name__ == "__main__":
    main()
