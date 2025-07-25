from scripts.entities.decoration.bones.bones import Bones
from scripts.entities.decoration.loot_container.chest import Chest
from scripts.entities.decoration.loot_container.mimic_chest import Mimic_Chest
from scripts.entities.decoration.loot_container.weapon_rack import Weapon_rack
from scripts.entities.decoration.loot_container.plinth import Plinth
from scripts.entities.decoration.loot_container.vase import Vase
from scripts.entities.decoration.loot_container.effigy_tomb import Effigy_Tomb
from scripts.entities.decoration.loot_container.potion_table import Potion_Table
from scripts.entities.decoration.doors.door import Door
from scripts.entities.decoration.shrine.rune_shrine import Rune_Shrine
from scripts.entities.decoration.shrine.portal_shrine import Portal_Shrine
from scripts.entities.decoration.shrine.soul_well import Soul_Well
from scripts.entities.decoration.shrine.hunter_shrine import Hunter_Shrine
from scripts.entities.decoration.shrine.sacrifice_shrine import Sacrifice_Shrine
from scripts.entities.decoration.boss_room.boss_room import Boss_Room
from scripts.entities.decoration.light_sources.brazier import Brazier
from scripts.entities.decoration.interactive.teleportation_circle import Teleportation_Circle
from scripts.entities.decoration.loot_container.bookshelf import Bookshelf
from scripts.entities.decoration.decoration_initialiser import Decoration_Initialiser

import random
import math
from scripts.engine.keys.keys import keys

