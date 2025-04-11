import pytest
import pygame
from TowerLogic import Tower
from TowerData import towers_base
from EnemyLogic import Enemy
from EnemyData import mob_data
from UI import draw_tower_stat
from ProjectileLogic import Projectile
from Main import *

# Initialize Pygame for testing
pygame.init()
pygame.display.set_mode((1, 1))  # Minimal display surface for headless testing

def test_tower_initialization():
    screen = None  # Mock screen object
    tower = Tower(100, 100, screen, "Witch")
    
    assert tower.x == 100
    assert tower.y == 100
    assert tower.tower_name == "Witch"
    assert tower.range == towers_base["Witch"]["range"]
    assert tower.damage == towers_base["Witch"]["damage"]
    assert tower.cost == towers_base["Witch"]["cost"]

def test_tower_upgrade():
    screen = None  # Mock screen object
    tower = Tower(100, 100, screen, "Witch")
    
    tower.do_upgrade()
    assert tower.upgrade == 1
    assert tower.damage == towers_base["Witch"]["upgrades"][1]["damage"]
    assert tower.range == towers_base["Witch"]["upgrades"][1]["range"]

    tower.do_upgrade()
    assert tower.upgrade == 2
    assert tower.damage == towers_base["Witch"]["upgrades"][2]["damage"]

def test_tower_sell():
    screen = None  # Mock screen object
    tower = Tower(100, 100, screen, "Witch")
    tower.do_upgrade()
    tower.do_upgrade()

    total_cost = tower.cost
    for i in range(1, tower.upgrade + 1):
        total_cost += towers_base["Witch"]["upgrades"][i]["cost"]

    refund = total_cost // 2
    assert refund == (100 + 50 + 75) // 2  # Testing witch refund after 2 upgrades

def test_enemy_initialization():
    screen = None  # Mock screen object
    enemy = Enemy(0, 0, screen, "Red")
    
    assert enemy.color == "Red"
    assert enemy.hp == mob_data["Red"]["Health"]
    assert enemy.speed == mob_data["Red"]["Speed"]
    assert enemy.money == mob_data["Red"]["Money"]

def test_enemy_movement():
    screen = None  # Mock screen object
    enemy = Enemy(0, 0, screen, "Red")
    initial_x, initial_y = enemy.x, enemy.y

    enemy.move()
    assert (enemy.x, enemy.y) != (initial_x, initial_y)
    
def test_tower_stats_display():
    screen = pygame.Surface((750, 400))  # Mock screen
    tower = Tower(100, 100, screen, "Witch")

    draw_tower_stat(screen, tower)
    # Check if the stats are drawn correctly (e.g., by comparing pixel colors or using a mock)
        
    
def test_wave_progression():
    wave_number = 1
    current_wave_enemies = get_wave_data(wave_number)

    assert len(current_wave_enemies) == 3  # Wave 1 should have 3 enemies
    assert current_wave_enemies == ["Red", "Red", "Red"]