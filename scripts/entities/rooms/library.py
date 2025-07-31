from scripts.engine.keys.keys import keys
from scripts.entities.rooms.loot_room import Loot_Room

class Library(Loot_Room):
    def Spawn_Room(game, decorations):
        libraries = game.tilemap.extract([(keys.room, keys.library)])

        drop_table = {
            keys.plinth : 0.2,
            keys.bookshelf : 1,
            None : 3
        }

        for decoration in drop_table:
            if decoration not in decorations:
                decorations[decoration] = []


        for library in libraries:
            decorations.update(Library.Spawn_Room_Decoration(game.tilemap, decorations, library, drop_table))
        return decorations
    