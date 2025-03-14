import pygame

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

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (400, 200, 40, 40))  # Red square as a Enemy

# Create a tower object
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
