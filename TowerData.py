towers_base = {
    "Witch": {
        "range": 120,
        "damage": 10,
        "has_projectile": True,
        "projectile": {
            "name": "fireball",
            "speed": 1,
            "frenetic": True
        },
        "aoeDmg": False,
        "aoeEnv": False,
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
        "has_projectile": True,
        "projectile": {
            "name": "arrow",
            "speed": 10,
            "frenetic": False
        },
        "aoeDmg": False,
        "aoeEnv": False,
        "cooldown": 1.5,
        "cost": 80,
        "upgrades": {
            1: {"cost": 40, "damage": 10, "cooldown": 1.4, "range": 160},
            2: {"cost": 60, "damage": 12, "cooldown": 1.3, "range": 170},
            3: {"cost": 100, "damage": 15, "cooldown": 1.2, "range": 180},
        }
    },
    "Bear": {
        "range": 50,
        "damage": 25,
        "has_projectile": False,
        "projectile": {
            "name": "arrow",
            "speed": 6,
            "frenetic": False
        },
        "aoeDmg": True,
        "aoeEnv": False,
        "cooldown": 2.8,
        "cost": 120,
        "upgrades": {
            1: {"cost": 60, "damage": 28, "cooldown": 2.5, "range": 60},
            2: {"cost": 80, "damage": 35, "cooldown": 2.3, "range": 65},
            3: {"cost": 120, "damage": 45, "cooldown": 2.0, "range": 80},
        }
    },
"Slime": {
        "range": 50,
        "damage": 0,
        "has_projectile": False,
        "projectile": {
            "name": "none",
            "speed": 6,
            "frenetic": False
        },
        "aoeDmg": False,
        "aoeEnv": True,
        "cooldown": 0,
        "cost": 120,
        "upgrades": {
            1: {"cost": 60, "damage": 0, "cooldown": 0, "range": 60},
            2: {"cost": 80, "damage": 0, "cooldown": 0, "range": 80},
            3: {"cost": 120, "damage": 0, "cooldown":0, "range": 120},
        }
    },
    "SuperArcher": {
        "range": 175,
        "damage": 12,
        "has_projectile": True,
        "projectile": {
            "name": "arrow",
            "speed": 50,
            "frenetic": False
        },
        "aoeDmg": False,
        "aoeEnv": False,
        "cooldown": 0.5,
        "cost": 650,
        "upgrades": {
            1: {"cost": 300, "damage": 16, "cooldown": 0.01, "range": 200},
            2: {"cost": 450, "damage": 20, "cooldown": 0.005, "range": 250},
            3: {"cost": 600, "damage": 27, "cooldown": 0.0001, "range": 300},
        }
    },

}

