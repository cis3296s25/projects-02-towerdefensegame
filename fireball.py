import pygame
import os

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, target, speed, screen):
        super().__init__()
        self.x = x
        self.y = y
        self.target = target
        self.speed = speed
        self.screen = screen
        self.image = pygame.image.load(os.path.join("images", "smallfireball.png")).convert_alpha()  
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Ensure target is valid
        if target:
            dx = target.rect.centerx - self.x
            dy = target.rect.centery - self.y
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Avoid division by zero
            self.direction = (dx / distance, dy / distance)
        else:
            self.direction = (0, 0)  # Fireball won’t move if there’s no target

    def update(self):
        if self.target is None or self.target.hp <= 0:
            self.kill()  # Remove fireball if the target is dead
            return

        # Move the fireball towards the target
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.rect.center = (self.x, self.y)

        # Check for collision with the target
        if self.rect.colliderect(self.target.rect):
            self.target.hp -= 10  # Damage the target
            self.kill()  # Remove the fireball from the game


    def draw(self):
        self.screen.blit(self.image, self.rect)