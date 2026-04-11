from scripts.engine.lights.lights import Light

class Light_Handler():
    def __init__(self, game) -> None:
        self.game = game
        self.lights = []

    def Add_Light(self, pos, light_level, tile):
        light = Light(self.game, pos, light_level, tile)
        self.lights.append(light)
        return light

    def Move_Light(self, pos, light_source, tile):
        light_source.Move_Light(pos, tile)

    def Remove_Light(self, light_source):
        if light_source in self.lights:
            self.lights.remove(light_source)
        light_source.Delete_Light()

    def Initialise_Light_Level(self, tile):
        if not tile: return 50
        # simplified math for the same result
        level = max(50, min(255, tile.light_level * 25))
        return level