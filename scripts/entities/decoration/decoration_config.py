from dataclasses import dataclass
from scripts.engine.keys.keys import keys
from typing import Tuple, Optional

@dataclass
class Decoration_Config:
    amount: Tuple[int, int]
    size: Tuple[int, int]
    check_player_path: Optional[bool] = False # Costly pathfinding in loading


