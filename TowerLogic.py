import pygame as pg

# ENEMY PATHS WHERE TOWERS CANNOT BE PLACED
ENEMY_PATHS = [
    (0, 200),
    (40, 200),
    (80, 200),
    (80, 160),
    (80, 120),
    (80, 80),
    (120, 80),
    (160, 80),
    (200, 80),
    (200, 120),
    (200, 160),
    (200, 200),
    (200, 240),
    (240, 240),
    (280, 240),
    (320, 240),
    (360, 240),
    (360, 200),
    (360, 160),
    (400, 160),
    (440, 160),
    (480, 160),
    (520, 160),
    (560, 160)
]

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
        
        
    '''
    def attack(self, enemy):
        dx = enemy.x - self.x   # get x distance between enemy and tower
        dy = enemy.y - self.y   # get y distance between enemy and tower
        dist = (dx ** 2 + dy ** 2) ** 0.5  # get distance between enemy and tower
        if dist <= self.range:
            enemy.hp -= self.damage
            return True
        return False
    '''
