import random
from scripts.engine.keys.keys import keys


class Boss_Room():
    def Spawn_Boss_Room(self, game):
        boss_rooms = game.tilemap.extract([(keys.room, keys.library)])
        decorations = {}

        if keys.boss_room not in decorations:
            decorations[keys.boss_room] = []

        for boss_room in boss_rooms:
            decorations.update(self.Spawn_Boss_Room(decorations, boss_room))
        return decorations
    
    # More traps, rewards etc can be spawned later
    def Spawn_Boss_Room(self, decorations, boss_room):
        pos = boss_room[keys.pos]

        decorations[keys.boss_room].append(pos)

  