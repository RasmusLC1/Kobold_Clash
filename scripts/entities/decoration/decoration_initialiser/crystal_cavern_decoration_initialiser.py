import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.decoration_initialiser.decoration_initialiser import Decoration_Initialiser
from scripts.entities.rooms.crypt_room_initialiser import Crypt_Room_Initialiser


class Crystal_Cavern_Decoration_Initialiser(Decoration_Initialiser):
    room_type = Crypt_Room_Initialiser

    def Spawn_Large_Objects(self):
        super().Spawn_Large_Objects()
        self.Spawn_Harmonic_Crystal()
        self.Spawn_Amplifying_Node()
        self.Spawn_Crystalisation_Shrine()

    def Spawn_Small_Objects(self):
        self.Spawn_Crystal_Plinth()
        super().Spawn_Small_Objects()


    def Spawn_Amplifying_Node(self):
        amount = random.randint(2, 4)
        self.Find_Floor_Tiles_Large_Object(keys.amplifying_node, amount)

    def Spawn_Harmonic_Crystal(self):
        amount = random.randint(30, 50)
        self.Find_Floor_Tiles_Large_Object(keys.harmonic_crystal, amount)

    def Spawn_Crystalisation_Shrine(self):
        amount = random.randint(2, 3)
        self.Find_Floor_Tiles_Large_Object(keys.crystalisation_shrine, amount)


    def Spawn_Crystal_Plinth(self):
        amount = random.randint(7, 12)
        self.Find_Floor_Tiles(keys.crystal_plinth, amount)