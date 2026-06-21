from dataclasses import dataclass
from typing import Tuple, Optional
from scripts.engine.keys.keys import keys


@dataclass
class Ability_Attribute:
    symbol : str
    can_attack_while_triggered : Optional[bool] = None
