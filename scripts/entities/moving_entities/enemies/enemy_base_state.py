from dataclasses import dataclass
from typing import Tuple, Optional
from scripts.engine.keys.keys import keys

@dataclass
class Enemy_Base_State:
    health: int
    souls: int
    size: Tuple[int, int]
    max_weapon_charge: float
    strength: int
    behavior: str
    ability: Optional[str] = None
    idle_animation: int = 1
    run_animation: 1
    attack_animation: 1
    path_finding_strategy: str = keys.standard