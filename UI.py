import pygame
import sys #required for .exe creation
import random
from pygame import mixer
import os
import json

from TowerData import towers_base
import Settings
from Achievements import achievements

pygame.font.init()

# Global fonts
button_font = pygame.font.Font("fonts/BrickSans.ttf", 18)
title_font = pygame.font.Font("fonts/BrickSans.ttf", 40)
small_font = pygame.font.Font("fonts/BrickSans.ttf", 13)
button_color = (255, 68, 58)
hover_color = (255, 101, 93)
white = (239,176,125)

class Spore:
   def __init__(self, screen_width, screen_height):
       self.x = random.randint(0, screen_width)
       self.y = random.randint(0, screen_height)
       self.radius = random.randint(1, 3)
       self.speed_y = random.uniform(0.1, 0.5)
       self.alpha = random.randint(100, 200)

   def update(self):
       self.y += self.speed_y
       if self.y > 700:
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
   leaderboard_btn = pygame.image.load("images/Homescreen/leaderboard.png").convert_alpha()
   information_btn = pygame.image.load("images/Homescreen/information.png").convert_alpha()
   achievements_btn = pygame.image.load("images/Homescreen/achievementsbutton.png").convert_alpha()


   # size of pngs
   logo = pygame.transform.smoothscale(logo, (800, 650))
   leaderboard_btn = pygame.transform.smoothscale(leaderboard_btn, (75, 75))
   information_btn = pygame.transform.smoothscale(information_btn, (40, 40))
   achievements_btn = pygame.transform.smoothscale(achievements_btn, (40, 40))

   # Get rects for positioning
   logo_rect = logo.get_rect(center=(screen.get_width() // 2, 150))
   leaderboard_rect = leaderboard_btn.get_rect(bottomleft = ((20), (screen.get_height() - (-5))))
   information_rect = information_btn.get_rect(bottomright = ((screen.get_width()-10), (screen.get_height() - 10)))
   achievements_rect = achievements_btn.get_rect(bottomleft = ((103), (screen.get_height() - 10)))
   pygame.font.init()
   button_font = pygame.font.Font("fonts/BrickSans.ttf", 18)
   button_color = (255, 68, 58)
   hover_color = (255, 101, 93)
   white = (239,176,125)
   
   # Create Play and Settings Rects
   button_width = 120
   button_height = 40
   play_rect = pygame.Rect((screen.get_width() - button_width) // 2, 335, button_width, button_height)
   settings_rect = pygame.Rect((screen.get_width() - button_width) // 2, 390, button_width, button_height)



   spores = [Spore(750, 600) for _ in range(50)]

   while True:
       # Background
       screen.fill((15, 15, 20))
       for spore in spores:
           spore.update()
           spore.draw(screen)

       # Draw logo and play button
       screen.blit(logo, logo_rect)
       mouse_pos = pygame.mouse.get_pos()
       for rect, label in [(play_rect, "Play"), (settings_rect, "Settings")]:
            hovered = rect.collidepoint(mouse_pos)
            color = hover_color if hovered else button_color
            pygame.draw.rect(screen, color, rect, border_radius=20)
            text = button_font.render(label, True, white)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

        # Blit icon-based buttons
       screen.blit(leaderboard_btn, leaderboard_rect)
       screen.blit(information_btn, information_rect)
       screen.blit(achievements_btn, achievements_rect)

       for event in pygame.event.get():

           mouse_pos = pygame.mouse.get_pos()
          
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                   if play_rect.collidepoint(mouse_pos):
                       return "play"
                   elif settings_rect.collidepoint(mouse_pos):
                       return "settings"
                   elif leaderboard_rect.collidepoint(mouse_pos):
                       return "leaderboard"
                   elif information_rect.collidepoint(mouse_pos):
                       return "information"
                   elif achievements_rect.collidepoint(mouse_pos):
                       return "achievements"
                   

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

def returntohome(screen):
    font = pygame.font.Font("fonts/BrickSans.ttf", 20)

    popup_width = 300
    popup_height = 150
    popup_rect = pygame.Rect((screen.get_width() - popup_width) // 2, (screen.get_height() - popup_height) // 2, popup_width, popup_height)
    yes_button = pygame.Rect(popup_rect.centerx - 110, popup_rect.bottom - 50, 80, 30)
    no_button = pygame.Rect(popup_rect.centerx + 30, popup_rect.bottom - 50, 80, 30)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return True
                elif no_button.collidepoint(event.pos):
                    return False

        pygame.draw.rect(screen, (40, 40, 40), popup_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2, border_radius=10)

        # text
        prompt = button_font.render("Return to Main Menu?", True, (255, 255, 255))
        screen.blit(prompt, (popup_rect.centerx - prompt.get_width() // 2, popup_rect.y + 30))

        # Yes button
        pygame.draw.rect(screen, (200, 0, 0), yes_button, border_radius=6)
        yes_text = font.render("Yes", True, (255, 255, 255))
        screen.blit(yes_text, (yes_button.centerx - yes_text.get_width() // 2, yes_button.centery - yes_text.get_height() // 2))

        # No button
        pygame.draw.rect(screen, (0, 150, 0), no_button, border_radius=6)
        no_text = font.render("No", True, (255, 255, 255))
        screen.blit(no_text, (no_button.centerx - no_text.get_width() // 2, no_button.centery - no_text.get_height() // 2))

        pygame.display.update(popup_rect)
        clock.tick(60)

def settings_screen(screen, in_game = False):
   clock = pygame.time.Clock()
   running = True

   achievements_btn = pygame.image.load("images/Homescreen/achievementsbutton.png").convert_alpha()
   achievements_btn = pygame.transform.smoothscale(achievements_btn, (40, 40))
   achievements_rect = achievements_btn.get_rect(bottomleft = ((103), (screen.get_height() - 10)))

   # Volume slider setup
   volume = mixer.music.get_volume()
   muted = volume == 0
   Settings.sfx_volume == 0
   dragging_music = False
   slider_rect = pygame.Rect(300, 200, 150, 10)
   handle_rect = pygame.Rect(slider_rect.x + int(slider_rect.width * volume) - 5, slider_rect.y - 5, 10, 20)

   # SFX Volume
   global sfx_volume
   dragging_sfx = False
   sfx_slider_rect = pygame.Rect(300, 300, 150, 10)
   sfx_handle_rect = pygame.Rect(sfx_slider_rect.x + int(sfx_slider_rect.width * Settings.sfx_volume) - 5, sfx_slider_rect.y - 5, 10, 20)

   # Speaker icons
   speaker_low = pygame.transform.scale(pygame.image.load("images/low-volume.png"), (24, 24))
   speaker_med = pygame.transform.scale(pygame.image.load("images/medium-volume.png"), (24, 24))
   speaker_high = pygame.transform.scale(pygame.image.load("images/high-volume.png"), (24, 24))
   speaker_mute = pygame.transform.scale(pygame.image.load("images/mute.png"), (24, 24))
   music_speaker_rect = pygame.Rect(slider_rect.x + slider_rect.width + 20, slider_rect.y - 5, 24, 24)
   sfx_speaker_rect = pygame.Rect(sfx_slider_rect.x + sfx_slider_rect.width + 20, sfx_slider_rect.y - 5, 24, 24)

   # Load exit button image
   exit_btn = pygame.image.load("images/Homescreen/exitbutton.png").convert_alpha()
   exit_btn = pygame.transform.scale(exit_btn, (40, 40))
   exit_rect = exit_btn.get_rect(topleft=(20, 20))

   # Load home button image
   home_btn = pygame.image.load("images/Homescreen/homebutton.png").convert_alpha()
   home_btn = pygame.transform.scale(home_btn, (40, 40))
   home_rect = home_btn.get_rect(bottomleft=(achievements_rect.left - 50, screen.get_height() - 10))
  
   # Volume icons for music and sfx
   music_icon = pygame.image.load("images/Homescreen/musicIcon.png").convert_alpha()
   music_icon = pygame.transform.scale(music_icon, (32, 32))
   sfx_icon = pygame.image.load("images/Homescreen/sfxIcon.png").convert_alpha()
   sfx_icon = pygame.transform.scale(sfx_icon, (32, 32))

   while running:
        screen.fill((40, 40, 40))
        font = pygame.font.Font("fonts/BrickSans.ttf", 40)
        title = font.render("Settings", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

        # MUSIC VOLUME
        screen.blit(music_icon, (slider_rect.x - 40, slider_rect.y - 8))
        pygame.draw.rect(screen, (200, 200, 200), slider_rect)
        current_volume = mixer.music.get_volume()
        filled_width = int(slider_rect.width * current_volume)
        if filled_width > 0:
            pygame.draw.rect(screen, (255, 255, 255), (slider_rect.x, slider_rect.y, filled_width, slider_rect.height))
        
        sfx_v = Settings.sfx_volume
        sfx_filled_width = int(sfx_slider_rect.width * sfx_v)
        if sfx_filled_width > 0:
            pygame.draw.rect(screen, (255, 255, 255), (sfx_slider_rect.x, sfx_slider_rect.y, sfx_filled_width, sfx_slider_rect.height))
        pygame.draw.rect(screen, (255, 255, 255), handle_rect) # the slider button
        
        actual_music_volume = mixer.music.get_volume()
        music_speaker_icon = (
            speaker_mute if actual_music_volume == 0
            else speaker_high if actual_music_volume > 0.66
            else speaker_med if actual_music_volume > 0.33
            else speaker_low
        )
        screen.blit(music_speaker_icon, music_speaker_rect)

        # SFX VOLUME
        screen.blit(sfx_icon, (sfx_slider_rect.x - 40, sfx_slider_rect.y - 8))
        pygame.draw.rect(screen, (200, 200, 200), sfx_slider_rect)
        pygame.draw.rect(screen, (255, 255, 255), (sfx_slider_rect.x, sfx_slider_rect.y, int(sfx_slider_rect.width * Settings.sfx_volume), sfx_slider_rect.height))
        pygame.draw.rect(screen, (255, 255, 255), sfx_handle_rect)
        sfx_speaker_icon = (
            speaker_mute if Settings.sfx_volume == 0
            else speaker_high if Settings.sfx_volume > 0.66
            else speaker_med if Settings.sfx_volume > 0.33
            else speaker_low
        )
        screen.blit(sfx_speaker_icon, sfx_speaker_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if handle_rect.collidepoint(event.pos):
                    dragging_music = True
                elif music_speaker_rect.collidepoint(event.pos):
                    actual_volume = mixer.music.get_volume()
                    if actual_volume == 0:
                        mixer.music.set_volume(Settings.music_volume) # Unmute to previous volume
                        handle_rect.x = slider_rect.x + int(slider_rect.width * Settings.music_volume) - 5
                    else:
                        Settings.music_volume = actual_volume # Mute and save current volume
                        mixer.music.set_volume(0)
                        handle_rect.x = slider_rect.x
                
                elif sfx_handle_rect.collidepoint(event.pos):
                    dragging_sfx = True

                elif sfx_speaker_rect.collidepoint(event.pos):
                    if Settings.sfx_volume == 0:
                        Settings.sfx_volume = 0.5
                    else:
                        Settings.sfx_volume = 0
                    sfx_handle_rect.x = sfx_slider_rect.x + int(sfx_slider_rect.width * Settings.sfx_volume) - 5
                elif achievements_rect.collidepoint(event.pos):
                    return "achievements"
                
                elif exit_rect.collidepoint(event.pos):
                    return
                elif home_rect.collidepoint(event.pos) and in_game:
                    if returntohome(screen):
                        return "home"

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_music = False
                dragging_sfx = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_music:
                    mouse_x = event.pos[0]
                    volume = max(0, min(1, (mouse_x - slider_rect.x) / slider_rect.width))
                    muted = volume == 0
                    mixer.music.set_volume(0 if muted else volume)
                    handle_rect.x = slider_rect.x + int(slider_rect.width * volume) - 5
                    Settings.music_volume = volume
                if dragging_sfx:
                    mouse_x = event.pos[0]
                    new_sfx_volume  = max(0, min(1, (mouse_x - sfx_slider_rect.x) / sfx_slider_rect.width))
                    sfx_handle_rect.x = sfx_slider_rect.x + int(sfx_slider_rect.width * new_sfx_volume) - 5
                    Settings.sfx_volume = new_sfx_volume
                    sfx_muted = new_sfx_volume == 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Go back to game or menu
          
        screen.blit(exit_btn, exit_rect)
        screen.blit(achievements_btn, achievements_rect)
        if in_game: # don't display if in settings at main menu
            screen.blit(home_btn, home_rect)

        pygame.display.flip()
        clock.tick(60)

def gameclear_screen(screen, score, SCORE_FILE, high_score, top_five, total_wave_time, time_high_score, time_top_five):
   BASE_PATH = os.path.abspath(os.path.dirname(__file__))
   mixer.music.stop()

   gameclear_sound = mixer.Sound(os.path.join(BASE_PATH, "sounds", "gameclear.mp3"))
   current_volume = pygame.mixer.music.get_volume()
   gameclear_sound.set_volume(0.4 * current_volume)
   gameclear_sound.play(fade_ms=500)

   clock = pygame.time.Clock()

   game_clear_img = pygame.image.load("images/gameClearScreen.png").convert_alpha()
   game_clear_img = pygame.transform.smoothscale(game_clear_img, (600, 500))  # adjust size if you want

   clear_rect = game_clear_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 75))
   sub_font = pygame.font.Font("fonts/BrickSans.ttf", 28)
   prompt_text = sub_font.render("Click or press any key to return to title", True, (255, 255, 255))
   prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, 500))
   if (high_score):
       score_text = pygame.font.Font("fonts/BrickSans.ttf", 40).render(f"HIGH SCORE: **{score}**", True, (138, 43, 226))
   elif (top_five):
       score_text = pygame.font.Font("fonts/BrickSans.ttf", 40).render(f"Top Five: *{score}*", True, (173, 216, 23))
   else:
       score_text = pygame.font.Font("fonts/BrickSans.ttf", 40).render(f"Score: {score}", True, (255, 255, 255))
   score_rect = score_text.get_rect(center=(screen.get_width() //2, 375))

   if (time_high_score):
       time_text = pygame.font.Font("fonts/BrickSans.ttf", 30).render(f"Time Taken: {total_wave_time}", True, (138, 43, 226))
   elif (time_top_five):
       time_text = pygame.font.Font("fonts/BrickSans.ttf", 30).render(f"Time Taken: {total_wave_time}", True, (173, 216, 23))
   else:
       time_text = pygame.font.Font("fonts/BrickSans.ttf", 30).render(f"Time Taken: {total_wave_time}", True, (255, 255, 255))
   time_rect = time_text.get_rect(center=(screen.get_width() //2, 450))

   spores = [Spore(750, 600) for _ in range(50)]
   while True:
       screen.fill((15, 15, 20))
       for spore in spores:
           spore.update()
           spore.draw(screen)
       screen.blit(game_clear_img, clear_rect)
       screen.blit(prompt_text, prompt_rect)
       screen.blit(score_text, score_rect)
       screen.blit(time_text, time_rect)
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
               return  # go back to homescreen

       pygame.display.flip()
       clock.tick(60)

def gameover_screen(screen, score, SCORE_FILE, high_score, top_five):
   BASE_PATH = os.path.abspath(os.path.dirname(__file__))
   mixer.music.stop()

   gameover_sound = mixer.Sound(os.path.join(BASE_PATH, "sounds", "gameover.mp3")) # sound effect
   current_volume = pygame.mixer.music.get_volume()
   gameover_sound.set_volume(0.4 * current_volume)
   gameover_sound.play()
   gameover_text = pygame.font.Font("fonts/BrickSans.ttf", 50).render("Game Over", True, (255, 0, 0))
   if (high_score):
       score_text = pygame.font.Font("fonts/BrickSans.ttf", 25).render(f"HIGH SCORE: **{score}**", True, (138, 43, 226))
   elif (top_five):
       score_text = pygame.font.Font("fonts/BrickSans.ttf", 25).render(f"Top Five: *{score}*", True, (173, 216, 23))
   else:
       score_text = pygame.font.Font("fonts/BrickSans.ttf", 25).render(f"Score: {score}", True, (225, 0, 0))
   quit_text = pygame.font.Font("fonts/BrickSans.ttf", 30).render("Press any key to quit or R to retry", True, (255, 255, 255))
   gameover_rect = gameover_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
   score_rect = score_text.get_rect(center=(screen.get_width() //2, screen.get_height() // 2 + 10))
   quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

   screen.fill((0, 0, 0))
   screen.blit(gameover_text, gameover_rect)
   screen.blit(score_text, score_rect)
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
  
   font = pygame.font.Font("fonts/BrickSans.ttf", 10)
  
   # text
   text_Lives = font.render(f"Lives: {lives}", True, (255, 255, 255))
   text_Money = font.render(f"Money: {money}", True, (255, 255, 255))  # (text, antialias, color, background=None)
   text_tower = font.render("Towers", True, (255, 255, 255)) 
   screen.blit(text_Lives, (610, 10))  # Position the Lives text
   screen.blit(text_Money, (610, 30))  # Position the Money text
   screen.blit(text_tower, (610, 60))  # Position the Tower text
   pygame.draw.line(screen, (255, 255, 255), (610, 80), (740, 80), 1) # Draw a line below the Tower text (surface, color, start_pos, end_pos, width)

def draw_underbar(screen, SCORE_FILE, score):
   pygame.draw.rect(screen, (30, 30, 30), (0, 400, 750, 200))
   font = pygame.font.Font("fonts/BrickSans.ttf", 15)

   text_Score = font.render(f"Score: ", True, (255, 255, 255))
   if (get_top_score(SCORE_FILE, "score") < score ):
       value_Score = font.render(f"**{score}**", True, (138, 43, 226))
   elif (is_top_five(SCORE_FILE, score, "score")):
       value_Score = font.render(f"*{score}*", True, (173, 216, 23))
   else:
       value_Score = font.render(f"{score}", True, (255, 255, 255))

   screen.blit(text_Score, (605, 525))
   screen.blit(value_Score, (605+text_Score.get_width(), 525))

def wave_description(wave):
    if wave == 1:
        return "Wave 1: The Red Menace\nA small group of Red shrooms is testing your defenses. They may be weak, but don’t \nunderestimate them!"
    elif wave == 2:
        return "You Earned: $20 for beating the wave! \nWave 2: Red Rush\nThe Red shrooms are back, and this time there are more of them! Can your towers \nhandle the swarm?"
    elif wave == 3:
        return "You Earned: $30 for beating the wave! \nWave 3: Feeling Blue\nThe Reds have brought reinforcements! Blue shrooms join the fight, adding a bit more \nspeed to the mix."
    elif wave == 4:
        return "You Earned: $40 for beating the wave! \nWave 4: Purple Trouble\nThe Blues are stepping up their game, and Purple shrooms have joined the fray. Watch \nout for their resilience!"
    elif wave == 5:
        return "You Earned: $50 for beating the wave! \nWave 5: Glowing Chaos\nThe battlefield lights up as Glowing shrooms enter the fight. Their eerie glow hides \ntheir true danger!"
    elif wave == 6:
        return "You Earned: $60 for beating the wave! \nWave 6: Giant Awakening\nA Giant shroom has arrived! It’s slow but incredibly tough. Can your towers bring \nit down before it reaches the end?"
    elif wave == 7:
        return "You Earned: $70 for beating the wave! \nWave 7: The Blue Horde\nA massive wave of Blue shrooms is charging forward, backed by Purple and Glowing \nshrooms. This is going to be intense!"
    elif wave == 8:
        return "You Earned: $80 for beating the wave! \nWave 8: Glowing Nightmare\nThe Glowing shrooms dominate this wave, with Purple shrooms adding to the chaos. \nCan you survive the glowing onslaught?"
    elif wave == 9:
        return "You Earned: $90 for beating the wave! \nWave 9: Giant’s Revenge\nThree Giants are leading the charge, supported by Reds and Blues. This is a true test \nof your defenses!"
    elif wave == 10:
        return "You Earned: $100 for beating the wave! \nWave 10: The Final Boss\nThe Boss has arrived! It’s massive, powerful, and ready to crush your defenses. \nThis is the ultimate challenge!"
    else:
        return "Unknown Wave\nPrepare for the unexpected!"
    

def draw_tower_stat(screen, tower, mode):
   pygame.draw.rect(screen, (50, 50, 50), (600, 0, 150, 400))
   font = pygame.font.Font("fonts/BrickSans.ttf", 12)

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
   if mode == "no_upgrades_mode":
       pygame.draw.rect(screen, (100, 100, 100), upgrade_button_rect)  # Grayed out
       upgrade_text = font.render("No Upgrades", True, (200, 200, 200))
   elif tower.upgrade < 3:
       pygame.draw.rect(screen, (0, 200, 0), upgrade_button_rect)  # Green
       upgrade_text = font.render(
            f"Upgrade: {towers_base[tower.tower_name]['upgrades'][tower.upgrade + 1]['cost']}",
            True, (255, 255, 255))
   else:
       pygame.draw.rect(screen, (0, 200, 0), upgrade_button_rect)
       upgrade_text = font.render("Max Upgrade", True, (255, 255, 255))

   upgrade_text_rect = upgrade_text.get_rect(center=upgrade_button_rect.center)
   screen.blit(upgrade_text, upgrade_text_rect)
    
   # Draw Sell Button
   sell_button_rect = pygame.Rect(620, 230, 80, 30)  # Button size and position
   pygame.draw.rect(screen, (200, 0, 0), sell_button_rect)  # Red button
  
   # Calculate refund amount
   total_cost = tower.cost
   for i in range(1, tower.upgrade + 1):
       total_cost += towers_base[tower.tower_name]["upgrades"][i]["cost"]
   refund = total_cost // 2

   # Sell Button Text
   sell_text = font.render(f"Sell for {refund}", True, (255, 255, 255))
   sell_text_rect = sell_text.get_rect(center=sell_button_rect.center)
   screen.blit(sell_text, sell_text_rect)

   return upgrade_button_rect, sell_button_rect  # Return both button rects

def number_wave(screen, wave_number):
   font = pygame.font.Font("fonts/BrickSans.ttf", 13)
   wave_text = font.render(f"Wave: {wave_number} of 10", True, (255, 255, 255))
   screen.blit(wave_text, (605, 360))  # Position the Wave text

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

def load_scores(SCORE_FILE):
   if not os.path.exists(SCORE_FILE):
       return[]
   with open(SCORE_FILE, "r") as file:
       try:
           return json.load(file)
       except json.JSONDecodeError:
           return[]

def save_scores(SCORE_FILE, scores):
   with open(SCORE_FILE, "w") as file:
       json.dump(scores, file)

def update_scores(SCORE_FILE, score, sort_method):
   scores = load_scores(SCORE_FILE)
   scores.append(score)
   if (sort_method == "score"):
       scores.sort(reverse = True)
   elif (sort_method == "time"):
       scores.sort(reverse = False)
   scores = scores[:5]
   save_scores(SCORE_FILE, scores)
   return scores

def get_top_score(SCORE_FILE, sort_method):
   scores = load_scores(SCORE_FILE)
   if not scores:
       if (sort_method == "score"):
           return 0
       elif (sort_method == "time"):
           return float('inf')
   if (sort_method == "score"):
       return (max(scores))
   elif (sort_method == "time"):
       return (min(scores))

def is_top_five(SCORE_FILE, score, sort_method):
   scores = load_scores(SCORE_FILE)
   if (len(scores) < 5):
       return True
   if (sort_method == "score"):
       return (score > min(scores))
   elif (sort_method == "time"):
       return (score > max(scores))
  
def leaderboard_screen(screen, SCORE_FILE, TOTAL_WAVE_TIME_FILE):
   pygame.font.init()
   font = pygame.font.SysFont("fonts/BrickSans.ttf", 30)
   smallFont = pygame.font.SysFont("fonts/BrickSans.ttf", 20)
   white = (255, 255, 255)
   clock = pygame.time.Clock()

   scores = load_scores(SCORE_FILE)
   times = load_scores(TOTAL_WAVE_TIME_FILE)

   total_pages = 2
   current_page = 0

   spores = [Spore(750, 600) for _ in range(50)]

   #space or esc to quit
   running = True
   while running:
       screen.fill((15, 15, 20))
       for spore in spores:
           spore.update()
           spore.draw(screen)

       if current_page == 0:
           for i, score in enumerate(scores):
               line = f"{i+1}. {score}"
               text = font.render(line, True, white)
               screen.blit(text, (100, 120 + i * 40))
           title = font.render("***TOP SCORES***", True, white)
           screen.blit (title, (screen.get_width() // 2 - title.get_width() // 2, 50))

           page_dir_text = smallFont.render(f"Press ESC or SPACE keys to return to home", True, (255, 255, 255))
           page_nav_text = smallFont.render(f"Use left and right arrow keys to navigate pages", True, (255, 255, 255))
           page_num_text = smallFont.render(f"Page {current_page + 1} of {total_pages}", True, (255, 255, 255))

           screen.blit(page_dir_text, (screen.get_width()//2 - page_dir_text.get_width()//2, screen.get_height() - 35 - page_nav_text.get_height()))
           screen.blit(page_nav_text, (screen.get_width()//2 - page_nav_text.get_width()//2, screen.get_height() - 30))
           screen.blit(page_num_text, (screen.get_width() - page_num_text.get_width() - 40, screen.get_height() - 30))
       elif current_page == 1:
           for i, time in enumerate(times):
               line = f"{i+1}. {time} seconds"
               text = font.render(line, True, white)
               screen.blit(text, (100, 120 + i * 40))
           title = font.render("***TOP TIMES***", True, white)
           screen.blit (title, (screen.get_width() // 2 - title.get_width() // 2, 50))

           page_dir_text = smallFont.render(f"Press ESC or SPACE keys to return to home", True, (255, 255, 255))
           page_nav_text = smallFont.render(f"Use left and right arrow keys to navigate pages", True, (255, 255, 255))
           page_num_text = smallFont.render(f"Page {current_page + 1} of {total_pages}", True, (255, 255, 255))

           screen.blit(page_dir_text, (screen.get_width()//2 - page_dir_text.get_width()//2, screen.get_height() - 35 - page_nav_text.get_height()))
           screen.blit(page_nav_text, (screen.get_width()//2 - page_nav_text.get_width()//2, screen.get_height() - 30))
           screen.blit(page_num_text, (screen.get_width() - page_num_text.get_width() - 40, screen.get_height() - 30))

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               exit()
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   running = False
               elif event.key == pygame.K_SPACE:
                   running = False
               elif event.key == pygame.K_LEFT and current_page > 0:
                   current_page -= 1
               elif event.key == pygame.K_RIGHT and current_page < (total_pages - 1):
                   current_page += 1
       pygame.display.flip()
       clock.tick(60)

def instructions_screen(screen, INSTRUCTIONS_FILE):
   pygame.font.init()
   clock = pygame.time.Clock()
   font = pygame.font.SysFont("fonts/BrickSans.ttf", 20)

   try:
       with open(INSTRUCTIONS_FILE, "r") as file:
           instructions = file.readlines()
   except FileNotFoundError:
       instructions = ["Instructions file not found"]

   lines_per_page = 12
   total_pages = (len(instructions)+lines_per_page-1) // lines_per_page
   current_page = 0

   spores = [Spore(screen.get_width(), screen.get_height()) for _ in range(50)]
  
   running = True
   while running:
       screen.fill((15, 15, 20))
       for spore in spores:
           spore.update()
           spore.draw(screen)
       start = current_page * lines_per_page
       end = start + lines_per_page

       title = font.render("***GAME INSTRUCTIONS***", True, (255, 255, 255))
       screen.blit (title, (screen.get_width() // 2 - title.get_width() // 2, 50))

       for i, line in enumerate(instructions[start:end]):
           text_surface = font.render(line.strip(), True, (255, 255, 255))
           screen.blit(text_surface, (50, 50+i * 30 + 30))

       page_dir_text = font.render(f"Press ESC or SPACE keys to return to home", True, (255, 255, 255))
       page_nav_text = font.render(f"Use left and right arrow keys to navigate pages", True, (255, 255, 255))
       page_num_text = font.render(f"Page {current_page + 1} of {total_pages}", True, (255, 255, 255))

       screen.blit(page_dir_text, (screen.get_width()//2 - page_dir_text.get_width()//2, screen.get_height() - 35 - page_nav_text.get_height()))
       screen.blit(page_nav_text, (screen.get_width()//2 - page_nav_text.get_width()//2, screen.get_height() - 30))
       screen.blit(page_num_text, (screen.get_width() - page_num_text.get_width() - 40, screen.get_height() - 30))  

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   running = False
               elif event.key == pygame.K_SPACE:
                   running = False
               elif event.key == pygame.K_LEFT and current_page > 0:
                   current_page -= 1
               elif event.key == pygame.K_RIGHT and current_page < (total_pages - 1):
                   current_page += 1
       pygame.display.flip()
       clock.tick(60)

def achievements_screen(screen, achievements):
   clock = pygame.time.Clock()
   running = True
   font = pygame.font.Font("fonts/BrickSans.ttf", 13)
   big_font = pygame.font.Font("fonts/BrickSans.ttf", 20)
  
   # Load and scale exit button (same as settings screen)
   exit_btn = pygame.image.load("images/Homescreen/exitbutton.png").convert_alpha()
   exit_btn = pygame.transform.scale(exit_btn, (40, 40))
   exit_rect = exit_btn.get_rect(topleft=(20, 20))

   # Calculate progress
   unlocked = sum(1 for a in achievements.values() if a["unlocked"])
   total = len(achievements)
  
   # Layout variables
   padding = 20
   card_width = 200
   card_height = 100
   cols = 3
   scroll_y = 0
   scroll_speed = 20
   max_scroll = ((total + cols - 1) // cols) * (card_height + padding) - 400

   def draw_wrapped_text(surface, text, font, color, x, y, max_width):
       words = text.split()
       lines = []
       current_line = ""

       for word in words:
           test_line = current_line + word + " "
           if font.size(test_line)[0] <= max_width:
               current_line = test_line
           else:
               lines.append(current_line.strip())
               current_line = word + " "
       lines.append(current_line.strip())

       for i, line in enumerate(lines):
           rendered = font.render(line, True, color)
           surface.blit(rendered, (x, y + i * font.get_linesize()))

   while running:
       screen.fill((20, 20, 20))
       mouse = pygame.mouse.get_pos()
       screen.blit(exit_btn, (exit_rect.x, exit_rect.y + scroll_y))

       # Title and Progress
       title = big_font.render("Achievements", True, (255, 255, 255))
       screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 20 + scroll_y))

       progress = font.render(f"{unlocked}/{total} Unlocked", True, (200, 200, 200))
       screen.blit(progress, (screen.get_width() // 2 - progress.get_width() // 2, 60 + scroll_y))
       # Draw achievements grid
       start_y = 110 + scroll_y
       achievements_list = list(achievements.items())
       for idx, (name, data) in enumerate(achievements_list):
           row = idx // cols
           col = idx % cols
           x = padding + col * (card_width + padding)
           y = start_y + row * (card_height + padding) + scroll_y

           # Card background
           bg_color = (60, 60, 60) if not data["unlocked"] else (255, 68, 58)
           pygame.draw.rect(screen, bg_color, (x, y, card_width, card_height), border_radius=5)

           # Card border color based on unlock status
           border_color = (100, 100, 100) if not data["unlocked"] else (239, 176, 125)
           pygame.draw.rect(screen, border_color, (x, y, card_width, card_height), width=2, border_radius=5)
                      
           is_secret = data.get("category") == "Secret" and not data["unlocked"]

           if is_secret:
               title_text = "???"
               desc_text = "???"
           else:
               title_text = name
               desc_text = data["description"]
          
           # Title (uses title_text now)
           font.set_underline(True)
           title_rendered = font.render(title_text, True, (239, 176, 125))
           font.set_underline(False)
           screen.blit(title_rendered, (x + 10, y + 10))

           # Description (uses desc_text now)
           draw_wrapped_text(screen, desc_text, font, (239, 176, 125), x + 10, y + 40, card_width - 20)

       # Handle events
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               exit()
           elif event.type == pygame.MOUSEBUTTONDOWN:
               if exit_rect.move(0, scroll_y).collidepoint(mouse):
                   return
               if event.button == 4:  # scroll up
                   scroll_y = min(scroll_y + scroll_speed, 0)
               if event.button == 5:  # scroll down
                   scroll_y = max(scroll_y - scroll_speed, -max_scroll)
       pygame.display.flip()
       clock.tick(60)

def mode_selection_screen(screen):
    clock = pygame.time.Clock()
    running = True

    pygame.font.init()
    title_font =  pygame.font.Font("fonts/BrickSans.ttf", 48)
    button_font = pygame.font.Font("fonts/BrickSans.ttf", 18)
    desc_font = pygame.font.Font("fonts/BrickSans.ttf", 11)

    white = (255, 255, 255)
    gray = (239,176,125)
    button_color = (255, 68, 58)
    hover_color = (255,101,93)

    exit_btn = pygame.image.load("images/Homescreen/exitbutton.png").convert_alpha()
    exit_btn = pygame.transform.scale(exit_btn, (40, 40))
    exit_rect = exit_btn.get_rect(topleft=(20, 20))

    modes = [
        {"name": "Normal Mode", "desc": "Standard gameplay with upgrades"},
        {"name": "No Upgrades Mode", "desc": "Towers cannot be upgraded"},
        {"name": "Hardcore Mode", "desc": "1 life, tougher enemies, costly towers"},
        {"name": "Reverse Mode", "desc": "Enemies spawn from the opposite side"},
    ]

    button_width = 300
    button_height = 60
    padding = 20
    start_y = 150
    button_rects = [
        pygame.Rect((screen.get_width() - button_width) // 2, start_y + i * (button_height + padding), button_width, button_height)
        for i in range(len(modes))
    ]

    spores = [Spore(750, 600) for _ in range(50)]

    while running:
        screen.fill((15, 15, 20))

        screen.blit(exit_btn, exit_rect)

        title_surface = title_font.render("Select Game Mode", True, white)
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 60))

        for spore in spores:
            spore.update()
            spore.draw(screen)


        mouse = pygame.mouse.get_pos()
        for i, rect in enumerate(button_rects):
            hovered = rect.collidepoint(mouse)
            pygame.draw.rect(screen, hover_color if hovered else button_color, rect, border_radius=8)
            text = button_font.render(modes[i]["name"], True, white)
            desc = desc_font.render(modes[i]["desc"], True, gray)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.y + 10))
            screen.blit(desc, (rect.centerx - desc.get_width() // 2, rect.y + 35))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    return "home"
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        return modes[i]["name"].lower().replace(" ", "_")

        pygame.display.flip()
        clock.tick(60)
