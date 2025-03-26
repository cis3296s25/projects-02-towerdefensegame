import pygame
import math
from os.path import abspath, dirname


# enemy's path
WAYPOINTS = [
    (0, 160),
    (60, 160),
    (60, 40),
    (180, 40),
    (180, 200),
    (340, 200),
    (340, 120),
    (570, 120)
]

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + "/images/enemy1/RedMushroom/"

class Enemy:

    def __init__(self, x, y, hp, attack_range, dmg, cooldown, screen):
        self.hp = hp
        self.range = attack_range
        self.dmg = dmg
        self.cooldown = cooldown
        self.x = x
        self.y = y
        
        self.screen = screen

        self.speed = 1.0

        #animates enemy
        self.frames = [
            pygame.image.load(IMAGE_PATH + f"mushroom{i}.png").convert_alpha()
            for i in range(8)
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.waypoints = WAYPOINTS
        self.waypoint_index = 0
        self.target_x, self.target_y = self.waypoints[self.waypoint_index]
        self.reached_end = False 

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


    
    def draw(self):

        #pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 40, 40))  # Red square as an Enemy
        self.screen.blit(self.image, (self.x, self.y))
        
        bar_width = 40
        bar_height = 5

        # Center above the enemy based on its rect
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top + 69  # ← move this number up or down as needed

        # Background
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))

        # Fill
        hp_percentage = self.hp / 50
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percentage, bar_height))

        
        # pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y + 45, 40, 5))  # HP Bar Background White
        # hpPercentage = self.hp / 50 # Max HP: 50 = 100%
        # pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y + 45, 40 * hpPercentage, 5))  # HP Bar Green
