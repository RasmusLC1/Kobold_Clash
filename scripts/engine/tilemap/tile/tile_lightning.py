class Tile_Lighting:
    __slots__ = ['tile', 'light_level', 'max_light', 'light_contributions', 'light_ID']

    def __init__(self, tile, light_level=0):
        self.tile = tile
        self.light_level = light_level
        self.max_light = 0
        self.light_ID = None
        self.light_contributions = {}

    def Add_Contribution(self, light_id, contribution):
        self.light_contributions[light_id] = contribution
        if contribution > self.max_light:
            self.max_light = contribution
        self.light_level = max(self.light_level, contribution)
        self.tile.needs_redraw = True

    def Remove_Contribution(self, light_id):
        if light_id not in self.light_contributions:
            return
        was_max = self.light_contributions[light_id] == self.max_light
        del self.light_contributions[light_id]
        if was_max:
            self.max_light = max(self.light_contributions.values(), default=0)
        self.light_level = self.max_light
        self.tile.needs_redraw = True