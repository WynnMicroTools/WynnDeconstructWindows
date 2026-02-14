import json
import heapq
import sys
import itertools
import math
import os
# import statistics
from itertools import combinations_with_replacement, permutations
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)
with open(resource_path("ingreds_dict.json"), "r") as file:
    ingreds_dict = json.load(file)
with open(resource_path("ingreds_ids_map.json"), "r") as f:
    ingreds_ids_map = json.load(f)
id_map = {
    "jh": "jump height",
    "eSteal": "stealing",
    "maxMana": "max mana",
    "kb": "knock back",
    "nMdRaw": "neutral melee damage raw",
    "aMdRaw": "air melee damage raw",
    "eMdRaw": "earth melee damage raw",
    "tMdRaw": "thunder melee damage raw",
    "fMdRaw": "fire melee damage raw",
    "wMdRaw": "water melee damage raw",
    "aSdRaw": "air spell damage raw",
    "eSdRaw": "earth spell damage raw",
    "tSdRaw": "thunder spell damage raw",
    "fSdRaw": "fire spell damage raw",
    "wSdRaw": "water spell damage raw",
    "sprint": 'sprint bonus',
    "sprintReg": "sprint regen bonus",
    "damPct": "damage%",
    "nDamRaw": "neutral damage raw",
    "expd": "exploding",
    "aSdPct": "air spell damage%",
    "eSdPct": "earth spell damage%",
    "tSdPct": "thunder spell damage%",
    "fSdPct": "fire spell damage%",
    "wSdPct": "water spell damage%",
    "fDamRaw": "fire damage raw",
    "wDamRaw": "water damage raw",
    "tDamRaw": "thunder damage raw",
    "eDamRaw": "earth damage raw",
    "aDamRaw": "air damage raw",
    "hprRaw": "raw health regen",
    "xpb": "combat xp bonus",
    "poison": "poison",
    "ls": "life steal",
    "atkTier": "attack speed bonus",
    "aDamPct": "air damage%",
    "fDamPct": "fire damage%",
    "wDamPct": "water damage%",
    "tDamPct": "thunder damage%",
    "eDamPct": "earth damage%",
    "rDamPct": "elemental damage%",
    "aDefPct": "air defense%",
    "fDefPct": "fire defense%",
    "wDefPct": "water defense%",
    "tDefPct": "thunder defense%",
    "eDefPct": "earth defense%",
    "rDefPct": "elemental defense%",
    "agi": "agility",
    "def": "defense",
    "dex": "dexterity",
    "int": "intelligence",
    "str": "strength",
    "sdPct": "spell damage%",
    "mdPct": "melee damage%",
    "sdRaw": "spell damage raw",
    "mdRaw": "melee damage raw",
    "gXp": "gathering xp bonus",
    "gSpd": "gathering speed bonus",
    "hprPct": "health regen%",
    "mr": "mana regen",
    "ms": "mana steal",
    "thorns": "thorns",
    "ref": "reflection",
    "spd": "walk speed bonus",
    "healPct": "heal effectiveness%",
    "lb": "loot bonus",
    "hpBonus": "health bonus",
    "lq": "loot quality",
}
inv_id_map = {
  "jump height": "jh",
  "stealing": "eSteal",
  "max mana": "maxMana",
  "knock back": "kb",
  "neutral melee damage raw": "nMdRaw",
  "air melee damage raw": "aMdRaw",
  "earth melee damage raw": "eMdRaw",
  "thunder melee damage raw": "tMdRaw",
  "fire melee damage raw": "fMdRaw",
  "water melee damage raw": "wMdRaw",
  "air spell damage raw": "aSdRaw",
  "earth spell damage raw": "eSdRaw",
  "thunder spell damage raw": "tSdRaw",
  "fire spell damage raw": "fSdRaw",
  "water spell damage raw": "wSdRaw",
  "sprint bonus": "sprint",
  "sprint regen bonus": "sprintReg",
  "damage %": "damPct",
  "neutral damage raw": "nDamRaw",
  "exploding": "expd",
  "air spell damage %": "aSdPct",
  "earth spell damage %": "eSdPct",
  "thunder spell damage %": "tSdPct",
  "fire spell damage %": "fSdPct",
  "water spell damage %": "wSdPct",
  "fire damage raw": "fDamRaw",
  "water damage raw": "wDamRaw",
  "thunder damage raw": "tDamRaw",
  "earth damage raw": "eDamRaw",
  "air damage raw": "aDamRaw",
  "raw health regen": "hprRaw",
  "combat xp bonus": "xpb",
  "poison": "poison",
  "life steal": "ls",
  "attack speed bonus": "atkTier",
  "air damage %": "aDamPct",
  "fire damage %": "fDamPct",
  "water damage %": "wDamPct",
  "thunder damage %": "tDamPct",
  "earth damage %": "eDamPct",
  "elemental damage %": "rDamPct",
  "air defense %": "aDefPct",
  "fire defense %": "fDefPct",
  "water defense %": "wDefPct",
  "thunder defense %": "tDefPct",
  "earth defense %": "eDefPct",
  "elemental defense %": "rDefPct",
  "agility": "agi",
  "defense": "def",
  "dexterity": "dex",
  "intelligence": "int",
  "strength": "str",
  "spell damage %": "sdPct",
  "melee damage %": "mdPct",
  "spell damage raw": "sdRaw",
  "melee damage raw": "mdRaw",
  "gathering xp bonus": "gXp",
  "gathering speed bonus": "gSpd",
  "health regen %": "hprPct",
  "mana regen": "mr",
  "mana steal": "ms",
  "thorns": "thorns",
  "reflection": "ref",
  "walk speed bonus": "spd",
  "heal effectiveness %": "healPct",
  "loot bonus": "lb",
  "health bonus": "hpBonus",
  "loot quality": "lq"
}
meta_items = ['Alginate Dressing', 'Amber-Encased Fleris', 'Ancient Spring Water', 'Aspect of the Void', 'Blessed Heart', "Bob's Tear", 'Borange Fluff', 'Claw of Demise', 'Coagulated Soulmass', 'Coalescence', 'Decaying Heart', 'Disturbed Dye', 'Dizzying Void', 'Dominant Force', 'Doom Stone', 'Draconic Bone Marrow', 'Etheric Fern', 'Eye of The Beast', 'Familiar Essence', 'Festering Face', 'Frenetic Heart', 'Golden Avia Feather', 'Infected Mass', 'Lashing Hellfire', 'Luminous Rune', 'Lunar Charm', "Major's Badge", 'Negative Rafflesia', 'Obelisk Core', 'Old Treasure֎', 'Parasitic Abscission', 'Peculiar Oddity', 'Plasteel Plating', 'Pride of the Heights', 'Sentient Magmatic Gem', 'Thermal Replication', 'Transformativity', 'Unicorn Horn', 'Unsettling Void', 'Warm Fleris', 'Zealous Illuminator']
meta_ranges = {
  "Alginate Dressing": {
    "min": -110,
    "max": 55
  },
  "Amber-Encased Fleris": {
    "min": 0,
    "max": 15
  },
  "Ancient Spring Water": {
    "min": 10,
    "max": 20
  },
  "Aspect of the Void": {
    "min": 0,
    "max": 125
  },
  "Blessed Heart": {
    "min": -40,
    "max": 0
  },
  "Bob's Tear": {
    "min": 0,
    "max": 25
  },
  "Borange Fluff": {
    "min": 15,
    "max": 15
  },
  "Claw of Demise": {
    "min": -65,
    "max": 0
  },
  "Coagulated Soulmass": {
    "min": 0,
    "max": 25
  },
  "Coalescence": {
    "min": -240,
    "max": 0
  },
  "Decaying Heart": {
    "min": -100,
    "max": 60
  },
  "Disturbed Dye": {
    "min": -50,
    "max": 0
  },
  "Dizzying Void": {
    "min": -115,
    "max": 115
  },
  "Dominant Force": {
    "min": -75,
    "max": 70
  },
  "Doom Stone": {
    "min": -100,
    "max": 60
  },
  "Draconic Bone Marrow": {
    "min": 0,
    "max": 30
  },
  "Etheric Fern": {
    "min": -45,
    "max": 115
  },
  "Eye of The Beast": {
    "min": -100,
    "max": 0
  },
  "Familiar Essence": {
    "min": -40,
    "max": -40
  },
  "Festering Face": {
    "min": -40,
    "max": 0
  },
  "Frenetic Heart": {
    "min": -35,
    "max": 50
  },
  "Golden Avia Feather": {
    "min": 0,
    "max": 25
  },
  "Infected Mass": {
    "min": -25,
    "max": 0
  },
  "Lashing Hellfire": {
    "min": 0,
    "max": 55
  },
  "Luminous Rune": {
    "min": 0,
    "max": 30
  },
  "Lunar Charm": {
    "min": 25,
    "max": 25
  },
  "Major's Badge": {
    "min": -145,
    "max": 20
  },
  "Negative Rafflesia": {
    "min": -145,
    "max": 155
  },
  "Obelisk Core": {
    "min": -200,
    "max": 0
  },
  "Old Treasure\u058e": {
    "min": -40,
    "max": 0
  },
  "Parasitic Abscission": {
    "min": -137,
    "max": -15
  },
  "Peculiar Oddity": {
    "min": -120,
    "max": 60
  },
  "Plasteel Plating": {
    "min": -160,
    "max": 0
  },
  "Pride of the Heights": {
    "min": 0,
    "max": 130
  },
  "Sentient Magmatic Gem": {
    "min": 0,
    "max": 25
  },
  "Thermal Replication": {
    "min": 15,
    "max": 15
  },
  "Transformativity": {
    "min": -25,
    "max": -25
  },
  "Unicorn Horn": {
    "min": 25,
    "max": 50
  },
  "Unsettling Void": {
    "min": -200,
    "max": 0
  },
  "Warm Fleris": {
    "min": -10,
    "max": 0
  },
  "Zealous Illuminator": {
    "min": 0,
    "max": 25
  }
}
normalized_ids_dict = {
  "damPct": {
    "min": 21.0,
    "max": 21.0
  },
  "hpBonus": {
    "min": -1450.0,
    "max": 2025.0
  },
  "agi": {
    "min": -6.5,
    "max": 11.5
  },
  "def": {
    "min": -6.5,
    "max": 11.5
  },
  "str": {
    "min": -9.0,
    "max": 13.0
  },
  "sdPct": {
    "min": -20.0,
    "max": 23.0
  },
  "dex": {
    "min": -5.5,
    "max": 13.0
  },
  "int": {
    "min": -8.0,
    "max": 10.0
  },
  "mdPct": {
    "min": -20.0,
    "max": 40.0
  },
  "poison": {
    "min": -330.0,
    "max": 6700.0
  },
  "ls": {
    "min": -105.0,
    "max": 172.5
  },
  "mr": {
    "min": -7.5,
    "max": 12.0
  },
  "sdRaw": {
    "min": -97.5,
    "max": 87.5
  },
  "mdRaw": {
    "min": -80.0,
    "max": 125.0
  },
  "gSpd": {
    "min": -3.5,
    "max": 9.5
  },
  "hprRaw": {
    "min": -140.0,
    "max": 135.0
  },
  "thorns": {
    "min": -13.5,
    "max": 40.0
  },
  "eDamPct": {
    "min": -11.0,
    "max": 18.0
  },
  "eDefPct": {
    "min": -17.5,
    "max": 26.0
  },
  "healPct": {
    "min": -9.0,
    "max": 13.0
  },
  "nDamRaw": {
    "min": -40.0,
    "max": -40.0
  },
  "aDamPct": {
    "min": -9.0,
    "max": 20.0
  },
  "fDamPct": {
    "min": -5.0,
    "max": 24.5
  },
  "wDamPct": {
    "min": -9.0,
    "max": 19.0
  },
  "tDamPct": {
    "min": -9.0,
    "max": 18.5
  },
  "ms": {
    "min": -4.0,
    "max": 8.0
  },
  "sprintReg": {
    "min": -1.0,
    "max": 17.5
  },
  "spd": {
    "min": -12.0,
    "max": 26.0
  },
  "expd": {
    "min": 3.5,
    "max": 22.5
  },
  "wSdRaw": {
    "min": 50.0,
    "max": 50.0
  },
  "gXp": {
    "min": -4.5,
    "max": 5.5
  },
  "rDamPct": {
    "min": -3.5,
    "max": 12.5
  },
  "rDefPct": {
    "min": -12.5,
    "max": 6.5
  },
  "lb": {
    "min": -3.0,
    "max": 11.0
  },
  "lq": {
    "min": 1.0,
    "max": 4.5
  },
  "hprPct": {
    "min": -22.0,
    "max": 20.0
  },
  "aDefPct": {
    "min": -8.5,
    "max": 27.5
  },
  "fDefPct": {
    "min": -22.0,
    "max": 32.5
  },
  "wDefPct": {
    "min": -27.5,
    "max": 26.0
  },
  "tDefPct": {
    "min": -7.0,
    "max": 17.5
  },
  "ref": {
    "min": -11.0,
    "max": 21.0
  },
  "tDamRaw": {
    "min": 24.0,
    "max": 24.0
  },
  "atkTier": {
    "min": -2.0,
    "max": 1.0
  },
  "xpb": {
    "min": -15.0,
    "max": 14.0
  },
  "maxMana": {
    "min": 10.0,
    "max": 10.0
  },
  "fSdRaw": {
    "min": 52.5,
    "max": 55.0
  },
  "kb": {
    "min": 1.5,
    "max": 2.5
  },
  "tMdRaw": {
    "min": 22.0,
    "max": 22.0
  },
  "fDamRaw": {
    "min": 9.0,
    "max": 37.5
  },
  "wDamRaw": {
    "min": 9.0,
    "max": 22.5
  },
  "eSteal": {
    "min": -1.5,
    "max": 6.5
  },
  "jh": {
    "min": 1.0,
    "max": 1.0
  },
  "eMdRaw": {
    "min": 15.0,
    "max": 45.0
  },
  "wMdRaw": {
    "min": 17.0,
    "max": 132.5
  },
  "eSdRaw": {
    "min": 52.5,
    "max": 52.5
  },
  "aDamRaw": {
    "min": 22.5,
    "max": 22.5
  },
  "sprint": {
    "min": 2.0,
    "max": 15.0
  },
  "aSdPct": {
    "min": 7.5,
    "max": 7.5
  },
  "wSdPct": {
    "min": 8.0,
    "max": 8.0
  },
  "eSdPct": {
    "min": -9.0,
    "max": -9.0
  },
  "fSdPct": {
    "min": 7.5,
    "max": 7.5
  },
  "nMdRaw": {
    "min": 32.5,
    "max": 32.5
  },
  "fMdRaw": {
    "min": 12.0,
    "max": 12.0
  }
}
skill_types = {
    "helment": "ARMORING",
    "chestplate": "ARMORING",
    "leggings": "TAILORING",
    "boots": "TAILORING",
    "spear": "WEAPONSMITHING",
    "dagger": 'WEAPONSMITHING',
    "bow": "WOODWORKING",
    "wand": "WOODWORKING",
    "relik": "WOODWORKING",
    "ring": "JEWELING",
    "bracelet": "JEWELING",
    "necklace": "JEWELING",
    "alchemism": "POTIONS",
    "scroll": "SCRIBING",
    "food": "COOKING"

    
}
class WeightedQueue:
    def __init__(self):
        self._queue = []
        self._counter = itertools.count()
    def push(self, item, weight):
        count = next(self._counter)
        heapq.heappush(self._queue, (weight, count, item))

    def pop(self):
        return heapq.heappop(self._queue)[2]
    def weighted_pop(self):
        item = heapq.heappop(self._queue)
        return [item[0], item[2]]
    def is_empty(self):
        return not self._queue
    def peek(self):
        if not self._queue:
            return None
        return self._queue[0]
