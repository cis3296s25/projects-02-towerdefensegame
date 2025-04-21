towers_base = {
    "Witch": {
        "range": 120,
        "damage": 27,
        "has_projectile": True,
        "projectile": {
            "name": "fireball",
            "speed": 1,
            "frenetic": True
        },
        "aoeDmg": False,
        "aoeEnv": False,
        "cooldown": 3,
        "cost": 100,
        "upgrades": {
            1: {"cost": 30, "damage": 27, "cooldown": 3, "range": 135},
            2: {"cost": 60, "damage": 27, "cooldown": 3, "range": 150},
            3: {"cost": 120, "damage": 28, "cooldown": 2, "range": 150},
        }
    },
    "Archer": {
        "range": 150,
        "damage": 5,
        "has_projectile": True,
        "projectile": {
            "name": "arrow",
            "speed": 6,
            "frenetic": False
        },
        "aoeDmg": False,
        "aoeEnv": False,
        "cooldown": 1,
        "cost": 60,
        "upgrades": {
            1: {"cost": 20, "damage": 8, "cooldown": 1, "range": 160},
            2: {"cost": 40, "damage": 8, "cooldown": 1, "range": 180},
            3: {"cost": 80, "damage": 10, "cooldown": 1, "range": 180},
        }
    },
    "Bear": {
        "range": 80,
        "damage": 15,
        "has_projectile": False,
        "projectile": {
            "name": "arrow",
            "speed": 6,
            "frenetic": False
        },
        "aoeDmg": True,
        "aoeEnv": False,
        "cooldown": 2,
        "cost": 60,
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

}

