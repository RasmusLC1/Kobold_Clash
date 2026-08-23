from scripts.engine.keys.keys import keys

BAD_REWARDS = {
    keys.poison: 4, keys.fire: 4, keys.frozen: 4, keys.electric: 4,
    keys.slow: 5, keys.snare: 5, keys.weakness: 5,
}

MID_REWARDS = {
    keys.healing: 20, keys.vampiric: 5, keys.regen: 3, keys.thorns: 5,
    keys.speed: 4, keys.arcane_hunger: 5, keys.arcane_conduit: 4, keys.resistance: 4,
}

GOOD_REWARDS = {
    keys.vampiric: 3, keys.regen: 1, keys.thorns: 3, keys.anchor: 3, keys.speed: 2,
    keys.power: 1, keys.arcane_hunger: 3, keys.arcane_conduit: 1, keys.resistance: 1,
    keys.frozen_resistance: 3, keys.fire_resistance: 3, keys.electric_resistance: 3,
    keys.poison_resistance: 3,
}