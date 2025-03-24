import pygame

class Map:
    def __init__(self, screen, image):
        self.screen = screen
        self.image = image
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

