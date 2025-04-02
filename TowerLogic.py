import pygame
import pygame as pg
import os

from fireball import Fireball

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
    def __init__(self, x, y, tower_range, damage, cooldown, screen, tower_name):
        self.x = x
        self.y = y
        self.range = tower_range
        self.damage = damage
        self.cooldown = cooldown
        self.screen = screen
        self.attack_time = 0
        self.fireballs = pygame.sprite.Group()
        self.target = None

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
        range_surface = pygame.Surface((240, 240), pygame.SRCALPHA)
        if boolean:
            pygame.draw.circle(range_surface, (255, 255, 255, 45), (140, 140), self.range)
        self.screen.blit(range_surface, (self.x - 120, self.y - 120))

        self.update_animation()
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


    
    def update_animation(self):
        if self.animating:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_anim_time > self.anim_speed:
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
                    #self.target.hp -= self.damage
                    fireball = Fireball(self.x, self.y, self.target, speed=3, screen=self.screen, damage = 10)
                    self.fireballs.add(fireball)  # Add fireball to group
                    self.attack_time = pygame.time.get_ticks()
                    # Place all damage logic below
                    self.target.hp -= fireball.damage
                    if self.target.hp <= 0:
                        self.target.is_dying = True

                    break

    def attack(self, enemies):
        #Add attack anims here
        if self.target:
            self.animating = True
            self.fireballs.update()
        else:
            if pygame.time.get_ticks() - self.attack_time > self.cooldown * 1000:
                self.take_aim(enemies)

    def update(self):
        # Update all fireballs
        self.fireballs.update()

    # def attack(self, enemies):
    #     if self.can_attack(enemy):
    #         self.attack_time = pygame.time.get_ticks() + self.cooldown * 1000
    #         self.anim_index = 0
    #         self.animating = True
    #         return True
    #     return False

