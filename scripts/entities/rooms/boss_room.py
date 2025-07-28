import random
from scripts.engine.keys.keys import keys


class Library():
    def Spawn_Library(self, game):
        libraries = game.tilemap.extract([(keys.room, keys.library)])
        decorations = {}

        for library in libraries:
            decorations.update(self.Spawn_Library_Decoration(game.tilemap, decorations, library))
        return decorations
  