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
screen = pygame.display.set_mode((750, 400))
clock = pygame.time.Clock()

IMG_NAMES = [
    "enemySample40x40",
    "mapSample",
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

class Map:
    def __init__(self):
        self.image = IMAGES["mapSample"]

    def draw(self):
        screen.blit(self.image, (0, 0))

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
    grid_surface = pygame.Surface((800, 600), pygame.SRCALPHA)  # Create a transparent surface
    grid_surface.set_alpha(15)  # Set transparency (0 = fully transparent, 255 = fully opaque)

    for x in range(0, 600, 40):
        for y in range(0, 600, 40):
            pygame.draw.rect(grid_surface, (255, 255, 255, 100), (x, y, 40, 40), 1)  # Draw on transparent surface

    screen.blit(grid_surface, (0, 0))

class Enemy:
    def __init__(self, x, y, hp, range, dmg, cooldown):
        self.hp = hp
        self.range = range
        self.dmg = dmg
        self.cooldown = cooldown
        self.x = x
        self.y = y
        self.image = IMAGES["enemySample40x40"]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        #pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 40, 40))  # Red square as a Enemy
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y + 45, 40, 5))  # HP Bar Background White
        hpPercentage = self.hp / 50 # Max HP: 50 = 100%
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + 45, 40 * hpPercentage, 5))  # HP Bar Green

def homescreen():
    #fonts
    title_font = pygame.font.SysFont("Arial", 60)
    smaller_font = pygame.font.SysFont("Arial", 20)
    #title
    title_text = title_font.render("My Tower Defense", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30))
    #instruction
    start_text = smaller_font.render("Press SPACE or Click to Start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
    
    screen.fill((0, 0, 0))
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    pygame.display.flip()
    
def draw_sidebar():
    pygame.draw.rect(screen, (50, 50, 50), (600, 0, 150, 400))
    
    font = pygame.font.SysFont("Arial", 18)
    
    # text
    text_Lives = font.render("Lives: 0.01", True, (255, 255, 255))  
    text_Money = font.render("Money: 69", True, (255, 255, 255))  # (text, antialias, color, background=None)
    text_tower = font.render("Towers", True, (255, 255, 255))  
    
    
    screen.blit(text_Lives, (610, 10))  # Position the Money text
    screen.blit(text_Money, (610, 30))  # Position the Money text
    screen.blit(text_tower, (610, 60))  # Position the Tower text
    pygame.draw.line(screen, (255, 255, 255), (610, 85), (740, 85), 1) # Draw a line below the Tower text (surface, color, start_pos, end_pos, width)


def game():
    tower = Tower(160, 160, 100, 10, 2)
    enemy = Enemy(200, 80, 50, 10, 5, 3)
    map = Map()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        map.draw()
        draw_sidebar()
        draw_grid()
        tower.draw()  # draw tower
        enemy.draw()  # draw enemy
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    


def main():
    homescreen()  # Show the home screen at the start
    waiting_for_input = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Wait for SPACE key press to start the game
                    waiting_for_input = False
                    game()  # Start the game loop

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Wait for mouse click to start the game (optional)
                    waiting_for_input = False
                    game()  # Start the game loop

if __name__ == "__main__":
    main()