def get_potential_items(solve_item, item_type):
    filtered_item_type = skill_types[item_type]
    filtered_items = sorted(solve_item.keys())
    def rec_search(search_terms, ingreds_map):
        if "list" in ingreds_map:
            results = [i for i in ingreds_map["list"]]
            if "dict" not in ingreds_map:
                return results
        else:
            results = []
        for item in search_terms:
            # result = []
            # print(ingreds_map["dict"])
            # print(item in ingreds_map["dict"].keys())
            if item in ingreds_map["dict"]:
                results += rec_search(search_terms=search_terms[1:], ingreds_map=ingreds_map["dict"][item]) 
        return results
    potential_items = rec_search(search_terms=filtered_items, ingreds_map=ingreds_ids_map)
    potential_items = [i for i in potential_items if filtered_item_type in ingreds_dict[i]["skills"] and i not in meta_items]
    return potential_items
def combo_value_calc_dumb(ingredients):#smarter way to do it would be to not treat every item like it could be max
    meta_ings = [i for i in ingredients if i in meta_items]
    meta_max = 0
    meta_min = 0
    values = {}
    for ing in meta_ings:
        ing_range = meta_ranges[ing]
        # print(ing_range)
        ing_max = ing_range["max"]
        ing_min = ing_range["min"]
        if ing_max > 0:
            if meta_max > 0:
                meta_max += ing_max
            else:
                meta_max = ing_max
        else:
            if meta_max < 0 and ing_max  > meta_max:
                meta_max = ing_max
        if ing_min < 0:
            if meta_min < 0:
                meta_min += ing_min
            else:
                meta_min = ing_min
        else:
            if meta_min > 0 and ing_min < meta_min:
                meta_min = ing_min
    meta_max = meta_max/100
    meta_min = meta_min/100
    # print(f"meta_max: {meta_max}")
    # print(f'meta_min: {meta_min}')
    for ing in ingredients:
        ing_ids = ingreds_dict[ing]["ids"]
        # print(ing)
        # print(ing_ids)
        if not ing_ids:
            continue
        for id in ing_ids.keys():
            if id not in values:
                values[id] = {"max": 0, "min": 0}
            val_range = values[id]
            id_max = ing_ids[id]["maximum"]
            id_min = ing_ids[id]["minimum"]
            max_mod = id_max * (1 + meta_max)
            if id_max > max_mod:
                max_mod = id_max
            if id_max * (1 + meta_min) > max_mod:
                max_mod = id_max * (1 + meta_min)
            if id_min * (1 + meta_min) > max_mod:
                max_mod = id_min * (1 + meta_min)
            min_mod = id_min * (1 + meta_max)
            if id_min < min_mod:
                min_mod = id_min
            if id_min * (1 + meta_max) < min_mod:
                min_mod = id_min * (1 + meta_min)
            if id_max * (1 + meta_min) < min_mod:
                min_mod = id_max * (1 + meta_min)
            val_range["max"] += max_mod
            val_range["min"] += min_mod
    return values
