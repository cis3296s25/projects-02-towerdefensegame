towers_base = {
    "Witch": {
        "range": 120,
        "damage": 10,
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
        "projectile": {
            "name": "arrow",
            "speed": 6,
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
"Slow": {
        "range": 50,
        "damage": 0,
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

}

