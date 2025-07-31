from scripts.entities.rooms.library import Library
from scripts.entities.rooms.treasure_room import Treasure_Room
from scripts.entities.rooms.boss_room import Boss_Room


class Room_Initialiser():
    def Spawn_Rooms(game, decorations):
        decorations = {}
        decorations.update(Library.Spawn_Room(game, decorations))
        decorations.update(Treasure_Room.Spawn_Room(game, decorations))
        decorations.update(Boss_Room.Spawn_Boss_Rooms(game))

        return decorations