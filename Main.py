import pygame
import os #required for .exe creation
import sys #required for .exe creation
from pygame import(
    image,
    mixer,
)
from EnemyLogic import Enemy
from TowerLogic import Tower
from MapLogic import Map
from UI import homescreen, pause_screen, draw_sidebar, draw_grid
from os.path import abspath, dirname

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + "/images/"

pygame.init()

#code for background music
mixer.init()
mixer.music.load(BASE_PATH + "/sounds/backgroundmusic.mp3")
mixer.music.set_volume(0.5)


screen = pygame.display.set_mode((750, 400))
clock = pygame.time.Clock()

IMG_NAMES = [
    "enemySample40x40",
    "mapSample",
    "towerSample",
]
IMAGES = {
    name: image.load(IMAGE_PATH + "{}.png".format(name)).convert_alpha()
    for name in IMG_NAMES
}
enemyImage = IMAGES["enemySample40x40"] #generate enemy image
towerImage = IMAGES["towerSample"] #generate tower image
mapSample = IMAGES["mapSample"] #generate map image

#Allows us to wrap the game into a .exe file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def game():
    mixer.music.play(-1) #plays music after leaving homescreen

    tower = Tower(160, 160, 100, 10, 2, screen, towerImage)
    enemy = Enemy(200, 80, 50, 10, 5, 3, screen, enemyImage)
    gameMap = Map(screen, mapSample)

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
    mixer.music.set_volume(volume)

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
                    pause_screen(screen, mixer)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_rect.collidepoint(event.pos):
                    dragging_volume = True
                elif speaker_rect.collidepoint(event.pos):
                    muted = not muted
                    mixer.music.set_volume(0 if muted else volume)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_volume = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_volume:
                    mouse_x = event.pos[0]
                    new_volume = max(0, min(1, (mouse_x - slider_rect.x) / slider_rect.width))
                    volume = new_volume
                    if not muted:
                        mixer.music.set_volume(volume)
                    handle_rect.x = slider_rect.x + int(slider_rect.width * volume) - 5

        screen.fill((0, 0, 0))
        gameMap.draw()
        draw_sidebar(screen)
        draw_grid(screen)
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

    mixer.music.stop()
    pygame.quit()

def main():
    homescreen(screen)  # Show the home screen at the start
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
