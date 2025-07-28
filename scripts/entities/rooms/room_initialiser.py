from scripts.entities.rooms.library import Library
from scripts.entities.rooms.loot_room import Loot_Room
from scripts.entities.rooms.boss_room import Boss_Room


class Room_Initialiser():
    def Spawn_Rooms(self, game):
        decorations = {}
        decorations.update(Library.Spawn_Library(game))
        decorations.update(Loot_Room.Spawn_Loot_Room(game))
        decorations.update(Boss_Room.Spawn_Boss_Room(game))