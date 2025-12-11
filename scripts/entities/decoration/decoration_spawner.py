from scripts.entities.decoration.ancient_tomb.loot_container.vase import Vase
from scripts.entities.decoration.ancient_tomb.loot_container.effigy_tomb import Effigy_Tomb
from scripts.entities.decoration.ancient_tomb.shrine.rune_shrine import Rune_Shrine
from scripts.entities.decoration.ancient_tomb.loot_container.bookshelf import Bookshelf
from scripts.entities.decoration.ancient_tomb.light_sources.brazier import Brazier
from scripts.entities.decoration.ancient_tomb.shrine.blood_shrine import Blood_Shrine
from scripts.entities.decoration.shared.shrine.sacrifice_shrine import Sacrifice_Shrine


from scripts.entities.decoration.shared.shrine.portal_shrine import Portal_Shrine
from scripts.entities.decoration.shared.shrine.soul_well import Soul_Well
from scripts.entities.decoration.shared.shrine.hunter_shrine import Hunter_Shrine
from scripts.entities.decoration.shared.bones.bones import Bones
from scripts.entities.decoration.shared.loot_container.chest import Chest
from scripts.entities.decoration.shared.loot_container.mimic_chest import Mimic_Chest
from scripts.entities.decoration.shared.loot_container.weapon_rack import Weapon_rack
from scripts.entities.decoration.shared.loot_container.plinth import Plinth
from scripts.entities.decoration.shared.loot_container.potion_table import Potion_Table
from scripts.entities.decoration.shared.doors.door import Door
from scripts.entities.decoration.shared.doors.fragile_wall import Fragile_Wall
from scripts.entities.decoration.shared.boss_room.boss_room import Boss_Room
from scripts.entities.decoration.shared.interactive.lever import Lever
from scripts.entities.decoration.shared.interactive.teleportation_circle import Teleportation_Circle
from scripts.entities.decoration.shared.interactive.campfire import Campfire

from scripts.entities.decoration.decoration_initialiser.crypt_decoration_initialiser import Crypt_Decoration_Initialiser
from scripts.entities.decoration.decoration_initialiser.crystal_cavern_decoration_initialiser import Crystal_Cavern_Decoration_Initialiser
from scripts.engine.keys.keys import keys

import random

class Decoration_Spawner():
    def __init__(self, game) -> None:
        self.game = game
        self.decoration_initialiser = None
        self.decorations = []
        self.bones = []
        self.nearby_decoration_cooldown = 0
        self.saved_data = {}

        self.spawn_methods = None


        self.light_sources = {
            keys.torch : 0.1,
            keys.brazier : 0.3,
        }

        self.item_sacrifice = []


    def Clear_Decorations(self):
        self.decorations.clear()
        self.saved_data.clear()

    def Initialise(self, depth=0):
        self.Get_Dungeon_Type()
        self.Generic_Spawn(self.spawn_methods.keys())
        self.Spawn_Lightsource()
        self.Set_Item_Sacrifice_Decorations()
        self.Link_Teleportation_Circles()
        self.Spawn_Items()
        return self.decorations, self.item_sacrifice, self.spawn_methods


    def Get_Dungeon_Type(self):
        # Shared decorations for all dungeons
        shared_spawns = {
            keys.door_basic: Door,
            keys.fragile_wall: Fragile_Wall,
            keys.chest: Chest,
            keys.vase: Vase,
            keys.potion_table: Potion_Table,
            keys.portal_shrine: Portal_Shrine,
            keys.hunter_shrine: Hunter_Shrine,
            keys.soul_well: Soul_Well,
            keys.bones: Bones,
            keys.weapon_rack: Weapon_rack,
            keys.plinth: Plinth,
            keys.lever: Lever,
            keys.teleportation_circle: Teleportation_Circle,
            keys.campfire: Campfire,
            keys.torch: None,
        }

        # Dungeon-specific decorations
        dungeon_specific = {
            keys.ancient_crypt: {
                keys.effigy_tomb: Effigy_Tomb,
                keys.rune_shrine: Rune_Shrine,
                keys.blood_shrine: Blood_Shrine,
                keys.sacrifice_shrine: Sacrifice_Shrine,
                keys.bookshelf: Bookshelf,
                keys.brazier: Brazier,
            },
            keys.crystal_caverns: {
                # Add crystal-specific ones if needed
            }
        }

        # Merge shared + dungeon-specific
        # ** unpacks the key-value pairs from a dictionary and then merges them
        dungeon_types = {
            key: {**shared_spawns, **dungeon_specific.get(key, {})}
            for key in [keys.ancient_crypt, keys.crystal_caverns]
        }

        decoration_initialisers = {
            keys.ancient_crypt: Crypt_Decoration_Initialiser,
            keys.crystal_caverns: Crystal_Cavern_Decoration_Initialiser,
        }

        self.spawn_methods = dungeon_types.get(self.game.dungeon_type)
        initaliser_type = decoration_initialisers.get(self.game.dungeon_type)
        self.decoration_initialiser = initaliser_type(self.game)


    def Generic_Spawn(self, types):
        for t in types:
            if t not in self.decoration_initialiser.decorations:
                continue
            cls = self.spawn_methods.get(t)
            if cls is None:
                continue
            for pos in self.decoration_initialiser.decorations[t]:
                decoration = cls(self.game, pos)
                self.decorations.append(decoration)

    def Spawn_Items(self):
        for decoration in self.decorations:
            if decoration.type == keys.weapon_rack:
                decoration.Spawn_Weapons()
                continue

            if decoration.type == keys.plinth:
                decoration.Spawn_Rune()

    
    def Spawn_Lightsource(self):
        if not keys.light_source in self.decoration_initialiser.decorations:
            return
        for pos in self.decoration_initialiser.decorations[keys.light_source]:

            # Type needs to be reset
            type = random.choices(
                population=list(self.light_sources.keys()),
                weights=list(self.light_sources.values()),
                k=1
            )[0]

            if type == keys.torch:
                self.game.item_handler.weapon_handler.Weapon_Spawner(keys.torch, pos[0], pos[1])
            else:
                light_source = Brazier(self.game, pos)
                self.decorations.append(light_source)
    
    def Spawn_Mimic_Chest(self, pos, size=None, version=None, radius=None, level=None):
        chest = Mimic_Chest(self.game, pos)  
        self.decorations.append(chest)
        return chest
   

    
    def Link_Teleportation_Circles(self):
        teleportation_circles = []
        for decoration in self.decorations:
            if not decoration.type == keys.teleportation_circle:
                continue

            teleportation_circles.append(decoration)

        random.shuffle(teleportation_circles)  # Randomly pair circles

        for i in range(0, len(teleportation_circles) - 1, 2):
            a = teleportation_circles[i]
            b = teleportation_circles[i + 1]
            a.Set_Linked_Portal(b)
            b.Set_Linked_Portal(a)

        for teleport_circle in teleportation_circles:
            if not teleport_circle.linked_portal:
                self.Remove_Decoration(teleport_circle)
                teleportation_circles.remove(teleport_circle)


    def Set_Item_Sacrifice_Decorations(self):
        item_sacrifice_decorations = [
            keys.soul_well,
            keys.hunter_shrine,
            keys.sacrifice_shrine,
        ]

        for decoration in self.decorations:
            if decoration.type in item_sacrifice_decorations:
                self.item_sacrifice.append(decoration)