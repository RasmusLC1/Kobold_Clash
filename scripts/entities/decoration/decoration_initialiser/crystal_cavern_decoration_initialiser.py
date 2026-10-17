import random
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.decoration_initialiser.decoration_initialiser import Decoration_Initialiser
from scripts.entities.rooms.ancient_tomb_room_initialiser import Ancient_Tomb_Room_Initialiser


class Crystal_Cavern_Decoration_Initialiser(Decoration_Initialiser):
    room_type = Ancient_Tomb_Room_Initialiser