def hard_solve(ingredients, solve_item):
    meta_ings = {}
    ings = {}
    
    
    for ing in [i for i in ingredients if i in meta_items]:
        meta_ings[ing] = {
        "left": ingreds_dict[ing]["posMods"]["left"]  / 100,
        "right": ingreds_dict[ing]["posMods"]["right"] / 100,
        "above": ingreds_dict[ing]["posMods"]["above"] / 100,
        "under": ingreds_dict[ing]["posMods"]["under"] / 100,
        "touching": ingreds_dict[ing]["posMods"]["touching"] / 100,
        "notTouching": ingreds_dict[ing]["posMods"]["notTouching"] / 100,
        }
   
    for ing in ingredients:
        ings[ing] = ingreds_dict[ing]["ids"]
    while len(ingredients) < 6:
        ingredients.append(None)
    counter = 0
    for perm in permutations(ingredients):
        # print(counter)
        counter += 1
        item_ranges = {}
        multiplier_map = [1, 1, 1, 1, 1, 1]
        for i in range(len(perm)):
            ing = perm[i]
            if ing in meta_items:
                modified = [False, False, False, False, False, False]
                modified[i] = True
                if i%2 == 0:
                    multiplier_map[i+1] = round(meta_ings[ing]['right'] + meta_ings[ing]['touching'] + multiplier_map[i+1], 2)
                    modified[i+1] = True
                else:
                    multiplier_map[i-1] = round(meta_ings[ing]["left"] + meta_ings[ing]['touching'] + multiplier_map[i-1], 2)
                    modified[i-1] = True
                if i > 1:
                    multiplier_map[i-2] = round(meta_ings[ing]['above'] + meta_ings[ing]['touching'] + multiplier_map[i-2], 2)
                    modified[i-2] = True
                if i > 3:
                    multiplier_map[i-4] = round(meta_ings[ing]['above'] + multiplier_map[i-4], 2)
                if i < 2: 
                    multiplier_map[i+4] = round(meta_ings[ing]['under'] + multiplier_map[i+4], 2)
                if i < 4: 
                    multiplier_map[i+2] = round(meta_ings[ing]['under'] + meta_ings[ing]['touching'] + multiplier_map[i+2], 2)
                    modified[i+2] = True
                for j in range(len(modified)):
                    modded = modified[j]
                    if not modded:
                        multiplier_map[j] = round(meta_ings[ing]["notTouching"] + multiplier_map[j], 2)
                # if all([a == b for a, b in zip(perm, ["Decaying Heart", "Bob's Tear", "Negative Rafflesia", "Mega Fern", "Crystalline Growth", "Crystalline Growth"])]):  
                #     print(f"Multiplier map after applying: {ing}")
                #     print(multiplier_map)
        for i in range(len(perm)):
            ing = perm[i]
            if ing is not None and ingreds_dict[ing]['ids']:
                for id in ingreds_dict[ing]['ids'].keys():
                    if id not in item_ranges:
                        item_ranges[id] = {"min": 0, "max": 0}
                    
                    max_range = ingreds_dict[ing]['ids'][id]['maximum'] * multiplier_map[i]
                    min_range = ingreds_dict[ing]['ids'][id]['minimum'] * multiplier_map[i]
                    # if id=="mr" and all([a == b for a, b in zip(perm, [ "Decaying Heart", "Elephelk Trunk", "Negative Rafflesia", "Mega Fern", "Crystalline Growth", "Crystalline Growth"])]):
                    #     print(f"ing: {ing}, id: {id}, max_range: {max_range}, min_range: {min_range}")
                    max_range = math.floor(max_range)
                    min_range = math.floor(min_range)
                    # min_range = math.ceil(min_range)
                    # max_range = math.ceil(max_range)
                    if max_range > min_range:
                        item_ranges[id]['max'] = item_ranges[id]['max'] + max_range
                        item_ranges[id]['min'] = item_ranges[id]['min'] + min_range
                        
                    else:
                        item_ranges[id]['min'] = item_ranges[id]['min'] + max_range
                        item_ranges[id]['max'] = item_ranges[id]['max'] + min_range
                    # print(f"ing_name: {ing}, id: {id},ing_max: {ingreds_dict[ing]['ids'][id]['maximum']}, multiplier: {multiplier_map[i]}, result: {ingreds_dict[ing]['ids'][id]['maximum'] * multiplier_map[i]}")
                    # print(f"ing_name: {ing}, id: {id},ing_max: {ingreds_dict[ing]['ids'][id]['minimum']}, multiplier: {multiplier_map[i]}, result: {ingreds_dict[ing]['ids'][id]['minimum'] * multiplier_map[i]}")
        del_id = []
        for id in item_ranges:
            item_min = math.floor(item_ranges[id]['min'])
            item_max = math.floor(item_ranges[id]['max'])
            # item_min = math.ceil(item_ranges[id]['min'])
            # item_max = math.ceil(item_ranges[id]['max'])
            # item_max = item_ranges[id]['max']
            # item_min = item_ranges[id]['min']
            
            if item_min == 0 and item_max == 0:
                del_id.append(id)
            else:
                item_ranges[id]['min'] = item_min
                item_ranges[id]['max'] = item_max
        for id in del_id:
            del item_ranges[id]
        match = True
        # print(match)
        # if all([a == b for a, b in zip(perm, ["Decaying Heart", "Bob's Tear", "Negative Rafflesia", "Mega Fern", "Crystalline Growth", "Crystalline Growth"])]):
        #     print("=========== start ================ ")
        #     print(perm)
        #     print(f"fulltruth: {len(item_ranges) == len(solve_item) and len([i for i in solve_item.keys() if i in item_ranges.keys()]) == len(solve_item)}")
        #     print(len([i for i in solve_item.keys() if i in item_ranges.keys()]) == len(solve_item))
        #     print(len(item_ranges) == len(solve_item))
            
        #     print(f"item_rangs: {item_ranges}")
        #     print(f"solve_item: {solve_item}")
        #     print(f'multiplier_map: {multiplier_map}')
        #     print("============= end ============")
        # print(item_ranges)
        if len(item_ranges) == len(solve_item) and len([i for i in solve_item.keys() if i in item_ranges.keys()]) == len(solve_item):
            for id in item_ranges.keys():
                id_range = item_ranges[id]
                item_val = solve_item[id]
                # print(f"item_val: {item_val}, id range: {id_range}")
                if item_val < id_range['min'] or item_val > id_range['max']:
                    # print("hit this")
                    # if all([a == b for a, b in zip(perm, ["Archaic Medallion", "Obelisk Core", "Archaic Medallion", "Obelisk Core", "Major's Badge", "Old Treasure֎"])]):
                    #     print(item_ranges)
                    #     print(f"{id}: {item_val}, range: {id_range}")
                    #     print(f"max comparison: {item_val >= id_range['max']}, min comparison: {item_val < id_range['min']}")
                    match = False
                    break
        else:
            match = False
        if match:
            return perm
