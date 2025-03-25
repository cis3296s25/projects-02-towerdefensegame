import pygame
import math

# enemy's path
WAYPOINTS = [
    (0, 185),
    (75, 185),
    (75, 72),
    (200, 72),
    (200, 230),
    (355, 230),
    (355, 150),
    (600, 150)
]

class Enemy:

    def __init__(self, x, y, hp, range, dmg, cooldown, screen, image):
        self.hp = hp
        self.range = range
        self.dmg = dmg
        self.cooldown = cooldown
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.screen = screen

        self.speed = 1.0

        self.waypoints = WAYPOINTS
        self.waypoint_index = 0
        self.target_x, self.target_y = self.waypoints[self.waypoint_index]
        self.reached_end = False 

    def move(self):
        if self.reached_end:  # Enemy reached the end
            return
        
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
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y + 45, 40, 5))  # HP Bar Background White
        hpPercentage = self.hp / 50 # Max HP: 50 = 100%
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y + 45, 40 * hpPercentage, 5))  # HP Bar Green
