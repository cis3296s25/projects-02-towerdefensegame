import os
towers_base = {
    "Witch": {
        "range": 120,
        "damage": 10,
        "projectile": "fireball",
        "cooldown": 2,
        "cost": 100,
        "upgrades": {
            1: {"cost": 50, "damage": 12, "cooldown": 2, "range": 130},
            2: {"cost": 75, "damage": 15, "cooldown": 1.8, "range": 140},
            3: {"cost": 120, "damage": 18, "cooldown": 1.5, "range": 150},
        }
    },
    "Archer": {
        "range": 150,
        "damage": 8,
        "projectile": "arrow",
        "cooldown": 1.5,
        "cost": 80,
        "upgrades": {
            1: {"cost": 40, "damage": 10, "cooldown": 1.4, "range": 160},
            2: {"cost": 60, "damage": 12, "cooldown": 1.3, "range": 170},
            3: {"cost": 100, "damage": 15, "cooldown": 1.2, "range": 180},
        }
    }
}

