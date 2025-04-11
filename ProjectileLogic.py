from re import match
from unittest import case

import pygame
import os

from TowerData import towers_base


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, range, frenetic, target, speed, screen, damage):
        super().__init__()
        self.x = x
        self.y = y
        self.target = target
        self.speed = speed
        self.screen = screen
        self.damage = damage
        self.range = range
        self.image = self.choose_image(image)
        self.name = image
        self.frenetic = frenetic

        self.rect = self.image.get_rect(center=(self.x, self.y))


        # Ensure target is valid

        dx = target.rect.centerx - self.x
        dy = target.rect.centery - self.y
        distance = self.dist_to(self.target)  # Avoid division by zero
        self.direction = (dx / distance, dy / distance)
        # else:
        #     self.direction = (0, 0)  # Fireball won’t move if there’s no target

    def update(self):
        if self.target is None or self.target.hp <= 0:
            self.kill()  # Remove fireball if the target is dead
            return
        elif self.dist_to(self.target) > self.range:
            self.kill()
            return


        if self.frenetic:
            # current distance to target (dtt) and calculate trajectory
            dx = self.target.rect.centerx - self.x
            dy = self.target.rect.centery - self.y
            dist_to_target = self.dist_to(self.target)
            self.direction = (dx/dist_to_target, dy/dist_to_target)
            self.speed += 1



        #move the projectile
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed


        self.rect.center = (self.x, self.y)
        # Check for collision with the target
        if self.rect.colliderect(self.target.rect) or self.dist_to(self.target) > self.range:
            #self.target.hp -= self.damage  # Damage the target
            if self.target.hp <= 0:
                self.target.is_dying = True
            self.kill()  # Remove the fireball from the game

    def dist_to(self, target):
        dx = target.rect.centerx - self.x
        dy = target.rect.centery - self.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        return distance
    def dist_to_coord(self, coord):
        dx = coord[0] - self.x
        dy = coord[1] - self.y
        return max(1, (dx ** 2 + dy ** 2) ** 0.5)
    def choose_image(self, image):
        global projectile
        match image:
            case "fireball":
                projectile = self.image = pygame.image.load("images/smallfireball.png")
                self.frenetic = True
            case "arrow":
                projectile = self.image = pygame.image.load("images/arrowPlaceHolder.png")
        return projectile

    def draw(self):
        self.screen.blit(self.image, self.rect)