def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
def normalize_range(solve_range):
    normalized_range = {}
    for id in solve_range.keys():
        normalized_range[id] = {}
        id_min = normalized_ids_dict[id]['min']
        id_max = normalized_ids_dict[id]['max']
        if id_min == id_max:
            normalized_range[id]["max"] = solve_range[id]['max']/id_min
            normalized_range[id]["min"] = solve_range[id]['min']/id_min
        else:
            normalized_range[id]['max'] = (solve_range[id]['max'] - id_min) / (id_max - id_min)
            normalized_range[id]['min'] = (solve_range[id]['min'] - id_min) / (id_max - id_min)
    return normalized_range
def normalize_item(solve_item):
    normalized_item = {}
    for id in solve_item.keys():
        id_min = normalized_ids_dict[id]['min']
        id_max = normalized_ids_dict[id]['max']
        if id_min == id_max:
            normalized_item[id] = solve_item[id]/id_min
        else:
            normalized_item[id] = (solve_item[id] - id_min) / (id_max - id_min)
    return normalized_item
def range_item_distance(solve_item, solve_range, use_normalization=False):
    ids = list(set(solve_item.keys()) | set(solve_range.keys()))
    n = len(ids)
    range_vect = [0]*n
    item_vect = [0]*n
    
    # Apply normalization if enabled
    if use_normalization:
        normalized_range = normalize_range(solve_range)
        normalized_item = normalize_item(solve_item)
    else:
        normalized_range = solve_range
        normalized_item = solve_item
    modified = 0
    for id in ids:
        # Get values without mutating originals
        item_val = normalized_item.get(id, 0)
        range_val = normalized_range.get(id, {"min": 0, "max": 0})
        if item_val == 0 or (range_val['min']==0 and range_val['max']==0):
            modified += 1
        norm_min = range_val['min']
        norm_max = range_val['max']
        
        item_vect.append(item_val)
        
        if norm_min <= item_val <= norm_max:
            range_vect.append(item_val)
        else:
            if abs(norm_min - item_val) > abs(norm_max - item_val):
                range_vect.append(norm_max)
            else:
                range_vect.append(norm_min)
    
    return (modified + .5) * euclidean_distance(range_vect, item_vect)
