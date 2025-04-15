import pygame

achievements = {
    # --- Combat Achievements ---
    "First Blood": {
        "unlocked": False,
        "category": "Combat",
        "description": "Kill your first enemy"
    },
    "Wave Warrior": {
        "unlocked": False,
        "category": "Combat",
        "description": "Survive 5 waves"
    },
    "Boss Slayer": {
        "unlocked": False,
        "category": "Combat",
        "description": "Defeat the Shroomgod"
    },
    "Sporeshield Shatterer": {
        "unlocked": False,
        "category": "Combat",
        "description": "Break the Sporeshield in under 5 seconds (time starts when first bit of damage is dealt)"
    },
    "Flawless": {
        "unlocked": False,
        "category": "Combat",
        "description": "Beat the game without losing lives"
    },

    "Clutch Save": {
        "unlocked": False,
        "category": "Combat",
        "description": "Win the game with only 1 life remaining"
    },
    "Raw Power": {
        "unlocked": False,
        "category": "Combat",
        "description": "Beat wave 5 with only base towers"
    },
    "No Upgrades, No Problem": {
        "unlocked": False,
        "category": "Combat",
        "description": "Beat a wave without upgrading a tower"
    },

    # --- Economy Achievements ---
    "Economist": {
        "unlocked": False,
        "category": "Economy",
        "description": "Win a game with 1000+ unspent gold"
    },
    "Last Cent": {
        "unlocked": False,
        "category": "Economy",
        "description": "Start a wave with exactly 0 money"
    },
    "Oops!": {
        "unlocked": False,
        "category": "Economy",
        "description": "Sell a tower in the middle of a wave"
    },
    "Refund Master": {
        "unlocked": False,
        "category": "Economy",
        "description": "Sell 3 towers in one wave"
    },
    "Tower Tycoon": {
        "unlocked": False,
        "category": "Economy",
        "description": "Place 20 towers on a map at once"
    },

    # --- Tower-Based Achievements ---
    "Sniper": {
        "unlocked": False,
        "category": "Tower",
        "description": "Kill 10 enemies using only archer towers in a single wave"
    },
    "Balanced Loadout": {
        "unlocked": False,
        "category": "Tower",
        "description": "Complete a round with all types of towers fielded"
    },
    "Bear Force One": {
        "unlocked": False,
        "category": "Tower",
        "description": "Use only bear towers to win a wave"
    },
    "Witching Hour": {
        "unlocked": False,
        "category": "Tower",
        "description": "Deal 300 amount of damage with witch towers in one wave"
    },
    "Maxed Out": {
        "unlocked": False,
        "category": "Tower",
        "description": "Fully upgrade a tower"
    },
    "Triple Threat": {
        "unlocked": False,
        "category": "Tower",
        "description": "Fully upgrade 3 towers in the same round"
    },

    # --- Secret Achievements ---
    "Pacifist": {
        "unlocked": False,
        "category": "Secret",
        "description": "Complete a wave without killing a single enemy"
    },
    "Speedrunner": {
        "unlocked": False,
        "category": "Secret",
        "description": "Beat the game in under X minutes"
    },
    "One Man Army": {
        "unlocked": False,
        "category": "Secret",
        "description": "Win a wave with just 1 tower placed"
    }
}


def unlock_achievement(name, notifications_list=None):
    if name in achievements and not achievements[name]["unlocked"]:
        achievements[name]["unlocked"] = True
        print(f"Achievement Unlocked: {name} - {achievements[name]['description']}")

        if notifications_list is not None:
            notifications_list.append((name, pygame.time.get_ticks()))
    print("[DEBUG] Notifications List:", notifications_list)



def check_achievements(state, notifications_list):
    # Kill-based
    if state["kills"] >= 1:
        unlock_achievement("First Blood", notifications_list)
    # Wave-based
    if state["waves_survived"] >= 5:
        unlock_achievement("Wave Warrior", notifications_list)

    # Boss kill
    if state["boss_defeated"]:
        unlock_achievement("Boss Slayer", notifications_list)

    # Money-based
    if state["gold"] >= 1000 and state["game_won"]:
        unlock_achievement("Economist", notifications_list)

    if state["lives"] == 25 and state["game_won"]:
        unlock_achievement("Flawless", notifications_list)

    if state["lives"] == 1 and state["game_won"]:
        unlock_achievement("Clutch Save", notifications_list)

    # Tower usage
    if len(state["tower_types"]) == 3:  # adjust based on # of tower types
        unlock_achievement("Balanced Loadout", notifications_list)

    if state["towers_placed"] >= 20:
        unlock_achievement("Tower Tycoon", notifications_list)

    # Selling towers
    if state["towers_sold_this_wave"] >= 3:
        unlock_achievement("Refund Master", notifications_list)

    if state["sold_mid_wave"]:
        unlock_achievement("Oops!", notifications_list)
    
    if state["start_money"] == 0 and state["wave_completed"]:
        unlock_achievement("Last Cent", notifications_list)

    if state["wave"] == 6 and state["upgrades_used"] == 0:
        unlock_achievement("Raw Power", notifications_list)
    
    if state["archer_wave_kills"] >= 10:
        unlock_achievement("Sniper", notifications_list)

    if state["witch_dmg_this_wave"] >= 300:
        unlock_achievement("Witching Hour", notifications_list)

    if state["tower_types"] == {"Bear"} and state["wave_completed"]:
        unlock_achievement("Bear Force One", notifications_list)

    if state["upgrades_used"] == 0 and state["wave_completed"] >= 1 and state["towers_placed"] > 0:
        unlock_achievement("No Upgrades, No Problem", notifications_list)

    if state["maxed_towers"] >= 1:
        unlock_achievement("Maxed Out", notifications_list)
    
    if state["maxed_towers"] == 3:
        unlock_achievement("Triple Threat", notifications_list)

    if state["kills"] == 0 and state["wave_completed"]:
        unlock_achievement("Pacifist", notifications_list)
    
    if state['wave_completed'] and state["one_tower_challenge"] and state["lives"] == 25:
        unlock_achievement("One Man Army", notifications_list)

####################### ACHIEVEMENTS ABOVE WORK ### BELOW STILL NEED TESTING ####################################

