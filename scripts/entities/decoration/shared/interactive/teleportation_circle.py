from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys

activation_radius = 200

class Teleportation_Circle(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.teleportation_circle, pos, (32, 32))
        self.description = "Teleport to\nlinked portal\ncosts 10 souls"
        self.linked_portal = None
        self.linked_portal_ID = None


    def Save_Data(self):
        super().Save_Data()
        self.saved_data['linked_portal'] = self.linked_portal_ID
    
    def Load_Data(self, data):
        self.linked_portal_ID = data['linked_portal']
        return super().Load_Data(data)

    def Open(self, generate_clatter=False):
        if not self.linked_portal:
            print("NO LINKED PORTAL:  ", vars(self))
            return
        
        player = self.game.player
        if not player.Decrease_Souls(10):
            return
        player.Set_Position(self.linked_portal.pos.copy())
        self.linked_portal.Generate_Sound(keys.teleportation, 0.2, 500)

        self.game.particle_handler.Activate_Particles(random.randint(8, 12), keys.soul_particle, self.linked_portal.rect().center)
        
    
    def Set_Linked_Portal(self, linked_portal):
        if not linked_portal:
            print("FAILED TO LINK PORTALS")
            return
        self.linked_portal = linked_portal
        self.linked_portal_ID = linked_portal.ID