from multiprocessing import Pool, Manager
import multiprocessing as mp

def search_from_seed(args):
    ing, potential_items, meta_items_filtered, solve_item, item_type, all_items, item_to_idx, combinations = args
    
    pq = WeightedQueue()
    solution = None
    counter = 0
    potential_counter = 0
    
    item_range = combo_value_calc_dumb([ing])
    dist = range_item_distance(solve_item, item_range)
    
    if dist == 0:
        solution = hard_solve([ing], solve_item=solve_item)
        if solution is not None:
            return solution, counter, potential_counter
    
    pq.push(
        item=[sorted([ing] + list(i), key=lambda x: item_to_idx[x]) for i in combinations],
        weight=dist
    )
    
    while not pq.is_empty():
        dequed = pq.weighted_pop()
        ingredients_list = dequed[1]
        
        for ingredients in ingredients_list:
            counter += 1
            ranges = combo_value_calc_dumb(ingredients=ingredients)
            dist = range_item_distance(solve_item=solve_item, solve_range=ranges, use_normalization=False)
            
            if dist == 0:
                solution = hard_solve(ingredients=ingredients, solve_item=solve_item)
                potential_counter += 1
                if solution is not None:
                    return solution, counter, potential_counter
            
            if len(ingredients) < 6:
                last_ing = max(ingredients, key=lambda x: item_to_idx[x])
                last_ing_idx = item_to_idx[last_ing]
                new_combinations = [
                    sorted(ingredients + [all_items[i]], key=lambda x: item_to_idx[x])
                    for i in range(last_ing_idx, len(all_items))
                ]
                pq.push(item=new_combinations, weight=dist)
    
    return None, counter, potential_counter