class Decoration_Handler():
    def __init__(self, game) -> None:
        self.game = game
        self.decoration_initialiser = Decoration_Initialiser(game)
        self.decorations = []
        self.teleportation_circles = []
        self.bones = []
        self.nearby_decoration_cooldown = 0
        self.saved_data = {}

        self.spawn_methods = {
            keys.door_basic: Door,
            keys.chest: Chest,
            keys.vase: Vase,
            keys.effigy_tomb: Effigy_Tomb,
            keys.potion_table: Potion_Table,
            keys.rune_shrine: Rune_Shrine,
            keys.portal_shrine: Portal_Shrine,
            keys.hunter_shrine: Hunter_Shrine,
            keys.sacrifice_shrine: Sacrifice_Shrine,
            keys.soul_well: Soul_Well,
            keys.bones: Bones,
            keys.weapon_rack: Weapon_rack,
            keys.plinth: Plinth,
            keys.bookshelf: Bookshelf,
            keys.teleportation_circle: Teleportation_Circle,
            keys.brazier: Brazier,
            keys.torch : None,
        }


        self.light_sources = {
            keys.torch : 0.1,
            keys.brazier : 0.3,

        }

        self.item_sacrifice = []


    def Clear_Decorations(self):
        self.decorations.clear()
        self.saved_data.clear()

    def Initialise(self, depth=0):
        self.Spawn_Chest()
        self.Spawn_Vase()
        self.Spawn_Lightsource()
        self.Spawn_Effigy_Tomb()
        self.Set_Item_Sacrifice_Decorations()
        self.Spawn_Portal_Shrine()
        self.Spawn_Sacrifice_Shrine()
        self.Spawn_Soul_Well()
        self.Spawn_Hunter_Shrine()
        self.Spawn_Teleportation_Circle()
        
        self.Spawn_Items()

        self.Spawn_Rooms()


    def Spawn_Items(self):
        for decoration in self.decorations:
            if decoration.type == keys.weapon_rack:
                decoration.Spawn_Weapons()
                continue

            if decoration.type == keys.plinth:
                decoration.Spawn_Rune()

    def Get_Random_Decoration_Of_Type(self, type):
        decorations_with_type = []
        for decoration in self.decorations:
            if decoration.type in type:
                decorations_with_type.append(decoration)

        if not decorations_with_type:
            return None

        return random.choice(decorations_with_type)
    

    def Set_Item_Sacrifice_Decorations(self):
        item_sacrifice_decorations = [
            keys.soul_well,
            keys.hunter_shrine,
            keys.sacrifice_shrine,
        ]

        for decoration in self.decorations:
            if decoration.type in item_sacrifice_decorations:
                self.item_sacrifice.append(decoration)

    def Set_Chest_Version(self, depth = 1):
        i = 0
        while i < 9:
            version = i
            if random.randint(depth, max(depth + 5, 10)) < max(depth + 2, 5):
                break
            i += 1
        return version  

    def Save_Decoration_Data(self):
        for decoration in self.decorations:
            decoration.Save_Data()
            self.saved_data[decoration.ID] = decoration.saved_data

    def Load_Data(self, data):
        for ID, item_data in data.items():
            if not item_data:
                continue
            try:
                type = item_data[keys.type]
                pos = item_data[keys.pos]
                size = item_data.get('size')
                version = item_data.get('version')
                radius = item_data.get('radius')
                level = item_data.get('level')
                self.Decoration_Spawner(type, pos, size=size, version=version, radius=radius, level=level, data=item_data)
            except Exception as e:
                print("DATA WRONG DECORATION HANDLER", item_data, e)

    def Decoration_Spawner(self, type, pos, size=None, version=None, radius=None, level=None, data=None):
        spawn_function = self.spawn_methods.get(type)
        if not spawn_function:
            print(f"Warning: Decoration type '{type}' not recognized. Decoration_Handler Decoration_Spawner")
            return None
        decoration = spawn_function(self.game, pos)
        if decoration:
            if data:
                decoration.Load_Data(data)
        self.decorations.append(decoration)
        return decoration

    def Spawn_Door(self, pos, size, version=None, radius=None, level=None):
        door = Door(self.game, keys.door_basic, pos, size)
        self.decorations.append(door)
        return door

    def Spawn_Chest(self):
        for chest_pos in self.decoration_initialiser.decorations[keys.chest]:
            chest = Chest(self.game, chest_pos)  
            self.decorations.append(chest)
            
    def Spawn_Vase(self):
        for pos in self.decoration_initialiser.decorations[keys.vase]:
            vase = Vase(self.game, pos)  
            self.decorations.append(vase)

    def Spawn_Lightsource(self):
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
        chest = Mimic_Chest(self.game, pos, version)  
        self.decorations.append(chest)
        return chest
    
    
    def Spawn_Effigy_Tomb(self):
        for pos in self.decoration_initialiser.decorations[keys.effigy_tomb]:
            effigy_tomb = Effigy_Tomb(self.game, pos)  
            self.decorations.append(effigy_tomb)

    def Spawn_Portal_Shrine(self):
        for pos in self.decoration_initialiser.decorations[keys.portal_shrine]:
            shrine = Portal_Shrine(self.game, pos)
            self.decorations.append(shrine)

        
    
    def Spawn_Sacrifice_Shrine(self):
        for pos in self.decoration_initialiser.decorations[keys.sacrifice_shrine]:
            shrine = Sacrifice_Shrine(self.game, pos)
            self.decorations.append(shrine)

        
    def Spawn_Soul_Well(self):
        for pos in self.decoration_initialiser.decorations[keys.soul_well]:
            soul_well = Soul_Well(self.game, pos)
            self.decorations.append(soul_well)

    def Spawn_Hunter_Shrine(self):
        for pos in self.decoration_initialiser.decorations[keys.hunter_shrine]:
            shrine = Hunter_Shrine(self.game, pos)
            self.decorations.append(shrine)
    
        
    def Spawn_Teleportation_Circle(self):
        for pos in self.decoration_initialiser.decorations[keys.teleportation_circle]:
            teleportation_circle = Teleportation_Circle(self.game, pos)
            self.decorations.append(teleportation_circle)
            self.teleportation_circles.append(teleportation_circle)
        
        self.Link_Teleportation_Circles()

    
    def Link_Teleportation_Circles(self):
        teleport_circles = self.teleportation_circles.copy()
        random.shuffle(teleport_circles)  # Randomly pair circles

        for i in range(0, len(teleport_circles) - 1, 2):
            a = teleport_circles[i]
            b = teleport_circles[i + 1]
            a.Set_Linked_Portal(b)
            b.Set_Linked_Portal(a)

        for teleport_circle in teleport_circles:
            if not teleport_circle.linked_portal:
                self.Remove_Decoration(teleport_circle)
                teleport_circles.remove(teleport_circle)

    def Spawn_Potion_Table(self, pos, size=None, version=None, radius=None, level=None):
        potion_table = Potion_Table(self.game, pos)  
        self.decorations.append(potion_table)
        return potion_table
    
    def Spawn_Bookshelf(self, pos, size=None, version=None, radius=None, level=None):
        bookshelf = Bookshelf(self.game, pos)  
        self.decorations.append(bookshelf)
        return bookshelf
    
    def Spawn_Weapon_Rack(self, pos, size=None, version=None, radius=None, level=None):
        weapon_rack = Weapon_rack(self.game, pos)  
        self.decorations.append(weapon_rack)
        return weapon_rack
    
    def Spawn_Plinth(self, pos, size=None, version=None, radius=None, level=None):
        plinth = Plinth(self.game, pos)  
        self.decorations.append(plinth)
        return plinth

    def Spawn_Rune_Shrine(self, pos, size=None, version=None, radius=None, level=None):
        shrine = Rune_Shrine(self.game, pos)
        self.decorations.append(shrine)
        return shrine


    def Spawn_Rune_Shrine(self, pos, size=None, version=None, radius=None, level=None):
        shrine = Rune_Shrine(self.game, pos)
        self.decorations.append(shrine)
        return shrine
    

    def Spawn_Bones(self, pos, size=None, version=None, radius=None, level=None):
        bones = Bones(self.game, pos, None)  
        self.bones.append(bones)
        return bones

    def Spawn_Boss_Room(self, pos, size=None, version=None, radius=None, level=None):
        boss_room = Boss_Room(self.game, pos, radius, level)
        self.decorations.append(boss_room)
        return boss_room
    

    def Spawn_Brazer(self, pos, size=None, version=None, radius=None, level=None):
        brazier = Brazier(self.game, pos) 
        self.decorations.append(brazier)
        return brazier


