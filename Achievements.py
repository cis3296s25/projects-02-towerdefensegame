import pygame

achievements = {
    # --- 100% Completion Achievement --- #
    "Master Defender": {
        "unlocked": False,
        "category": "Trophy",
        "description": "Unlock all other achievements",
        "modes": ["all"]
    },

    # --- Combat Achievements --- #
    "First Blood": {
        "unlocked": False,
        "category": "Combat",
        "description": "Kill your first enemy",
        "modes": ["normal"]
    },
    "Wave Warrior": {
        "unlocked": False,
        "category": "Combat",
        "description": "Survive 5 waves",
        "modes": ["normal"]
    },
    "Boss Slayer": {
        "unlocked": False,
        "category": "Combat",
        "description": "Defeat the Shroomgod",
        "modes": ["normal"]
    },
    "Flawless": {
        "unlocked": False,
        "category": "Combat",
        "description": "Beat the game without losing lives",
        "modes": ["normal"]
    },

    "Barely Breathing": {
        "unlocked": False,
        "category": "Combat",
        "description": "Win the game with only 1 life remaining",
        "modes": ["normal"]
    },
    "Raw Power": {
        "unlocked": False,
        "category": "Combat",
        "description": "Beat wave 5 with only base towers",
        "modes": ["normal"]
    },
    "No Upgrades, No Problem": {
        "unlocked": False,
        "category": "Combat",
        "description": "Beat a wave without upgrading a tower",
        "modes": ["normal"]
    },

    # --- Economy Achievements --- #
    "Economist": {
        "unlocked": False,
        "category": "Economy",
        "description": "Win a game with 1000+ unspent gold",
        "modes": ["normal"]
    },
    "Last Cent": {
        "unlocked": False,
        "category": "Economy",
        "description": "Start a wave with exactly 0 money",
        "modes": ["normal"]
    },
    "Oops!": {
        "unlocked": False,
        "category": "Economy",
        "description": "Sell a tower in the middle of a wave",
        "modes": ["normal"]
    },
    "Refund Master": {
        "unlocked": False,
        "category": "Economy",
        "description": "Sell 3 towers in one wave",
        "modes": ["normal"]
    },
    "Tower Tycoon": {
        "unlocked": False,
        "category": "Economy",
        "description": "Place 20 towers on a map at once",
        "modes": ["normal"]
    },

    # --- Tower-Based Achievements --- #
    "Sniper": {
        "unlocked": False,
        "category": "Tower",
        "description": "Kill 10 enemies using only archer towers in a single wave",
        "modes": ["normal"]
    },
    "Balanced Loadout": {
        "unlocked": False,
        "category": "Tower",
        "description": "Complete a round with all types of towers fielded",
        "modes": ["normal"]
    },
    "Bear Force One": {
        "unlocked": False,
        "category": "Tower",
        "description": "Use only bear towers to win a wave",
        "modes": ["normal"]
    },
    "Witching Hour": {
        "unlocked": False,
        "category": "Tower",
        "description": "Deal 300 amount of damage with witch towers in one wave",
        "modes": ["normal"]
    },
    "Splat Specialist": {
        "unlocked": False,
        "category": "Tower",
        "description": "Win a game with more Slime towers than any other tower type",
        "modes": ["normal"]
    },
    "Maxed Out": {
        "unlocked": False,
        "category": "Tower",
        "description": "Fully upgrade a tower",
        "modes": ["normal"]
    },
    "Triple Threat": {
        "unlocked": False,
        "category": "Tower",
        "description": "Fully upgrade 3 towers in the same round",
        "modes": ["normal"]
    },

    # --- Secret Achievements --- #
    "Pacifist": {
        "unlocked": False,
        "category": "Secret",
        "description": "Complete a wave without killing a single enemy",
        "modes": ["normal"]
    },
    "One Man Army": {
        "unlocked": False,
        "category": "Secret",
        "description": "Win a wave with just 1 tower placed",
        "modes": ["normal"]
    },

    # --- No Upgrades Mode Achievements --- #
    "Raw Talent": {
        "unlocked": False,
        "category": "NoUpgrades",
        "description": "Beat the game in No Upgrades Mode",
        "modes": ["no_upgrades_mode"]
    },
    "The Art of Spam": {
        "unlocked": False,
        "category": "NoUpgrades",
        "description": "Place 30+ towers in No Upgrades Mode",
        "modes": ["no_upgrades_mode"]
    },
    "Pure Skill": {
        "unlocked": False,
        "category": "NoUpgrades",
        "description": "Beat No Upgrades Mode without losing any lives",
        "modes": ["no_upgrades_mode"]
    },
    "Tactician's Triumph": {
        "unlocked": False,
        "category": "NoUpgrades",
        "description": "Beat No Upgrades Mode using all tower types",
        "modes": ["no_upgrades_mode"]
    },
    "The Purist": {
        "unlocked": False,
        "category": "NoUpgrades",
        "description": "Beat No Upgrades Mode without selling any towers",
        "modes": ["no_upgrades_mode"]
    },

# --- Hardcore Mode Achievements --- #

    "Iron Shroom": {
    "unlocked": False,
    "category": "Hardcore",
    "description": "Beat the game in Hardcore Mode. Total Perfection.",
    "modes": ["hardcore_mode"]
    },
    "Masochist": {
        "unlocked": False,
        "category": "Hardcore",
        "description": "Lose Hardcore Mode in the first wave",
        "modes": ["hardcore_mode"]
    },
    "You Knew This Was Coming": {
        "unlocked": False,
        "category": "Secret",
        "description": "Try to beat Hardcore Mode with no towers…Why??",
        "modes": ["hardcore_mode"]
    },
    "Flow State": {
        "unlocked": False,
        "category": "Secret",
        "description": "Beat Hardcore Mode without fast-forwarding or pausing the game",
        "modes": ["hardcore_mode"]
    },

    #--- Reverse Mode Achievements ---#
    "Backtrack Boss": {
        "unlocked": False,
        "category": "Reverse",
        "description": "Defeat the Shroomgod in Reverse Mode",
        "modes": ["reverse_mode"]
    },
    "Reverse Sweep": {
        "unlocked": False,
        "category": "Reverse",
        "description": "Lose the first 3 waves in Reverse Mode, then win the game without losing another life",
        "modes": ["reverse_mode"]
    },
    "Reverse Engineering": {
        "unlocked": False,
        "category": "Reverse",
        "description": "Only place towers on the left half of the map in Reverse Mode and win",
        "modes": ["reverse_mode"]
    },
    "True Survivor": {
        "unlocked": False,
        "category": "Secret",
        "description": "Survive Reverse Mode on Hardcore rules… without a single upgrade.",
        "modes": ["reverse_mode"]
    },
    # --- Mode Achievements --- #
    "Challenge Accepted": {
        "unlocked": False,
        "category": "Mode",
        "description": "Play each challenge mode at least once",
        "modes": ["all"]
    },
    "Mode Master": {
        "unlocked": False,
        "category": "Mode",
        "description": "Win a full game in each challenge mode",
        "modes": ["all"]
    },
}


