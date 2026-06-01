from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys

class Bones(Decoration):
    def __init__(self, game, pos, entity_type) -> None:
        super().__init__(game, "bones", pos, (32, 32))
        self.entity_type = str(entity_type)
        self.activated = False

    def Save_Data(self):
        super().Save_Data()
        self.saved_data['entity_type'] = self.entity_type
        self.saved_data['activated'] = self.activated  # Added persistence state tracking

    def Load_Data(self, data):
        super().Load_Data(data)
        self.entity_type = data['entity_type']
        self.activated = data.get('activated', False)  # Added safety default on load

    def Consume(self) -> bool:
        if self.activated:
            return False
        self.activated = True
        self.game.decoration_handler.Remove_Decoration(self)
        return True

    def Revive(self):
        if self.activated:
            return
        
        self.Consume()
        self.game.enemy_handler.Enemy_Spawner(self.pos, self.entity_type)