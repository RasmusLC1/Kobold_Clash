from scripts.engine.keys.keys import keys
from .symbol import Symbol

class SymbolRegistry:
    def __init__(self, game):
        self.game = game
        self._symbols = {}
        self._load_registry()

    def _load_registry(self):
        # Your ordered keys list
        ordered_keys = [
            keys.healing, keys.increase_strength, keys.speed,
            keys.souls, keys.invisibility,
            keys.slash, keys.blunt, keys.electric,
            keys.resistance, keys.regen, keys.silence,
            keys.jump, keys.vampiric, keys.fire,
            keys.frozen, keys.poison, keys.wet,
            keys.block, keys.fire_resistance,
            keys.frozen_resistance, keys.poison_resistance,
            keys.power, keys.gold, keys.range, keys.key,
            keys.arcane_conduit, keys.magnet, keys.arcane_hunger, 
            keys.invulnerable, keys.snare, keys.thorns,
            keys.electric_resistance,
            keys.chain, keys.enemy, keys.curse,
            keys.weakness, keys.vulnerable, keys.luck,
            keys.anchor, keys.blood_tomb, keys.halo,
            keys.demonic_bargain, keys.temptress_embrace,
            keys.slow, keys.soul_drained, keys.health, keys.blood_ring,
            keys.forsaken_grimoire, keys.black_coin, keys.charge,
            keys.run_away  
        ]
        
        spritesheet = self.game.assets[keys.symbols]
        
        for index, key in enumerate(ordered_keys):
            if index < len(spritesheet):
                # Just store the raw key and the pre-sliced image surface
                self._symbols[key.lower()] = Symbol(key, spritesheet[index])

    # Finds a symbol by its string key and renders it if it exists
    def Render_Symbol_By_Key(self, surf, key, pos, scale=1.0):
        symbol = self.get(key)
        if not symbol:
            print(f"Warning: No symbol icon registered for key: '{key}'")
            return
        symbol.render(surf, pos, scale)

    # Get the symbol
    def get(self, key: str) -> Symbol:
        return self._symbols.get(key.lower())

    # Check if a symbol exists
    def exists(self, key: str) -> bool:
        return key.lower() in self._symbols