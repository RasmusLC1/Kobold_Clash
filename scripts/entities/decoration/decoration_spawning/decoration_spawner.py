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

from .decoration_initialiser import Decoration_Initialiser

from scripts.engine.keys.keys import keys

import random

DUNGEON_REGISTRIES = {
        keys.ancient_tomb: ancient_tomb_registry,
        keys.crystal_caverns: crystal_caverns_registry,
    }

DUNGEON_LIGHT_SOURCES = {
    keys.ancient_tomb: ancient_tomb_light_source_registry,
    keys.crystal_caverns: crystal_cavern_light_source_registry,
}


class Decoration_Spawner():
    def __init__(self, game) -> None:
        self.game = game
        self.decorations = []
        self.bones = []
        self.nearby_decoration_cooldown = 0
        self.saved_data = {}
        self.decoration_initialiser = None
        self.spawn_methods = None


    def Clear_Decorations(self):
        self.decorations.clear()
        self.saved_data.clear()

    def Initialise(self, depth=0):
        self.Get_Dungeon_Type()
        self.decorations = []
        self.decoration_initialiser = Decoration_Initialiser(self.game)  # fresh pool and path cache
        if not self.Spawn_Initial_Decorations():
            return None
        
        return self.decorations, self.spawn_methods


    def Spawn_Initial_Decorations(self):
        decorations_to_spawn = self.decoration_initialiser.Initialise_Dungeon()

        if not decorations_to_spawn:
            print("DEOCRATION SPAWNING FAILED")
            return False

        for decoration_type, tiles in decorations_to_spawn.items():
            for tile in tiles:
                self.Spawn_Deocration(decoration_type, tile.scaled_pos)

        return True


    def Spawn_Deocration(self, type, pos):
        cls = self.spawn_methods.get(type)
        if cls is None:
            print(f"Warning: no spawn method for decoration type '{type}'")
            return
        self.decorations.append(cls(self.game, pos))


    def Get_Dungeon_Type(self):
        dungeon_type = self.game.dungeon_type
        dungeon_registry = DUNGEON_REGISTRIES.get(dungeon_type)
        if dungeon_registry is None:
            raise ValueError(f"No decoration registry found for dungeon type: {dungeon_type}")

        self.spawn_methods = {
            **shared_registry.DECORATION_REGISTRY,
            **dungeon_registry.DECORATION_REGISTRY,
        }
        self._Set_Dungeon_Light_Sources()

    def _Set_Dungeon_Light_Sources(self):
        dungeon_lights = DUNGEON_LIGHT_SOURCES.get(self.game.dungeon_type)

        self.light_source_classes = dict(light_sources_registry.LIGHT_SOURCE_REGISTRY)
        self.light_source_probability = dict(light_sources_registry.LIGHT_SOURCE_PROBABILITY)

        if dungeon_lights is not None:  # no dungeon-specific lights: shared ones only
            self.light_source_classes.update(dungeon_lights.LIGHT_SOURCE_REGISTRY)
            self.light_source_probability.update(dungeon_lights.LIGHT_SOURCE_PROBABILITY)

    

    def All_Spawn_Methods(self):
        return {**self.spawn_methods, **self.light_source_classes}



    def Spawn_Mimic_Chest(self, pos, size=None, version=None, radius=None, level=None):
        mimic_chest = self.spawn_methods.get(keys.mimic_chest)
        if mimic_chest is None:
            print(f"Warning: mimic chest not registered for dungeon type {self.game.dungeon_type}")
            return None
        chest = mimic_chest(self.game, pos)
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
                self.game.decoration_handler.Remove_Decoration(teleport_circle)
                teleportation_circles.remove(teleport_circle)