def reverse_engineer(solve_item, item_type):
    print(solve_item)
    print(item_type)
    potential_items = get_potential_items(solve_item=solve_item, item_type=item_type)
    meta_items_list = ['Alginate Dressing', 'Amber-Encased Fleris', 'Ancient Spring Water', 'Aspect of the Void', 'Blessed Heart', "Bob's Tear", 'Borange Fluff', 'Claw of Demise', 'Coagulated Soulmass', 'Coalescence', 'Decaying Heart', 'Disturbed Dye', 'Dizzying Void', 'Dominant Force', 'Doom Stone', 'Draconic Bone Marrow', 'Etheric Fern', 'Eye of The Beast', 'Familiar Essence', 'Festering Face', 'Frenetic Heart', 'Golden Avia Feather', 'Infected Mass', 'Lashing Hellfire', 'Luminous Rune', 'Lunar Charm', "Major's Badge", 'Negative Rafflesia', 'Obelisk Core', 'Old Treasure֎', 'Parasitic Abscission', 'Peculiar Oddity', 'Plasteel Plating', 'Pride of the Heights', 'Sentient Magmatic Gem', 'Thermal Replication', 'Transformativity', 'Unicorn Horn', 'Unsettling Void', 'Warm Fleris', 'Zealous Illuminator']
 
    filtered_item_type = skill_types[item_type]
    meta_items_filtered = [i for i in meta_items_list if filtered_item_type in ingreds_dict[i]["skills"]]
    
    n = len(potential_items) + len(meta_items_filtered)
    k = 6
    combs_len = math.comb(n + k - 1, k)
    print(f"Potential combinations: {combs_len}")
    
    all_items = potential_items + meta_items_filtered
    item_to_idx = {item: idx for idx, item in enumerate(all_items)}
    combinations = list(combinations_with_replacement(all_items, 3))
    
    # Build args for each seed ingredient
    args_list = [
        (ing, potential_items, meta_items_filtered, solve_item, item_type, all_items, item_to_idx, combinations)
        for ing in potential_items
    ]
    
    # Use pool with early termination
    num_cores = mp.cpu_count()
    # print(f"Using {num_cores} cores")
    
    with Pool(processes=num_cores) as pool:
        for result, counter, potential_counter in pool.imap_unordered(search_from_seed, args_list):
            if result is not None:
                pool.terminate()  # Stop all workers once solution found
                print(f"Found solution after {counter} combinations and {potential_counter} hard solves")
                return result
    
    return None

