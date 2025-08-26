from scripts.entities.traps.trap_spawners.trap_spawner import Trap_Spawner
from scripts.entities.traps.traps.ancient_tomb.bell_pressure_plate import Bell_Pressure_plate
from scripts.entities.traps.traps.ancient_tomb.tomb_pressure_plate import Tomb_Pressure_Plate
from scripts.entities.traps.traps.ancient_tomb.soul_trap import Soul_Trap
from scripts.engine.keys.keys import keys


class Ancient_Crypt_Trap_Spawner(Trap_Spawner):
    EXTRA_TRAPS = {
        keys.tomb_pressure_plate : 0.2,
        keys.bell_pressure_plate : 0.3,
        keys.soul_trap : 0.1,

    }
    EXTRA_TRAP_CLASSES = {
        keys.tomb_pressure_plate: Tomb_Pressure_Plate,
        keys.bell_pressure_plate: Bell_Pressure_plate,
        keys.soul_trap: Soul_Trap,

    }

    def __init__(self, game):
        super().__init__(game, self.EXTRA_TRAPS, self.EXTRA_TRAP_CLASSES)
