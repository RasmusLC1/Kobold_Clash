from scripts.entities.rooms.library import Library
from scripts.entities.rooms.loot_room import Loot_Room
from scripts.entities.rooms.boss_room import Boss_Room


class Room_Initialiser():
    def Spawn_Rooms(game, decorations):
        decorations = {}
        decorations.update(Library.Spawn_Library(game, decorations))
        decorations.update(Loot_Room.Spawn_Loot_Room(game, decorations))
        decorations.update(Boss_Room.Spawn_Boss_Rooms(game))

        return decorations