from re import match
from unittest import case

import pygame
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, range, target, speed, screen, damage):
        super().__init__()
        self.x = x
        self.y = y
        self.target = target
        self.speed = speed
        self.screen = screen
        self.damage = damage
        self.range = range
        self.image = self.choose_image(image)

        self.rect = self.image.get_rect(center=(self.x, self.y))


        # Ensure target is valid

        dx = target.rect.centerx - self.x
        dy = target.rect.centery - self.y
        distance = self.get_distance(self.target)  # Avoid division by zero
        self.direction = (dx / distance, dy / distance)
        # else:
        #     self.direction = (0, 0)  # Fireball won’t move if there’s no target

    def update(self):
        if self.target is None or self.target.hp <= 0:
            self.kill()  # Remove fireball if the target is dead
            return
        elif self.get_distance(self.target) > self.range:
            self.kill()
            return

        # Move the fireball towards the target
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.rect.center = (self.x, self.y)

        # Check for collision with the target
        if self.rect.colliderect(self.target.rect) or self.get_distance(self.target) > self.range:
            #self.target.hp -= self.damage  # Damage the target
            if self.target.hp <= 0:
                self.target.is_dying = True
            self.kill()  # Remove the fireball from the game

    def get_distance(self, target):
        dx = target.rect.centerx - self.x
        dy = target.rect.centery - self.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        return distance
    def choose_image(self, image):
        global projectile
        match image:
            case "fireball":
                projectile = self.image = pygame.image.load("images/smallfireball.png")
            case "arrow":
                projectile = self.image = pygame.image.load("images/arrowPlaceHolder.png")
        return projectile

    def draw(self):
        self.screen.blit(self.image, self.rect)
