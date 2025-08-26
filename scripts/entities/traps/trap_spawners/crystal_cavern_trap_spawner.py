from scripts.entities.traps.trap_spawners.trap_spawner import Trap_Spawner

from scripts.engine.keys.keys import keys


class Crystal_Cavern_Trap_Spawner(Trap_Spawner):
    EXTRA_TRAPS = {

    }
    EXTRA_TRAP_CLASSES = {
    }

    def __init__(self, game):
        super().__init__(game, self.EXTRA_TRAPS, self.EXTRA_TRAP_CLASSES)
