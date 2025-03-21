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

#code for background music
pygame.mixer.init()
pygame.mixer.music.load(BASE_PATH + "/sounds/backgroundmusic.mp3")
pygame.mixer.music.set_volume(0.5)


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


def pause_screen():
    pygame.mixer.music.pause() 

    # Create a transparent overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  
    overlay.fill((0, 0, 0, 150))  
    font = pygame.font.SysFont("Arial", 50)
    pause_text = font.render("Game Paused", True, (255, 255, 255))
    resume_text = pygame.font.SysFont("Arial", 30).render("Press ESC to Resume", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
    screen.blit(overlay, (0, 0))  
    screen.blit(pause_text, pause_rect)
    screen.blit(resume_text, resume_rect)
    pygame.display.flip() 

    # Pause gameloop
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    paused = False
    
    pygame.mixer.music.unpause()


def game():
    pygame.mixer.music.play(-1) #plays music after leaving homescreen

    tower = Tower(160, 160, 100, 10, 2)
    enemy = Enemy(200, 80, 50, 10, 5, 3)
    map = Map()

    # Load and scale speaker icons
    speaker_img_muted = pygame.transform.scale(
        pygame.image.load(IMAGE_PATH + "mute.png").convert_alpha(), (24, 24)
    )
    speaker_img_low = pygame.transform.scale(
        pygame.image.load(IMAGE_PATH + "low-volume.png").convert_alpha(), (24, 24)
    )
    speaker_img_medium = pygame.transform.scale(
        pygame.image.load(IMAGE_PATH + "medium-volume.png").convert_alpha(), (24, 24)
    )
    speaker_img_high = pygame.transform.scale(
        pygame.image.load(IMAGE_PATH + "high-volume.png").convert_alpha(), (24, 24)
    )

    # Volume/mute state
    muted = False
    volume = 0.5
    pygame.mixer.music.set_volume(volume)

    # Volume slider setup (placed inside sidebar area)
    slider_rect = pygame.Rect(20, screen.get_height() - 40, 100, 10)
    handle_rect = pygame.Rect(slider_rect.x + int(slider_rect.width * volume) - 5, slider_rect.y - 5, 10, 20)
    dragging_volume = False

    # Placeholder for speaker icon rect (will be updated dynamically)
    speaker_rect = pygame.Rect(0, 0, 24, 24)  # placeholder; will update dynamically below



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press 'ESC' to pause
                    pause_screen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_rect.collidepoint(event.pos):
                    dragging_volume = True
                elif speaker_rect.collidepoint(event.pos):
                    muted = not muted
                    pygame.mixer.music.set_volume(0 if muted else volume)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_volume = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_volume:
                    mouse_x = event.pos[0]
                    new_volume = max(0, min(1, (mouse_x - slider_rect.x) / slider_rect.width))
                    volume = new_volume
                    if not muted:
                        pygame.mixer.music.set_volume(volume)
                    handle_rect.x = slider_rect.x + int(slider_rect.width * volume) - 5


        screen.fill((0, 0, 0))
        map.draw()
        draw_sidebar()
        draw_grid()
        tower.draw()  # draw tower
        enemy.draw()  # draw enemy

         # Volume slider bar
        pygame.draw.rect(screen, (200, 200, 200), slider_rect)  # Bar background
        pygame.draw.rect(screen, (100, 100, 255), (slider_rect.x, slider_rect.y, int(slider_rect.width * volume), slider_rect.height))  # Volume fill
        pygame.draw.rect(screen, (255, 255, 255), handle_rect)  # Slider handle

        # Choose which speaker icon to display
        if muted:
            speaker_img = speaker_img_muted
        elif volume <= 0.33:
            speaker_img = speaker_img_low
        elif volume <= 0.66:
            speaker_img = speaker_img_medium
        else:
            speaker_img = speaker_img_high

        # Position speaker icon next to slider
        speaker_rect = speaker_img.get_rect(topleft=(slider_rect.x + slider_rect.width + 10, slider_rect.y - 6))
        screen.blit(speaker_img, speaker_rect)


        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
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