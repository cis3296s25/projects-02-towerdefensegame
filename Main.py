import pygame
import os #required for .exe creation
import sys #required for .exe creation
from pygame import(
    image,
)
from os.path import abspath, dirname

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + "/images/"

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

IMG_NAMES = [
    "enemySample40x40",
]
IMAGES = {
    name: image.load(IMAGE_PATH + "{}.png".format(name)).convert_alpha()
    for name in IMG_NAMES
}

#Allows us to wrap the game into a .exe file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Tower:
    def __init__(self, x, y, range, damage, cooldown):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.cooldown = cooldown

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 40, 40))  # Green square as a tower

def draw_grid():
    for x in range(0, 650, 40):
        for y in range(0, 600, 40):
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 40, 40), 1)

class Enemy:
    def __init__(self, hp, range, dmg, cooldown):
        self.hp = hp
        self.range = range
        self.dmg = dmg
        self.cooldown = cooldown
        self.x, self.y = 400, 200  # enemy position
        self.image = IMAGES["enemySample40x40"]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        #pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 40, 40))  # Red square as a Enemy
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y + 45, 40, 5))  # HP Bar Background White
        hpPercentage = self.hp / 50 # Max HP: 50 = 100%
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + 45, 40 * hpPercentage, 5))  # HP Bar Green

tower = Tower(200, 200, 100, 10, 2)
enemy = Enemy(50, 10, 5, 3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_grid()
    tower.draw()  # draw tower
    enemy.draw()  # draw enemy
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
