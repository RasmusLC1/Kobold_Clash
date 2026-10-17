import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.decoration_initialiser.decoration_initialiser import Decoration_Initialiser
from scripts.entities.rooms.crypt_room_initialiser import Crypt_Room_Initialiser


class Crypt_Decoration_Initialiser(Decoration_Initialiser):
    room_type = Crypt_Room_Initialiser

    def Spawn_Large_Objects(self):
        super().Spawn_Large_Objects()
        self.Spawn_Sacrifice_Shrine()
        self.Spawn_Effigy_Tomb()
        self.Spawn_Blood_Shrine()

    def Spawn_Small_Objects(self):
        super().Spawn_Small_Objects()

