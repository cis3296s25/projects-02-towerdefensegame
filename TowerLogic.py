import pygame

class Tower:
    def __init__(self, x, y, range, damage, cooldown, screen, image):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