def unlock_achievement(name, notifications_list=None):
    if name in achievements and not achievements[name]["unlocked"]:
        achievements[name]["unlocked"] = True
        print(f"Achievement Unlocked: {name} - {achievements[name]['description']}")

        if notifications_list is not None:
            notifications_list.append((name, pygame.time.get_ticks()))


def check_achievements(state, notifications_list, modes_played_global = None, modes_won_global = None):
    current_mode = state.get("mode", "normal")

    for name, data in achievements.items():
        if data["unlocked"]:
            continue

        allowed_modes = data.get("modes", ["normal"])
        if current_mode not in allowed_modes:
            continue


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
        unlock_achievement("Barely Breathing", notifications_list)

    # Tower usage
    if len(state["tower_types"]) == 5:  # adjust based on # of tower types
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

    if state["tower_types"] == {"Bear"} and state["wave_completed"] and state["wave_kills"] > 0:
        unlock_achievement("Bear Force One", notifications_list)

    if state["upgrades_used"] == 0 and state["wave_completed"] >= 1 and state["towers_placed"] > 0 and state["wave_kills"] > 0:
        unlock_achievement("No Upgrades, No Problem", notifications_list)

    if state["maxed_towers"] >= 1:
        unlock_achievement("Maxed Out", notifications_list)
    
    if state["maxed_towers"] == 3:
        unlock_achievement("Triple Threat", notifications_list)

    if state["kills"] == 0 and state["wave_completed"]:
        unlock_achievement("Pacifist", notifications_list)
    
    if state['wave_completed'] and state["one_tower_challenge"] and state["lives"] == 25:
        unlock_achievement("One Man Army", notifications_list)

    # Slime-specific achievement
    tower_counts = state.get("tower_type_counts", {})
    slime_count = tower_counts.get("Slime", 0)
    other_counts = [
        tower_counts.get("Witch", 0),
        tower_counts.get("Archer", 0),
        tower_counts.get("Bear", 0)
    ]
    if slime_count > max(other_counts) and state.get("game_won"):
        unlock_achievement("Splat Specialist", notifications_list)

