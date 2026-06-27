from dataclasses import dataclass
from typing import Tuple, Optional
from scripts.engine.keys.keys import keys

@dataclass
class Enemy_Base_State:
    # Core Stats
    health: int
    souls: int
    size: Tuple[int, int]
    strength: int
    
    # Movement & RPG Stats
    speed: int
    agility: int
    intelligence: int
    stamina: int
    
    # AI & Category
    behavior: str
    sub_category: str
    ability: Optional[str] = None
    path_finding_strategy: str = keys.standard
    
    # Animation Frames
    idle_animation: int = 1
    run_animation: int = 1
    attack_animation: int = 1