import pygame
from pygame import mouse

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class Tower:
    def __init__(self, x, y, range, damage, cooldown):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.cooldown = cooldown

    def draw(self):
        # Green square as a tower
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 40, 40))



def draw_grid():
    for x in range(0, 650, 40):
        for y in range(0, 600, 40):
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 40, 40), 1)

class Enemy:
    # added color and rect as inputs for more precise tuning
    def __init__(self, hp, range, dmg, color, rect, cooldown):
        self.hp = hp
        self.range = range
        self.dmg = dmg
        self.cooldown = cooldown
        self.rect = rect
        self.color = color

    def draw(self):
        # Red square as a Enemy
        # Changed from hard coded red square to color of choice
        pygame.draw.rect(screen, self.color, self.rect)


# Create a tower object
tower = Tower(200, 200, 100, 10, 2)
enemy = Enemy(50, 10, 5,(255, 0, 0),(400, 200, 40, 40), 3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Register mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos #using position of the mouse at time of event
            grid_x = mouse_x // 40 # calculate the grid x
            grid_y = mouse_y // 40 # and y position to...
            grid_cell = (grid_x, grid_y) # ...generate a cell
            if grid_cell == (10, 5): # if the generated cell is the same cell as the enemy
                enemy.hp -= 10 # decrement enemy's health by 10
        if enemy.hp <= 0:
            # if the hp drops to 0 or less, update the enemy's color
            enemy = Enemy(50, 10, 5,(0, 0, 0),(400, 200, 40, 40), 3)
            enemy.draw() # and re-draw it

    screen.fill((0, 0, 0))
    draw_grid()
    tower.draw()  # draw tower 
    enemy.draw()  # draw enemy
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
