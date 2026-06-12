class Tile_Entity_Handler:
    __slots__ = ['tile', 'entities', 'update_entity_cooldown']

    def __init__(self, tile):
        self.tile = tile
        self.entities = {}
        self.update_entity_cooldown = 0.0

    def Add_Entity(self, entity):
        if not entity:
            return
        self.entities[entity.ID] = entity
        entity.Set_Active(self.tile.active)
        if self.tile.trap:
            self.tile.trap.Add_Entity(entity)

    def Remove_Entity(self, entity_ID):
        self.entities.pop(entity_ID, None)
        if self.tile.trap:
            self.tile.trap.Remove_Entity(entity_ID)

    def Set_Entity_Active(self, delta_time):
        if self.update_entity_cooldown > 0:
            self.update_entity_cooldown -= delta_time
            return
        
        for entity in self.entities.values():
            entity.Update_Active(self.tile.active)

        self.update_entity_cooldown = 0.1

    def Search_Entities(self, category, ID=0):
        return [e for e in self.entities.values() 
                if e.category == category and e.ID != ID]

    def Search_Type(self, type, ID=0):
        return [e for e in self.entities.values() 
                if e.type == type and e.ID != ID]