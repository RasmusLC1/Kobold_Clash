from scripts.entities.decoration.light_sources import light_sources_registry
from scripts.entities.decoration.light_sources import load_all

from scripts.entities.decoration.light_sources.crystal_caverns import light_sources_registry as crystal_cavern_light_source_registry
from scripts.entities.decoration.light_sources.crystal_caverns import load_all

from scripts.entities.decoration.light_sources.ancient_tomb import light_sources_registry as ancient_tomb_light_source_registry
from scripts.entities.decoration.light_sources.ancient_tomb import load_all


from scripts.entities.decoration.shared import shared_registry
from scripts.entities.decoration.shared import load_all

from scripts.entities.decoration.ancient_tomb import ancient_tomb_registry
from scripts.entities.decoration.ancient_tomb import load_all


from scripts.entities.decoration.crystal_caverns import crystal_caverns_registry
from scripts.entities.decoration.crystal_caverns import load_all


from scripts.entities.decoration.decoration_initialiser.crypt_decoration_initialiser import Crypt_Decoration_Initialiser
from scripts.entities.decoration.decoration_initialiser.crystal_cavern_decoration_initialiser import Crystal_Cavern_Decoration_Initialiser

from scripts.engine.keys.keys import keys

import random

DUNGEON_REGISTRIES = {
        keys.ancient_crypt: ancient_tomb_registry,
        keys.crystal_caverns: crystal_caverns_registry,
    }

DUNGEON_LIGHT_SOURCES = {
    keys.ancient_crypt: ancient_tomb_light_source_registry,
    keys.crystal_caverns: crystal_cavern_light_source_registry,
}


class Decoration_Spawner():
    def __init__(self, game) -> None:
        self.game = game
        self.decoration_initialiser = None
        self.decorations = []
        self.bones = []
        self.nearby_decoration_cooldown = 0
        self.saved_data = {}

        self.spawn_methods = None

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
        return self.decorations, self.item_sacrifice, self.spawn_methods

    

    def Get_Dungeon_Type(self):
        dungeon_specific_registry = DUNGEON_REGISTRIES.get(self.game.dungeon_type, {})
        self.spawn_methods = {**shared_registry, **dungeon_specific_registry}

        decoration_initialisers = {
            keys.ancient_crypt: Crypt_Decoration_Initialiser,
            keys.crystal_caverns: Crystal_Cavern_Decoration_Initialiser,
        }
        initaliser_type = decoration_initialisers.get(self.game.dungeon_type)
        self.decoration_initialiser = initaliser_type(self.game)

        dungeon_light_sources = DUNGEON_LIGHT_SOURCES.get(self.game.dungeon_type, {})
        self.light_source_classes = {**light_sources_registry.LIGHT_SOURCE_REGISTRY, **dungeon_light_sources.LIGHT_SOURCE_REGISTRY}
        self.light_source_probability = {**light_sources_registry.LIGHT_SOURCE_PROBABILITY, **dungeon_light_sources.LIGHT_SOURCE_PROBABILITY}


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



    def Spawn_Lightsource(self):
        if keys.light_source not in self.decoration_initialiser.decorations:
            return

        for pos in self.decoration_initialiser.decorations[keys.light_source]:
            type = random.choices(
                population=list(self.light_source_probability.keys()),
                weights=list(self.light_source_probability.values()),
                k=1
            )[0]

            if type == keys.torch:
                self.game.item_handler.weapon_handler.Weapon_Spawner(keys.torch, pos[0], pos[1])
                continue

            cls = self.light_source_classes.get(type)
            if cls is None:
                print(f"Warning: light source type '{type}' not recognized.")
                continue

            light_source = cls(self.game, pos)
            self.decorations.append(light_source)

            
    
    def Spawn_Mimic_Chest(self, pos, size=None, version=None, radius=None, level=None):
        mimic_chest = self.spawn_methods.get(keys.mimic_chest)
        if mimic_chest is None:
            print(f"Warning: mimic chest not registered for dungeon type {self.game.dungeon_type}")
            return None
        chest = mimic_chest(self.game, pos, size=size, version=version, radius=radius, level=level)
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
