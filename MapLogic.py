import pygame

class Map:
    def __init__(self, screen, image):
        self.screen = screen
        self.original_image = image
        self.image = image
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.width, self.height = self.image.get_size()
        print(f"Map image size: {self.width}x{self.height}")

    def draw(self, w_scale = 1, h_scale = 1):
        self.image = pygame.transform.scale(self.original_image, (self.width * w_scale, self.height * h_scale))
        self.screen.blit(self.image, (self.x, self.y))

