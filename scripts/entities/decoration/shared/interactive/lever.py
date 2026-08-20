from scripts.entities.decoration.decoration import Decoration
from scripts.engine.keys.keys import keys
from scripts.entities.decoration.shared.shared_registry import register_ability

@register_ability(keys.lever)
class Lever(Decoration):
    def __init__(self, game, pos) -> None:
        super().__init__(game, keys.lever, pos, (32, 32))
        self.description = "Opens something"
        self.max_animation = 1

    def Open(self, generate_clatter=False):
        if not self.empty:
            door = self.game.decoration_handler.Get_Random_Door()
            self.Set_Animation(1)
            self.empty = True
            print("OPEN LEVER", door)
            if not door:
                return
            
            door.is_open = True
            door.Open(False)
            return True
            
        return False
  