# --- No Upgrades Mode Achievements --- #
    if current_mode == "no_upgrades_mode":
        if state["game_won"]:
            unlock_achievement("Raw Talent", notifications_list)

        if state["towers_placed"] >= 30:
            unlock_achievement("The Art of Spam", notifications_list)

        if len(state["tower_types"]) == 4 and state["game_won"]:  # adjust based on # of tower types
            unlock_achievement("Tactician's Triumph", notifications_list)
        
        if state["lives"] == 25 and state["game_won"]:
            unlock_achievement("Pure Skill", notifications_list)
        
        if state["towers_sold"] == 0 and state["game_won"]:
            unlock_achievement("The Purist", notifications_list)
    
# --- Hardcore Mode Achievements --- #    
    if current_mode == "hardcore_mode":
        if state.get("game_won"):
            unlock_achievement("Iron Shroom", notifications_list)
        
        if state.get("game_over") and state.get("lives_lost", 0) >= 1 and state.get("waves_survived", 0) == 0 :
            unlock_achievement("Masochist", notifications_list)

        if state.get("game_over") and state.get("towers_placed", 0) == 0 and state.get("waves_survived", 0) == 0:
            unlock_achievement("You Knew This Was Coming", notifications_list)

        if state.get("game_won") and not state.get("fast_forward_used", False) and not state.get("paused_game", False):
            unlock_achievement("Flow State", notifications_list)

# --- Reverse Mode Achievements --- #

    if current_mode == "reverse_mode":
        if state.get("game_won"):
            unlock_achievement("Backtrack Boss", notifications_list)

        if (state.get("game_won") and state.get("pre_wave_4_kills", 0) == 0 and state.get("lives_lost_after_wave3", 0) == 0):
            unlock_achievement("Reverse Sweep", notifications_list)

        if state["game_won"]:
            all_left = all(x < 320 for x, y in state.get("tower_positions", []))
            if all_left:
                unlock_achievement("Reverse Engineering", notifications_list)
        
        if (state["game_won"] and state["lives"] == 25 and state["upgrades_used"] == 0):
            unlock_achievement("True Survivor", notifications_list)

    if {"no_upgrades_mode", "hardcore_mode", "reverse_mode"}.issubset(modes_played_global or set()):
        unlock_achievement("Challenge Accepted", notifications_list)

    if {"no_upgrades_mode", "hardcore_mode", "reverse_mode"}.issubset(modes_won_global or set()):
        unlock_achievement("Mode Master", notifications_list)

####################### ACHIEVEMENTS ABOVE WORK ### BELOW STILL NEED TESTING ####################################

    # === Check for 100% Completion Trophy ===
    if all(data["unlocked"] or name == "Master Defender" for name, data in achievements.items()):
        unlock_achievement("Master Defender", notifications_list)