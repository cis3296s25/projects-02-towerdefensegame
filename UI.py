import pygame
import sys #required for .exe creation
import random
from pygame import mixer
import os

from TowerData import towers_base

class Spore:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.radius = random.randint(1, 3)
        self.speed_y = random.uniform(0.1, 0.5)
        self.alpha = random.randint(100, 200)

    def update(self):
        self.y += self.speed_y
        if self.y > 400:
            self.y = 0
            self.x = random.randint(0, 750)

    def draw(self, screen):
        color = (255, 255, 255)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

def homescreen(screen):
    mixer.stop() # stop all bgm from playing
    clock = pygame.time.Clock()

    # Load logo and buttons
    logo = pygame.image.load("images/Homescreen/towerdefenseLogo.png").convert_alpha()
    play_btn = pygame.image.load("images/Homescreen/playbutton.png").convert_alpha()

    # size of pngs
    logo = pygame.transform.smoothscale(logo, (600, 450))
    play_btn = pygame.transform.smoothscale(play_btn, (300, 150))

    # Get rects for positioning
    logo_rect = logo.get_rect(center=(screen.get_width() // 2, 100))
    play_rect = play_btn.get_rect(center=(screen.get_width() // 2, 265))

    spores = [Spore(750, 400) for _ in range(50)]

    while True:
        # Background
        screen.fill((15, 15, 20))
        for spore in spores:
            spore.update()
            spore.draw(screen)

        # Draw logo and play button
        screen.blit(logo, logo_rect)
        screen.blit(play_btn, play_rect)
        
        for event in pygame.event.get():

            mouse_pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 if event.button == 1 and play_rect.collidepoint(mouse_pos):
                    return

        pygame.display.flip()
        clock.tick(60)


def pause_screen(screen, mixer):
    mixer.music.pause() 

    # Create a transparent overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  
    overlay.fill((0, 0, 0, 150))  
    font = pygame.font.SysFont("Arial", 50)
    pause_text = font.render("Game Paused", True, (255, 255, 255))
    resume_text = pygame.font.SysFont("Arial", 30).render("Press ESC to Resume", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
    screen.blit(overlay, (0, 0))  
    screen.blit(pause_text, pause_rect)
    screen.blit(resume_text, resume_rect)
    pygame.display.flip() 

    # Pause gameloop
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    paused = False
    
    mixer.music.unpause()

def gameclear_screen(screen):
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    mixer.music.stop()

    gameclear_sound = mixer.Sound(os.path.join(BASE_PATH, "sounds", "gameclear.mp3"))
    current_volume = pygame.mixer.music.get_volume()
    gameclear_sound.set_volume(0.4 * current_volume)
    gameclear_sound.play(fade_ms=500)

    clock = pygame.time.Clock()

    game_clear_img = pygame.image.load("images/gameClearScreen.png").convert_alpha()
    game_clear_img = pygame.transform.smoothscale(game_clear_img, (400, 300))  # adjust size if you want

    clear_rect = game_clear_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    sub_font = pygame.font.SysFont("Arial", 28)
    prompt_text = sub_font.render("Click or press any key to return to title", True, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, 280))

    spores = [Spore(750, 400) for _ in range(50)] 
    while True:
        screen.fill((15, 15, 20))
        for spore in spores:
            spore.update()
            spore.draw(screen)
        screen.blit(game_clear_img, clear_rect)
        screen.blit(prompt_text, prompt_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # go back to homescreen

        pygame.display.flip()
        clock.tick(60)

def gameover_screen(screen):
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    mixer.music.stop()

    gameover_sound = mixer.Sound(os.path.join(BASE_PATH, "sounds", "gameover.mp3")) # sound effect
    current_volume = pygame.mixer.music.get_volume()
    gameover_sound.set_volume(0.4 * current_volume)
    gameover_sound.play()

    gameover_text = pygame.font.SysFont("Arial", 50).render("Game Over", True, (255, 0, 0))
    quit_text = pygame.font.SysFont("Arial", 30).render("Press any key to quit or R to retry", True, (255, 255, 255))

    gameover_rect = gameover_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))

    screen.fill((0, 0, 0))
    screen.blit(gameover_text, gameover_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    # Wait for player to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def draw_sidebar(screen, lives, money):
    pygame.draw.rect(screen, (50, 50, 50), (600, 0, 150, 400))
    
    font = pygame.font.SysFont("Arial", 18)
    
    # text
    text_Lives = font.render(f"Lives: {lives}", True, (255, 255, 255))
    text_Money = font.render(f"Money: {money}", True, (255, 255, 255))  # (text, antialias, color, background=None)
    text_tower = font.render("Towers", True, (255, 255, 255))  
    
    screen.blit(text_Lives, (610, 10))  # Position the Money text
    screen.blit(text_Money, (610, 30))  # Position the Money text
    screen.blit(text_tower, (610, 60))  # Position the Tower text
    pygame.draw.line(screen, (255, 255, 255), (610, 85), (740, 85), 1) # Draw a line below the Tower text (surface, color, start_pos, end_pos, width)

def draw_tower_stat(screen, tower):
    pygame.draw.rect(screen, (50, 50, 50), (600, 0, 150, 400))
    font = pygame.font.SysFont("Arial", 18)

    # Create text for tower stats
    text_range = font.render(f"Range: {tower.range}", True, (255, 255, 255))  # White text for range
    text_damage = font.render(f"Damage: {tower.damage}", True, (255, 255, 255))  # White text for damage
    text_cooldown = font.render(f"Cooldown: {tower.cooldown}", True, (255, 255, 255))  # White text for tower name
    

    # Positioning the text on the screen (keeping it aligned on the right side)
    text_range_rect = text_range.get_rect(topleft=(610, 20))
    text_damage_rect = text_damage.get_rect(topleft=(610, 60))
    text_cooldown_rect = text_cooldown.get_rect(topleft=(610, 100))
    

    # Draw the text on the screen
    screen.blit(text_range, text_range_rect)  # Draw range text
    screen.blit(text_damage, text_damage_rect)  # Draw damage text
    screen.blit(text_cooldown, text_cooldown_rect)  # Draw cooldown text

     # Draw Upgrade Button
    upgrade_button_rect = pygame.Rect(620, 150, 120, 40)  # Button size and position
    pygame.draw.rect(screen, (0, 200, 0), upgrade_button_rect)  # Green button
    
    # Upgrade Button Text
    if tower.upgrade < 3:
        upgrade_text = font.render(f"Upgrade: {towers_base[tower.tower_name]["upgrades"][tower.upgrade + 1]["cost"]}", True, (255, 255, 255))
    else:
        upgrade_text = font.render("Max Upgrade", True, (255, 255, 255))
    upgrade_text_rect = upgrade_text.get_rect(center=upgrade_button_rect.center)
    screen.blit(upgrade_text, upgrade_text_rect)
    
    # Draw Sell Button
    sell_button_rect = pygame.Rect(620, 230, 80, 30)  # Button size and position
    pygame.draw.rect(screen, (200, 0, 0), sell_button_rect)  # Red button

    # Sell Button Text
    sell_text = font.render("Sell", True, (255, 255, 255))
    sell_text_rect = sell_text.get_rect(center=sell_button_rect.center)
    screen.blit(sell_text, sell_text_rect)

    
    return upgrade_button_rect, sell_button_rect  # Return both button rects

def number_wave(screen, wave_number):
    font = pygame.font.SysFont("Arial", 18)
    wave_text = font.render(f"Wave: {wave_number}", True, (255, 255, 255))
    screen.blit(wave_text, (630, 360))  # Position the Wave text

def draw_boss_health_bar(screen, boss):
    sporeshield_label = pygame.image.load("images/sporeshield.png").convert_alpha()
    shroomgod_label = pygame.image.load("images/shroomgod.png").convert_alpha()
    
    #Health Bar Dimensions
    screen_width = screen.get_width()
    bar_width = 400
    bar_height = 20
    bar_x = (screen_width - bar_width) // 2
    bar_y = 40  # top margin

    #border
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    # Draw main health (phase 2 or after shield broken)
    if boss.phase == 2:
        health_ratio = boss.hp / boss.max_hp
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    # Draw shield bar (Phase 1)
    if boss.phase == 1:
        shield_ratio = boss.hp / boss.shield_hp
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width * shield_ratio, bar_height))

    # Boss name
    if boss.phase == 1:
        screen.blit(sporeshield_label, (screen.get_width() // 2 - sporeshield_label.get_width() // 2, -238))
    elif boss.phase == 2:
        screen.blit(shroomgod_label, (screen.get_width() // 2 - shroomgod_label.get_width() // 2, -238))



def draw_grid(screen):
    grid_surface = pygame.Surface((800, 600), pygame.SRCALPHA)  # Create a transparent surface
    grid_surface.set_alpha(15)  # Set transparency (0 = fully transparent, 255 = fully opaque)

    for x in range(0, 600, 40):
        for y in range(0, 600, 40):
            pygame.draw.rect(grid_surface, (255, 255, 255, 100), (x, y, 40, 40), 1)  # Draw on transparent surface

    screen.blit(grid_surface, (0, 0))
    
