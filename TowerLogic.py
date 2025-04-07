import pygame
import pygame as pg
import os

from fireball import Fireball
from TowerData import towers_base

# ENEMY PATHS WHERE TOWERS CANNOT BE PLACED
ENEMY_PATHS = [
    (0, 200), (40, 200), (80, 200), (80, 160),
    (80, 120), (80, 80), (120, 80), (160, 80),
    (200, 80), (200, 120), (200, 160), (200, 200),
    (200, 240), (240, 240), (280, 240), (320, 240),
    (360, 240), (360, 200), (360, 160), (400, 160),
    (440, 160), (480, 160), (520, 160), (560, 160)
]

class Tower:
    def __init__(self, x, y, screen, tower_name):

        self.x = x
        self.y = y
        self.tower_name = tower_name
        self.range = towers_base[tower_name]["range"]
        self.damage = towers_base[tower_name]["damage"]
        self.cost = towers_base[tower_name]["cost"]
        self.cooldown = towers_base[tower_name]["cooldown"]
        self.screen = screen
        self.attack_time = 0
        self.fireballs = pygame.sprite.Group()
        self.target = None
        self.upgrade = 0

        # Load animation frames from folder
        folder = f"{tower_name}Tower"
        frame_prefix = tower_name.lower() + "Attack"
        image_path = os.path.join("images", "towers", folder)

        self.frames = [
            pygame.image.load(os.path.join(image_path, f"{frame_prefix}{i + 1}.png")).convert_alpha()
            for i in range(4)
        ]

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Animation control
        self.anim_index = 0
        self.animating = False
        self.last_anim_time = 0
        self.anim_speed = 100  # milliseconds between frames

    def draw(self, boolean):
        if boolean:
            # Create a transparent surface for the range circle
            range_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (255, 255, 255, 45), (self.range, self.range), self.range)
            
            # Adjust the position to center the circle on the tower
            center_x = self.x + self.rect.width // 2
            center_y = self.y + self.rect.height // 2
            self.screen.blit(range_surface, (center_x - self.range, center_y - self.range))

        # Draw the tower's animation
        self.screen.blit(self.image, (self.x, self.y))



        for fireball in self.fireballs:
            fireball.draw()

    #def enemy_in_range(self, enemy):
    #    dx = enemy.x - self.x  # get x distance between enemy and tower
    #    dy = enemy.y - self.y  # get y distance between enemy and tower
    #    dist = (dx ** 2 + dy ** 2) ** 0.5  # get distance between enemy and tower
    #    if dist <= self.range:
    #        return True
    #    return False


    
    def update_animation(self, fps):
        if self.animating:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_anim_time > self.anim_speed * (60 / fps):
                self.last_anim_time = current_time
                self.anim_index += 1
                if self.anim_index >= len(self.frames):
                    self.anim_index = 0
                    self.animating = False
                    self.attack_time = pygame.time.get_ticks()
                    self.target = None
                self.image = self.frames[self.anim_index]
        else:
            self.image = self.frames[0]  # reset to first frame

    # fixes towers not attacking giant: come back to here if any problems
    def take_aim(self, enemies):
        for enemy in enemies:
            if enemy.hp > 0:
                enemy_center_x = enemy.rect.centerx
                enemy_center_y = enemy.rect.centery
                dx = enemy_center_x - self.x
                dy = enemy_center_y - self.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist <= self.range:
                    self.target = enemy
                    fireball = Fireball(self.x, self.y, self.target, speed=3, screen=self.screen, damage = self.damage)
                    self.fireballs.add(fireball)  # Add fireball to group
                    self.attack_time = pygame.time.get_ticks()
                    # Place all damage logic below
                    self.target.hp -= fireball.damage
                    if self.target.hp <= 0:
                        self.target.is_dying = True

                    break

    def attack(self, enemies, fps):
        #Add attack anims here
        if self.target:
            self.animating = True
            self.fireballs.update()
        else:
            if pygame.time.get_ticks() - self.attack_time > (self.cooldown * 1000) * (60 / fps):
                self.take_aim(enemies)

    def update(self):
        # Update all fireballs
        self.fireballs.update()

    def do_upgrade(self):
        if self.upgrade == 3:
            print("Max upgrade reached")
        else:
            self.upgrade += 1
            self.damage = towers_base[self.tower_name]["upgrades"][self.upgrade]["damage"]
            self.cooldown = towers_base[self.tower_name]["upgrades"][self.upgrade]["cooldown"]
            self.range = towers_base[self.tower_name]["upgrades"][self.upgrade]["range"]

    # def attack(self, enemies):
    #     if self.can_attack(enemy):
    #         self.attack_time = pygame.time.get_ticks() + self.cooldown * 1000
    #         self.anim_index = 0
    #         self.animating = True
    #         return True
    #     return False

