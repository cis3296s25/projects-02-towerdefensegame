import pygame
import math
import os
from os.path import abspath, dirname

from EnemyData import mob_data

# enemy's path
WAYPOINTS = [
    (-40, 160),
    (60, 160),
    (60, 40),
    (180, 40),
    (180, 200),
    (340, 200),
    (340, 120),
    (570, 120)
]

GIANT_PATH = [
    (-120, 35),
    (-20, 35),
    (-20, -85),
    (100, -85),
    (100, 75),
    (260, 75),
    (260, -5),
    (510, -5)
]

BASE_PATH = abspath(dirname(__file__))
#IMAGE_PATH = BASE_PATH + "/images/enemy1/RedMushroom/"

class Enemy:

    def __init__(self, x, y, screen, color, waypoints = None):

        self.waypoints = waypoints if waypoints else WAYPOINTS
        self.color = color
        self.money = mob_data[color]["Money"]
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

        self.frames = [
            pygame.image.load(os.path.join(image_path, f"{frame_prefix}{i}.png")).convert_alpha()
            for i in range(8)
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

        #Load death animation frames
        self.death_frames = [
            pygame.image.load(os.path.join(image_path, "Die", f"{frame_prefix}die{i}.png")).convert_alpha()
            for i in range(7)
        ]


        self.is_dying = False
        self.death_frame_index = 0
        self.death_animation_done = False

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
        if self.is_dying:
            self.frame_timer += 1
            if self.frame_timer % 10 == 0: #can adjust speed as needed
                if self.death_frame_index < len(self.death_frames):
                    self.image = self.death_frames[self.death_frame_index]
                    self.death_frame_index += 1
                else:
                    self.death_animation_done = True
                    self.death_frame_index = 0  # Reset the death frame index
                    self.frame_timer = 0  # Reset the frame timer
                    #self.death_animation_done = False  # Reset the death animation flag
                    #self.is_dying = False  # Stop the death animation from looping

            return
        
        self.move()

    
    def draw(self):

        #pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 40, 40))  # Red square as an Enemy
        self.screen.blit(self.image, (self.x, self.y))
        
        bar_width = 40
        bar_height = 5

        # Center above the enemy based on its rect
        bar_x = self.rect.centerx - bar_width // 2
        #bar_y = self.rect.top + 69  # ← move this number up or down as needed

        if "giant" in self.color.lower():
            bar_y = self.rect.top + 195 #giant mushroom bar
        else:
            bar_y = self.rect.top + 69 #regular mushroom bar



        # Background
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))

        # Fill
        hp_percentage = self.hp / self.max_hp  
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percentage, bar_height))
        
        # pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y + 45, 40, 5))  # HP Bar Background White
        # hpPercentage = self.hp / 50 # Max HP: 50 = 100%
        # pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y + 45, 40 * hpPercentage, 5))  # HP Bar Green
