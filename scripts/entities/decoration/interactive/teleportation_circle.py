from scripts.entities.decoration.decoration import Decoration
import random
from scripts.engine.keys.keys import keys

activation_radius = 200

class Teleportation_Circle(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.teleportation_circle, pos, (32, 32))
        self.description = "Teleport to\nlinked portal\ncosts 10 souls"
        self.linked_portal = None



    def Update(self):
        return super().Update()


    def Open(self, generate_clatter=False):
        if not self.linked_portal:
            print("NO LINKED PORTAL:  ", vars(self))
            return
        
        player = self.game.player
        self.game.player.Set_Position(self.linked_portal.pos.copy())
        self.game.sound_handler.Play_Sound('teleportation', 0.2)
        self.game.clatter.Generate_Clatter(self.linked_portal.pos, 500) # Generate clatter to alert nearby enemies

        player.Decrease_Souls(10)
        self.game.particle_handler.Activate_Particles(random.randint(8, 12), keys.soul_particle, self.linked_portal.rect().center, frame=random.randint(50, 70))
        

        

        
    
    def Set_Linked_Portal(self, linked_portal):
        self.linked_portal = linked_portal