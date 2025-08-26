from scripts.engine.keys.keys import keys
from scripts.entities.rooms.room_types.loot_room import Loot_Room


class Treasure_Room(Loot_Room):
    def Spawn_Room(game, decorations):
        loot_rooms = game.tilemap.extract([(keys.room, keys.treasure_room)])

        drop_table = {
            keys.weapon_rack : 0.5,
            keys.chest : 0.7,
            keys.vase : 1,
            None : 2
        }

        for decoration in drop_table:
            if decoration not in decorations:
                decorations[decoration] = []

        for loot_room in loot_rooms:
            decorations.update(Treasure_Room.Spawn_Room_Decoration(game.tilemap, decorations, loot_room, drop_table))
        return decorations