# TODO: Might need a seperate class for handling rooms
    def Spawn_Rooms(self):
        self.Spawn_Library()
        self.Spawn_Loot_Room()
        self.Spawn_Boss_Room()


    def Spawn_Library(self, pos, size):
        libraries = self.game.tilemap.extract([(keys.room, keys.library)])


    def Spawn_Loot_Room(self, pos, size):
        libraries = self.game.tilemap.extract([(keys.room, keys.loot_room)])


    def Spawn_Boss_Room(self, pos, size):
        libraries = self.game.tilemap.extract([(keys.room, keys.boss_room)])





    def Update(self, delta_time):
        self.Check_Keyboard_Input()
        for decoration in self.decorations:
            decoration.Update(delta_time)

    def Check_Keyboard_Input(self):
        if self.game.keyboard_handler.e_pressed:
            if not self.Check_Decorations():
                return
            self.game.keyboard_handler.Set_E_Key(False)

    def Check_Decorations(self):
        nearby_decorations = self.Find_Nearby_Decorations(self.game.player.pos, 2)
        if not nearby_decorations:
            return False
        self.Open_Decoration(nearby_decorations)
        return True

    
    def Find_Nearby_Decorations(self, player_pos, max_distance):
        nearby_decorations = []
        if max_distance <= 5:
            nearby_decorations = self.game.tilemap.Search_Nearby_Tiles(max_distance, player_pos, 'decoration')
        else:
            nearby_decorations = self.Find_Nearby_Decorations_Long_Distance(player_pos, max_distance)
        return nearby_decorations

    def Find_Nearby_Decorations_Long_Distance(self, player_pos, max_distance):
        nearby_decorations = []
        for decoration in self.decorations:
            distance = math.sqrt((player_pos[0] - decoration.pos[0]) ** 2 + (player_pos[1] - decoration.pos[1]) ** 2)
            if distance < max_distance:
                nearby_decorations.append(decoration)
        return nearby_decorations

    def Open_Decoration(self, decorations):      
        for decoration in decorations:
            if decoration.type == keys.bones:
                decorations.remove(decoration)
        if not decorations:
            return False
        player_pos = self.game.player.pos
        decorations.sort(key=lambda decoration: math.sqrt((player_pos[0] - decoration.pos[0]) ** 2 + (player_pos[1] - decoration.pos[1]) ** 2))
        decoration = decorations[0]
        decoration.Open()


    def Sort_Decorations(self, decorations):
        player_pos = self.game.player.pos
        decorations.sort(key=lambda decoration: math.sqrt((player_pos[0] - decoration.pos[0]) ** 2 + (player_pos[1] - decoration.pos[1]) ** 2))
        return decorations


    def Add_Decoration(self, decoration):
        if decoration in self.decorations:
            return
        self.decorations.append(decoration)

    def Remove_Decoration(self, decoration):
        if decoration in self.decorations:
            self.decorations.remove(decoration)
            self.game.item_handler.Remove_Item(decoration)
            self.game.tilemap.Remove_Entity_From_Tile(decoration.tile, decoration.ID)
            decoration.Delete()

    def Remove_Bones(self, bones):
        self.bones.remove(bones)
        return
 
    def Check_Item_Collision(self, item):
        for decoration in self.item_sacrifice:
            if decoration.rect().colliderect(item.rect()):
                return decoration.Spawn_Reward(item)
                 
            
        return False