from scripts.engine.keys.keys import keys

class Attribute_Distributor():

    def Get_Health(type):
        enemy_types = {
            # [Undead / Crypt]
            keys.skeleton_warrior : 70,
            keys.skeleton_ranger : 40,
            keys.skeleton_cleric : 40,
            keys.skeleton_bell_toller: 60,
            keys.skeleton_undertaker: 110,
            keys.skeleton_guardian: 120,
            keys.skeleton_warlock: 40,
            keys.wight_king: 200,
            keys.skeleton_banner_bearer: 50,
            keys.phantom : 20,
            keys.wraith: 50,
            keys.shade: 50,
            keys.vampire: 150,
            keys.ghoul : 80,

            # [Crystal Caverns]
            keys.fire_spirit: 40,
            keys.ice_spirit: 50,
            keys.earth_elemental: 80,
            keys.electric_elemental: 50,
            keys.poison_elemental: 20,
            keys.medusa: 20,
            keys.minotaur: 20,
            keys.spider: 60,
        }
        # Returns 1 as a safe default if type is not found
        return enemy_types.get(type, 1)
    
    def Get_Soul_Value(type):
        enemy_types = {
            # [Undead / Crypt]
            keys.skeleton_warrior : 10,
            keys.skeleton_ranger : 15,
            keys.skeleton_cleric : 20,
            keys.skeleton_bell_toller: 15,
            keys.skeleton_undertaker: 0.8,
            keys.skeleton_guardian: 15,
            keys.skeleton_warlock: 40,
            keys.wight_king: 55,
            keys.skeleton_banner_bearer: 15,
            keys.phantom : 30,
            keys.wraith: 25,
            keys.shade: 20,
            keys.vampire: 60,
            keys.ghoul : 20,

            # [Crystal Caverns]
            keys.fire_spirit: 20,
            keys.ice_spirit: 20,
            keys.earth_elemental: 30,
            keys.electric_elemental: 30,
            keys.poison_elemental: 10,
            keys.medusa: 60,
            keys.minotaur: 55,
            keys.spider: 20,
        }
        # Returns 1 as a safe default if type is not found
        return enemy_types.get(type, 1)
    
    def Get_Max_Weapon_Charge(type):
        enemy_types = {
            # [Undead / Crypt]
            keys.skeleton_warrior : 0.8,
            keys.skeleton_ranger : 1.2,
            keys.skeleton_cleric : 1.1,
            keys.skeleton_bell_toller: 1.2,
            keys.skeleton_undertaker: 40,
            keys.skeleton_guardian: 1.2,
            keys.skeleton_warlock: 1,
            keys.wight_king: 0.6,
            keys.skeleton_banner_bearer: 1,
            keys.phantom : 0.6,
            keys.wraith: 1,
            keys.shade: 1,
            keys.vampire: 0.5,
            keys.ghoul : 0.8,

            # [Crystal Caverns]
            keys.fire_spirit: 1.4,
            keys.ice_spirit: 1.6,
            keys.earth_elemental: 1.6,
            keys.electric_elemental: 3,
            keys.poison_elemental: 0.1,
            keys.medusa: 0.9,
            keys.minotaur: 0.7,
            keys.spider: 0.9,
        }
        # Returns 1 as a safe default if type is not found
        return enemy_types.get(type, 1)

    def Get_Aggression(type):
        enemy_types = {
        # [Undead / Crypt]
        keys.skeleton_warrior : 7,
        keys.skeleton_ranger : 4,
        keys.skeleton_cleric : 2,
        keys.skeleton_bell_toller: 3,
        keys.skeleton_undertaker: 5,
        keys.skeleton_guardian: 7,
        keys.skeleton_warlock: 6,
        keys.wight_king: 6,
        keys.skeleton_banner_bearer: 2,
        keys.phantom : 10,
        keys.wraith: 8,
        keys.shade: 9,
        keys.vampire: 6,
        keys.ghoul : 8,

        # [Crystal Caverns]
        keys.earth_elemental: 8,
        keys.ice_spirit: 5,
        keys.fire_spirit: 7,
        keys.electric_elemental: 3,
        keys.poison_elemental: 10,
        keys.minotaur: 8,
        keys.medusa: 6,
        }

        return enemy_types.get(type, 1)
    
    def Get_Strength(type):
        enemy_types = {
            # [Undead / Crypt]
            keys.skeleton_warrior : 3,
            keys.skeleton_ranger : 2,
            keys.skeleton_cleric : 1,
            keys.skeleton_bell_toller: 3,
            keys.skeleton_undertaker: 5,
            keys.skeleton_guardian: 4,
            keys.skeleton_warlock: 1,
            keys.wight_king: 6,
            keys.skeleton_banner_bearer: 1,
            keys.phantom : 5,
            keys.wraith: 3,
            keys.shade: 3,
            keys.vampire: 4,
            keys.ghoul : 6,

            # [Crystal Caverns]
            keys.fire_spirit: 4,
            keys.ice_spirit: 7,
            keys.earth_elemental: 7,
            keys.electric_elemental: 4,
            keys.poison_elemental: 4,
            keys.medusa: 4,
            keys.minotaur: 4,
            keys.spider: 4,
        }
        return enemy_types.get(type, 1)

    def Get_Speed(type):
        enemy_types = {
            # [Undead / Crypt]
            keys.skeleton_warrior : 3,
            keys.skeleton_ranger : 4,
            keys.skeleton_cleric : 2,
            keys.skeleton_bell_toller: 3,
            keys.skeleton_undertaker: 2,
            keys.skeleton_guardian: 1,
            keys.skeleton_warlock: 1,
            keys.wight_king: 4,
            keys.skeleton_banner_bearer: 2,
            keys.phantom : 6,
            keys.wraith: 4,
            keys.shade: 1,
            keys.vampire: 3,
            keys.ghoul : 6,

            # [Crystal Caverns]
            keys.fire_spirit: 4,
            keys.ice_spirit: 3,
            keys.earth_elemental: 2,
            keys.electric_elemental: 2,
            keys.poison_elemental: 4,
            keys.medusa: 4,
            keys.minotaur: 4,
            keys.spider: 6,
        }
        return enemy_types.get(type, 1)

    def Get_Agility(type):
        enemy_types = {
            # [Undead / Crypt]
            keys.skeleton_warrior : 2,
            keys.skeleton_ranger : 2,
            keys.skeleton_cleric : 2,
            keys.skeleton_bell_toller: 2,
            keys.skeleton_undertaker: 2,
            keys.skeleton_guardian: 2,
            keys.skeleton_warlock: 2,
            keys.wight_king: 6,
            keys.skeleton_banner_bearer: 2,
            keys.phantom : 2,
            keys.wraith: 2,
            keys.shade: 2,
            keys.vampire: 3,
            keys.ghoul : 2,

            # [Crystal Caverns]
            keys.fire_spirit: 4,
            keys.ice_spirit: 3,
            keys.earth_elemental: 3,
            keys.electric_elemental: 3,
            keys.poison_elemental: 3,
            keys.medusa: 3,
            keys.minotaur: 3,
            keys.spider: 3,
        }
        return enemy_types.get(type, 1)

    def Get_Intelligence(type):
        enemy_types = {
            # [Undead / Crypt]
            keys.skeleton_warrior : 2,
            keys.skeleton_ranger : 2,
            keys.skeleton_cleric : 2,
            keys.skeleton_bell_toller: 2,
            keys.skeleton_undertaker: 2,
            keys.skeleton_guardian: 2,
            keys.skeleton_warlock: 5,
            keys.wight_king: 5,
            keys.skeleton_banner_bearer: 2,
            keys.phantom : 2,
            keys.wraith: 2,
            keys.shade: 2,
            keys.vampire: 2,
            keys.ghoul : 2,

            # [Crystal Caverns]
            keys.fire_spirit: 2,
            keys.ice_spirit: 2,
            keys.earth_elemental: 2,
            keys.electric_elemental: 2,
            keys.poison_elemental: 2,
            keys.medusa: 2,
            keys.minotaur: 2,
            keys.spider: 5,
        }
        return enemy_types.get(type, 1)

    def Get_Stamina(type):
        enemy_types = {
            # [Undead / Crypt]
            keys.skeleton_warrior : 2,
            keys.skeleton_ranger : 2,
            keys.skeleton_cleric : 2,
            keys.skeleton_bell_toller: 2,
            keys.skeleton_undertaker: 2,
            keys.skeleton_guardian: 2,
            keys.skeleton_warlock: 2,
            keys.wight_king: 5,
            keys.skeleton_banner_bearer: 2,
            keys.phantom : 2,
            keys.wraith: 2,
            keys.shade: 2,
            keys.vampire: 2,
            keys.ghoul : 2,

            # [Crystal Caverns]
            keys.fire_spirit: 2,
            keys.ice_spirit: 2,
            keys.earth_elemental: 2,
            keys.electric_elemental: 2,
            keys.poison_elemental: 2,
            keys.medusa: 2,
            keys.minotaur: 2,
            keys.spider: 2,
        }
        return enemy_types.get(type, 1)