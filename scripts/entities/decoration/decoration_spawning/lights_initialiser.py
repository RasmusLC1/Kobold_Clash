import random

LIGHT_DENSITY = 40          # lower = more torches (1 in LIGHT_DENSITY + 1 chance per tile)
MIN_LIGHT_DISTANCE = 8      # tiles between lights
MIN_LIGHT_DISTANCE_SQ = MIN_LIGHT_DISTANCE ** 2


class Lights_Initialiser():
    def __init__(self, game, floor_tiles_finder):
        self.game = game
        self.floor_tiles_finder = floor_tiles_finder 

    def Initialise_Light_Sources(self, decoration_config):
        light_sources = self._Find_Light_Sources_From_Config(decoration_config)
        if not light_sources:
            print("NO LIGHT SOURCES FOUND")
            return {}
        return self._Spawn_Lightsource(light_sources)

    def _Find_Light_Sources_From_Config(self, decoration_config):
        # light_source is the weight; 0 or unset means the entry isn't a light
        return {decoration_type: values.light_source
                for decoration_type, values in decoration_config.items()
                if values.light_source}

    def _Spawn_Lightsource(self, light_sources):
        light_types = list(light_sources.keys())
        weights = list(light_sources.values())

        decorations_to_spawn = {light_type: [] for light_type in light_types}
        placed_positions = []  # tile coordinates of lights placed so far

        for tile in self.floor_tiles_finder.floor_tiles:
            if tile.contains_decoration:
                continue

            # Random chance to try placing a light on this tile
            if random.randint(0, LIGHT_DENSITY) != 1:
                continue

            if self._Too_Close_To_Existing(tile.pos, placed_positions):
                continue

            light_type = random.choices(light_types, weights=weights)[0]
            decorations_to_spawn[light_type].append(tile)
            placed_positions.append(tile.pos)
            tile.Set_Contains_Decoration(True)

        return decorations_to_spawn

    @staticmethod
    def _Too_Close_To_Existing(pos, placed_positions):
        x, y = pos
        for px, py in placed_positions:
            dx, dy = x - px, y - py
            if dx * dx + dy * dy < MIN_LIGHT_DISTANCE_SQ:  # squared distance, no sqrt needed
                return True
        return False