# examples = []

# examples.append(({"raw health regen": 200, "health bonus": 1200, "mana regen": 18, "spell damage raw": 300, "melee damage raw": 140, "water defense %": -4, "earth defense %": -4}, "leggings"))
# examples.append(({"raw health regen": 210, "health bonus": 1300, "mana regen": 20, "spell damage raw": 300, "melee damage raw": 140}, "leggings"))
# examples.append(({"health regen %": -40, "spell damage %": 20, "combat xp bonus": -2, "loot bonus": -2}, "necklace"))
# examples.append(({"strength": 4, "dexterity": 2, "mana regen": 8, "spell damage %": 2, "elemental damage %": 14, "fire defense %": -10, "water defense %": -10, "thunder defense %": -10, "air defense %": -10, "earth defense %": -10}, "ring"))
# examples.append(({"health bonus": -1600, "heal effectiveness %": -5, "mana regen": 10, "spell damage raw": 90, "spell damage %": 14, "fire damage %": 60, "water damage %": -8, "water defense %": -4, "earth defense %": -4, "gathering xp bonus": 4}, "leggings"))


# import time
# average_time = []
# for example in examples:
#     example_item = example[0]
#     item_type = example[1]
#     example_item = {inv_id_map[k]: v for k,v in example_item.items()}
#     before = time.time()
#     solution = reverse_engineer(example_item, item_type)
#     time_taken = time.time() - before
#     average_time.append(time_taken)
#     print(f"time to solve: {time_taken}")
#     print(solution)
#     print("+=====================================+")
# print(f"Average time taken: {statistics.mean(average_time)}")