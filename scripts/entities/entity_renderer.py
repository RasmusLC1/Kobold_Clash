import math
from scripts.engine.keys.keys import keys

class Entity_Renderer():
    def __init__(self, game):
        self.game = game
        self.entities = []

    def Clear_Entities(self):
        self.entities.clear()

    def Update(self):
        self.Find_Nearby_Entities()
        self.entities.sort(key=lambda entity: (entity.category != 'trap', entity.pos[1]))

    def Find_Nearby_Entities(self):
        self.entities.clear()
        for tile in self.game.ray_caster.tiles:
            self.entities.extend(tile.entities.values())

    def Add_Entity(self, entity):
        if entity in self.entities:
            return
        if not entity.render:
            return
        self.entities.append(entity)

    
    def Remove_Entity(self, entity):
        if not entity in self.entities:
            return
        
        tile = self.game.tilemap.Current_Tile(entity.tile)
        if tile:
            tile.Clear_Entity(entity.ID)
        self.entities.remove(entity)


    def Render(self, surf, offset = (0,0)):
        nearest_interactable_object_found = False
        for entity in self.entities:
            if not entity.render:
                continue

            if entity.category == keys.item:
                entity.Update_Animation()
            entity.Render(surf, offset)

            if nearest_interactable_object_found:
                continue

            nearest_interactable_object_found = self.Render_Tool_Tip(surf, offset, nearest_interactable_object_found, entity)

    
    def Render_Tool_Tip(self, surf, offset, nearest_interactable_object_found, entity):
        if entity.category == keys.item and not entity.picked_up or entity.category == keys.decoration:
            if entity.category == keys.decoration:
                if entity.empty:
                    return False
            distance = math.sqrt((entity.pos[0] - self.game.player.pos[0]) ** 2 + (entity.pos[1] - self.game.player.pos[1]) ** 2)
            if distance < 40:
                self.game.interactable_object.Render(surf, offset, entity)
                return True
        
        return False
