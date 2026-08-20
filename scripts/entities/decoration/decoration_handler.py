from scripts.entities.decoration.decoration_spawner import Decoration_Spawner
import random
import pygame
from scripts.engine.keys.keys import keys

class Decoration_Handler():
    def __init__(self, game) -> None:
        self.game = game
        self.decoration_initialiser = None
        self.decorations = []
        self.bones = []
        self.nearby_decoration_cooldown = 0
        self.saved_data = {}
        self.decoration_spawner = Decoration_Spawner(game)
        self.initalised = False

        self.spawn_methods = None

        self.item_sacrifice = []


    def Clear_Decorations(self):
        self.decorations.clear()
        self.saved_data.clear()

    def Initialise(self):
        self.decorations, self.item_sacrifice, self.spawn_methods = self.decoration_spawner.Initialise()
        self.initalised = True


    def Get_Random_Decoration_Of_Type(self, type):
        decorations_with_type = []
        for decoration in self.decorations:
            if decoration.type in type:
                decorations_with_type.append(decoration)

        if not decorations_with_type:
            return None

        return random.choice(decorations_with_type)
    

    def Save_Decoration_Data(self):
        for decoration in self.decorations:
            decoration.Save_Data()
            self.saved_data[decoration.ID] = decoration.saved_data

    def Load_Data(self, data):
        # Check if the decoration spawner is initialised
        if not self.initalised:
            self.Initialise()

        self.decoration_spawner.Get_Dungeon_Type()
        for ID, item_data in data.items():
            if not item_data:
                continue
            try:
                type = item_data[keys.type]
                pos = item_data[keys.pos]
                self.Decoration_Spawner(type, pos, data=item_data)
            except Exception as e:
                print("DATA WRONG DECORATION HANDLER", item_data, e)

        self.Load_Portal_Links()

    def Load_Portal_Links(self):
        for decoration in self.decorations:
            if decoration.type == keys.teleportation_circle:
                linked_portal = self.Get_Decoration_By_ID(decoration.linked_portal_ID)
                decoration.Set_Linked_Portal(linked_portal)
        

    def Decoration_Spawner(self, type, pos, data=None):
        spawn_function = self.spawn_methods.get(type)
        if not spawn_function:
            print(f"Warning: Decoration type '{type}' not recognized. Decoration_Handler Decoration_Spawner")
            return None
        decoration = spawn_function(self.game, pos)
        if not decoration:
            return None
        
        if data:
            decoration.Load_Data(data)
        self.decorations.append(decoration)
        return decoration



    def Update(self, delta_time):
        self.Check_Keyboard_Input()
        for decoration in self.decorations:
            decoration.Update(delta_time)

    def Check_Keyboard_Input(self):
        if self.game.keyboard_handler.is_key_pressed(pygame.K_e):
            if not self.Check_Decorations():
                return
            self.game.keyboard_handler.Set_E_Key(False)

    def Check_Decorations(self):
        nearby_decorations = self.Find_Nearby_Decorations()
        if not nearby_decorations:
            return False
        self.Open_Decoration(nearby_decorations)
        return True

    
    def Find_Nearby_Decorations(self):
        player_tile = self.game.player.tile
        nearby_decorations = []
        nearby_decorations = player_tile.Search_Entities(keys.decoration)
        for tile in player_tile.neighbor_tiles:
            nearby_decorations.extend(tile.Search_Entities(keys.decoration))
        return nearby_decorations


    def Open_Decoration(self, decorations):
        open_decorations = []      
        for decoration in decorations:
            if decoration.type == keys.bones:
                continue
            open_decorations.append(decoration)
        if not open_decorations:
            return False
        player_pos = self.game.player.pos
        open_decorations.sort(key=lambda decoration: self.Calculate_Distance(decoration))
        decoration = open_decorations[0]
        decoration.Open()

    # Look for fragile walls and doors and pick a random one
    def Get_Random_Door(self):
        doors = []

        for decoration in self.decorations:
            if not "door" in decoration.type and not keys.fragile_wall in decoration.type:
                continue

            doors.append(decoration)

        if not doors:
            return None

        door = random.choice(doors)
        return door
    

    def Sort_Decorations(self, decorations):
        player_pos = self.game.player.pos
        decorations.sort(key=lambda decoration: self.Calculate_Distance(decoration))
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

    def Remove_Bones(self, bone):
        if not bone in self.bones:
            return 

        self.bones.remove(bone)
        return
    
    def Get_Decoration_By_ID(self, ID):
        for decoration in self.decorations:
            if decoration.ID == ID:
                return decoration
            
        return None
 
    def Check_Item_Collision(self, item):
        for decoration in self.item_sacrifice:
            if decoration.rect().colliderect(item.rect()):
                return decoration.Spawn_Reward(item)
                 
            
        return False
    
    def Spawn_Mimic_Chest(self, pos, size=None, version=None, radius=None, level=None):
        chest = self.decoration_spawner.Spawn_Mimic_Chest(pos, version=version)
        self.decorations.append(chest)
        return chest
   
    

    def Calculate_Distance(self, decoration):
        player_pos = self.game.player.pos
        dx = player_pos[0] - decoration.pos[0]
        dy = player_pos[1] - decoration.pos[1]
        return dx * dx + dy * dy