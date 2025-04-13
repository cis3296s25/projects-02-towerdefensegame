import pygame
import math
import os
from os.path import abspath, dirname

from EnemyData import mob_data

# enemy's path
WAYPOINTS = [
    (-40, 195),
    (82, 195),
    (82, 75),
    (202, 75),
    (202, 235),
    (362, 235),
    (362, 155),
    (601, 155),
    (601, 155)
]

GIANT_PATH = [
    (-100, 120),
    (52, 120),
    (52, 10),
    (173, 10),
    (173, 164),
    (333, 164),
    (333, 87),
    (595, 87),
    (595, 87)
]

BASE_PATH = abspath(dirname(__file__))
#IMAGE_PATH = BASE_PATH + "/images/enemy1/RedMushroom/"

class Enemy:

    def __init__(self, x, y, screen, color, waypoints = None, scream_sound = None, boss_music = None):

        self.waypoints = waypoints if waypoints else WAYPOINTS
        self.color = color
        self.money = mob_data[color]["Money"]
        self.score = mob_data[color]["Score"]
        self.speed = mob_data[color]["Speed"]
        self.hp = mob_data[color]["Health"]
        self.max_hp = mob_data[color]["Health"]
        self.dmg = mob_data[color]["Damage"] 
        self.x = x
        self.y = y

        self.screen = screen

        folder = f"{color}Mushroom"
        frame_prefix = color.lower() + "mushroom"

        image_path = os.path.join(BASE_PATH, "images", "enemy1", folder)

        if self.color == "Boss":
            self.load_boss_frames()
        else:
            folder = f"{color}Mushroom"
            frame_prefix = color.lower() + "mushroom"
            image_path = os.path.join(BASE_PATH, "images", "enemy1", folder)
            self.frames = [
                pygame.image.load(os.path.join(image_path, f"{frame_prefix}{i}.png")).convert_alpha()
                for i in range(8)
            ]
            self.death_frames = [
                pygame.image.load(os.path.join(image_path, "Die", f"{frame_prefix}die{i}.png")).convert_alpha()
                for i in range(7)
            ]

        self.current_frame = 0
        self.frame_timer = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


        if color == "Giant":
            self.waypoints = GIANT_PATH
        elif waypoints:
            self.waypoints = waypoints
        else:
            self.waypoints = WAYPOINTS


        self.waypoint_index = 0
        self.target_x, self.target_y = self.waypoints[self.waypoint_index]
        self.reached_end = False 


        self.is_dying = False
        self.death_frame_index = 0
        self.death_animation_done = False


        self.transforming = False

        self.is_boss = color == "Boss"
        self.phase = 1 if self.is_boss else None
        if self.is_boss:
            self.shield_hp = 1000
            self.hp = self.shield_hp

            self.boss_scream_sound = scream_sound
            self.boss_battle_music = boss_music

            # Boss transformation setup
            
            self.transformation_start = 0
            self.transformation_duration = 2500  # 2.5 seconds

            self.load_boss_frames()

    def load_boss_frames(self):
        if self.color == "Boss":
            #Phase 1 walking frames
            image_path = os.path.join(BASE_PATH, "images", "enemy1", "BossMushroom", "Phase1")
            self.frames = [
                pygame.image.load(os.path.join(image_path, f"bossphase1_{i}.png")).convert_alpha()
                for i in range(8)
            ]

            #Phase 2 walking and death frames
            self.phase2_frames = [
                pygame.image.load(os.path.join(BASE_PATH, "images", "enemy1", "BossMushroom", "Phase2", f"bossphase2_{i}.png")).convert_alpha()
                for i in range(8)
            ]
            self.phase2_death_frames = [
                pygame.image.load(os.path.join(BASE_PATH, "images", "enemy1", "BossMushroom", "Phase2", "Die", f"bossphase2die{i}.png")).convert_alpha()
                for i in range(7)
            ]

        else:
            folder = f"{self.color}Mushroom"
            frame_prefix = self.color.lower() + "mushroom"
            image_path = os.path.join(BASE_PATH, "images", "enemy1", folder)
            self.frames = [
                pygame.image.load(os.path.join(image_path, f"{frame_prefix}{i}.png")).convert_alpha()
                for i in range(8)
            ]
            self.death_frames = [
                pygame.image.load(os.path.join(image_path, "Die", f"{frame_prefix}die{i}.png")).convert_alpha()
                for i in range(7)
            ]

    def move(self):
        if self.reached_end:  # Enemy reached the end
            return
        
         # Animate enemy
        self.frame_timer += 1
        if self.frame_timer % 10 == 0:  # Adjust frame speed
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.x, self.y = self.target_x, self.target_y
            self.waypoint_index += 1 # moves to next waypoint

            if self.waypoint_index >= len(self.waypoints):
                self.reached_end = True # no more waypoints
                return
            else:
                self.target_x, self.target_y = self.waypoints[self.waypoint_index]
        else:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

        self.rect.topleft = (self.x, self.y)

    #update method handles whether move animation or death animation is played
    def update(self):
        if self.is_boss:
            # Start transformation if shield breaks
            if self.phase == 1 and self.hp <= 0 and not self.transforming:
                self.phase = 2
                self.transforming = True
                self.transformation_start = pygame.time.get_ticks()
                self.speed = 0  # stop boss movement
                self.target = None  # towers should also stop firing (handled externally)
                self.image = self.frames[0]  # freeze current frame

                if self.boss_scream_sound:
                    pygame.mixer.music.stop()
                    self.boss_scream_sound.play()
                return

            # Handle transformation timer
            if self.transforming:
                now = pygame.time.get_ticks()
                if now - self.transformation_start >= self.transformation_duration:
                    # End transformation and enter Phase 2
                    self.transforming = False
                    self.hp = 1500
                    self.max_hp = 1500
                    self.speed = 0.4
                    self.frames = self.phase2_frames
                    self.death_frames = self.phase2_death_frames
                    self.current_frame = 0
                    self.frame_timer = 0
                    self.image = self.frames[0]

                    if self.boss_battle_music:
                        pygame.mixer.music.load(self.boss_battle_music)
                        pygame.mixer.music.play(-1)
                return  # Don't move while transforming

        # Death animation (only for enemies or boss in phase 2)
        if self.is_dying:
            self.frame_timer += 1
            if self.frame_timer % 10 == 0:
                if self.death_frame_index < len(self.death_frames):
                    self.image = self.death_frames[self.death_frame_index]
                    self.death_frame_index += 1
                else:
                    self.death_animation_done = True
                    self.death_frame_index = 0
                    self.frame_timer = 0
            return

        # Normal move animation
        self.move()




    def draw(self):

        #pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 40, 40))  # Red square as an Enemy
        self.screen.blit(self.image, (self.x, self.y))
        
        bar_width = 40
        bar_height = 5

        # Center above the enemy based on its rect
        bar_x = self.rect.centerx - bar_width // 2
        #bar_y = self.rect.top + 69  # ← move this number up or down as needed
        if getattr(self, "is_boss", False):
            return
        elif "giant" in self.color.lower():
            bar_y = self.rect.top + 112 #giant mushroom bar
        else:
            bar_y = self.rect.top + 42 #regular mushroom bar



        # Background
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))

        # Fill
        hp_percentage = self.hp / self.max_hp  
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percentage, bar_height))
        
        # pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y + 45, 40, 5))  # HP Bar Background White
        # hpPercentage = self.hp / 50 # Max HP: 50 = 100%
        # pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y + 45, 40 * hpPercentage, 5))  # HP Bar Green
