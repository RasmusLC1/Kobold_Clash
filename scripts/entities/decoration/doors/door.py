from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys


class Door(Decoration):
    def __init__(self, game, type, pos, size) -> None:
        super().__init__(game, type, pos, size)
        self.is_open = False
        self.high_light_cooldown = 0
        self.tile.Set_Physics(True)
        self.tile.Set_Translucent(False)
        # self.game.tilemap.Update_Tile_Type(self.tile, keys.floor)

    def Save_Data(self):
        super().Save_Data()
        self.tile.Set_Physics(True)
        self.game.tilemap.Update_Tile_Type(self.tile, keys.door_basic)
        self.saved_data['is_open'] = self.is_open


    def Load_Data(self, data):
        super().Load_Data(data)
        self.is_open = data['is_open']
        if self.is_open:
            self.Open(False)

    def Update(self):
        if not self.high_light_cooldown:
            return
        self.high_light_cooldown -= 1


    def Set_Highlight(self):
        self.high_light_cooldown = 5


    # TODO: IMPLEMENT walls that can be walked through, I.E walls without physics in tilemap
    def Open(self, generate_clatter = True):
        self.is_open = True
        self.tile.Set_Physics(False)

        self.render = False
        self.game.decoration_handler.Remove_Decoration(self)
        self.Generate_Sound('door_open', 1)
        if generate_clatter:
            self.game.clatter.Generate_Clatter(self.pos, 700) # Generate clatter to alert nearby enemies


    


    def Render(self, surf, offset = (0,0)):
        super().Render(surf, offset)
        # print(self.rendered_image)
        if not self.high_light_cooldown:
            return
        self.Lightup(self.rendered_image)

    def Update_Dark_Surface(self):
        if self.high_light_cooldown:
            return
        return super().Update_Dark_Surface()


    def Update_Light_Level(self):
        nearby_tile = self.game.tilemap.tiles_around(self.pos)
        # Set the light level based on the tile that the entity is placed on
        tile = self.tile

        nearby_tile.remove(tile)
        max_light = max(tile.light_level for tile in nearby_tile)

        tile.Set_Light_Level(max_light)

        return super().Update_Light_Level()
