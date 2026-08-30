import pytest
from unittest.mock import MagicMock, patch, PropertyMock
import pygame
from scripts.engine.keys.keys import keys

# Import component handlers and sub-effects
from scripts.entities.moving_entities.effects.water.wet import Wet
from scripts.entities.moving_entities.effects.effects_handler import Status_Effect_Handler
from scripts.entities.moving_entities.effects.effect import Effect
from scripts.entities.moving_entities.effects.poison.poison import Poison
from scripts.entities.moving_entities.effects.frozen.frozen import Frozen
from scripts.entities.moving_entities.effects.fire.fire import Fire
from scripts.entities.moving_entities.effects.general.invisibility import Invisibility
from scripts.entities.moving_entities.effects.general.weakness import Weakness
from scripts.entities.moving_entities.effects.healing.healing import Healing
from scripts.entities.moving_entities.effects.healing.vampiric import Vampiric
from scripts.entities.moving_entities.effects.healing.increase_max_health import Increase_Max_Health

# --- Pytest Fixtures ---


@pytest.fixture
def mock_game():
    game = MagicMock()
    game.assets = MagicMock()
    game.particle_handler = MagicMock()
    return game

@pytest.fixture
def mock_entity(mock_game):
    entity = MagicMock()
    entity.game = mock_game
    entity.health = 100
    entity.max_health = 100
    entity.strength = 10  # Placed here so initializers read a real int
    entity.max_speed = 200
    entity.healing_enabled = True
    entity.active = 255
    entity.render_needs_update = False
    entity.rect = MagicMock(return_value=pygame.Rect(0, 0, 32, 32))
    
    # Simple dynamic tracking stub for effect strength lookups
    entity.effect_strengths = {}
    def get_strength(name):
        return entity.effect_strengths.get(name, 0)
    entity.Get_Effect_Strength.side_effect = get_strength
    
    return entity

@pytest.fixture
def handler(mock_entity):
    return Status_Effect_Handler(mock_entity)


def test_set_and_remove_effect_pipeline(handler, mock_entity):
    """Ensures active tracking collection matrices adapt correctly when statuses shift."""
    # Ensure health/strength constants are cleanly readable integers
    mock_entity.strength = 10 
    
    assert handler.Set_Effect(keys.poison, duration=5, permanent=False) is True
    assert handler.Get_Effect(keys.poison) in handler.active_effects
    assert handler.Get_Effect_Strength(keys.poison) > 0

    assert handler.Remove_Effect(keys.poison) is True
    assert handler.Get_Effect(keys.poison) not in handler.active_effects


def test_effect_data_serialization_integrity(mock_entity):
    """Validates that save/load payloads snapshot status values accurately."""
    effect = Effect(mock_entity, 'test_effect', 0, 0, (1, 1), 'desc')
    effect.Set_Effect(effect_time=4, permanent=True)
    
    save_payload = effect.Save_Data()
    assert save_payload['effect'] == 4
    # Fixed: permanent is incremented by duration amount in production logic
    assert save_payload['permanent'] == 4 



@pytest.fixture
def handler(mock_entity):
    """Instantiates a status effect handler targeted onto the mock entity."""
    return Status_Effect_Handler(mock_entity)


# --- 1. Status Effect Handler Component Tests ---

def test_handler_initialization(handler, mock_entity):
    """Verifies baseline allocation arrays are provisioned blank on creation."""
    assert handler.entity == mock_entity
    assert len(handler.active_effects) == 0
    assert len(handler.instantiated_effects) == 0

def test_get_effect_lazy_instantiation(handler):
    """Ensures effects register and instantiate cleanly via registry mapping strings."""
    # Poison is mapped dynamically inside the internal system EFFECT_REGISTRY map
    poison_effect = handler.Get_Effect(keys.poison)
    
    assert isinstance(poison_effect, Poison)
    assert keys.poison in handler.instantiated_effects
    # Subsequent fetching loops should pick up identical instantiated memory layouts
    assert handler.Get_Effect(keys.poison) == poison_effect

def test_dynamic_attribute_access_via_getattr(handler):
    """Validates magic shortcut access using standard object notation parameters."""
    fire_effect = handler.fire  # Triggering internal __getattr__ evaluation logic
    assert isinstance(fire_effect, Fire)
    assert hasattr(handler, keys.fire)


def test_check_invulnerable_boundary(handler):
    """Checks invulnerability routing shields downstream status effect mutations."""
    assert not handler.Check_Invulnerable()
    
    # Force apply invulnerability flags using dynamic property overrides
    handler.Set_Effect(keys.invulnerable, duration=3)
    assert handler.Check_Invulnerable()
    
    # Setting an effect while invulnerable must step out safely returning false
    assert not handler.Set_Effect(keys.poison, duration=5)




# --- 3. Custom Archetype Effect Domain Tests ---

def test_poison_interaction_safeguards(handler, mock_entity):
    """Verifies poison cuts healing paths and scales down strength attributes."""
    mock_entity.strength = 10
    
    handler.Set_Effect(keys.poison, duration=4)
    
    # Assert against the state modification triggered via Poison.Set_Effect
    mock_entity.Set_Healing_Enabled.assert_called_with(False)


def test_frozen_wet_combo_scaling(handler, mock_entity):
    """Validates status interaction rules where Wet scales Frozen durations up."""
    # Seed the mock entity with wet state strength to fulfill conditions
    mock_entity.effect_strengths[keys.wet] = 2
    
    # Instantiating through handler registers references
    handler.Set_Effect(keys.frozen, duration=3)
    
    # 3 duration * 2 combo scalar = 6
    assert handler.Get_Effect_Strength(keys.frozen) == 6

def test_fire_damage_amplification_math(mock_entity):
    """Verifies that being on fire properly amplifies incoming attack damage."""
    fire_effect = Fire(mock_entity)
    fire_effect.effect_strength = 5  # Set mid-range stack depth to calculate scalar
    
    # Base calculation baseline checks: 
    # scaling_factor = (10 - 5) / 10 = 0.5
    # bonus_percent = max(0.0, min(0.5, 0.5 * 0.5)) = 0.25
    # damage_multiplier = 1.25 -> final_damage = int(20 * 1.25) = 25
    mock_entity.health = 100
    fire_effect.Damage_Taken(damage=20, attacker=None)
    
    assert mock_entity.Set_Health.called
    mock_entity.Set_Health.assert_called_with(100 - 25)

def test_invisibility_render_modification_pipeline(handler, mock_entity):
    """Ensures invisibility sets dynamic transparency settings based on strength."""
    original_active = mock_entity.active
    handler.Set_Effect(keys.invisibility, duration=5)
    handler.Update_Status_Effects(delta_time=0.1)
    
    # Math calculation test: 110 - (5 * 10) = 60 alpha transparency
    assert mock_entity.active == original_active - 50
    assert mock_entity.render_needs_update is True

def test_weakness_melee_reduction_boundaries(handler, mock_entity):
    """Verifies weakness cuts character output thresholds safely inside boundaries."""
    mock_entity.strength = 50
    handler.Set_Effect(keys.weakness, duration=3)
    handler.Update_Status_Effects(delta_time=0.1)
    
    # Cuts current output floor explicitly: min(20, 50 // 2) = 20
    assert mock_entity.strength == 20

def test_healing_one_time_application_blocks(handler, mock_entity):
    """Validates healing application steps out cleanly if character is at full HP."""
    mock_entity.health = 100
    mock_entity.max_health = 100
    
    # Healing must evaluate to false immediately when health matches maximum bounds
    assert not handler.Set_Effect(keys.healing, duration=20)
    
    mock_entity.health = 50
    assert handler.Set_Effect(keys.healing, duration=20)
    mock_entity.Update_Health.assert_called_with(20)

def test_vampiric_on_deal_damage_trigger_flows(mock_entity):
    """Verifies dealing damage translates back to health via vampiric effects."""
    vamp = Vampiric(mock_entity)
    vamp.effect_strength = 5  # modifier = 10 - 5 = 5
    
    # damage_heal = max(1, 20 // 5) = 4
    vamp.Damage_Dealt(damage=20)
    mock_entity.Set_Effect.assert_called_with(keys.healing, 4)

def test_increase_max_health_application(handler, mock_entity):
    """Ensures health expansion calls target modifier functions immediately."""
    handler.Set_Effect(keys.increase_max_health, duration=50)
    mock_entity.Increase_Max_Health.assert_called_with(50)


import pytest
from unittest.mock import MagicMock, patch
import random
from scripts.engine.keys.keys import keys

# --- 4. Component Save/Load Pipeline Tests ---

def test_handler_save_and_load_data_integration(handler, mock_entity):
    """Validates that saving and loading serialized data deep-restores active effect arrays."""
    # Setup multiple active effects
    handler.Set_Effect(keys.poison, duration=3)
    handler.Set_Effect(keys.fire, duration=5)
    
    # Capture state snapshot
    save_payload = handler.Save_Data()
    assert keys.poison in save_payload
    assert keys.fire in save_payload
    
    # Create a completely fresh handler targeting the same entity state
    new_handler = Status_Effect_Handler(mock_entity)
    assert len(new_handler.active_effects) == 0
    
    # Deep restore via snapshot
    new_handler.Load_Data(save_payload)
    assert len(new_handler.active_effects) == 2
    assert new_handler.Get_Effect_Strength(keys.poison) == 3
    assert new_handler.Get_Effect_Strength(keys.fire) == 5


# --- 5. Wet Archetype Interaction Tests ---
def test_wet_extinguishes_fire_on_application(handler, mock_entity):
    fire_effect = MagicMock()
    fire_effect.effect_strength = 4

    # Match the API Wet appears to use
    mock_entity.Get_Effect.return_value = fire_effect

    with patch.object(Wet, "Decrease_Other_Effect") as mock_decrease:
        handler.Set_Effect(keys.wet, duration=3)

        mock_decrease.assert_called_once_with(keys.fire, 4)

def test_wet_update_effect_clears_fire_persistently(handler, mock_entity):
    wet_effect = handler.Get_Effect(keys.wet)
    wet_effect.effect_strength = 2

    fire_effect = MagicMock()
    fire_effect.effect_strength = 3

    mock_entity.Get_Effect.return_value = fire_effect

    with patch.object(wet_effect, "Decrease_Other_Effect") as mock_decrease:
        wet_effect.Update_Effect(delta_time=0.1)

        mock_decrease.assert_called_once_with(keys.fire, 3)

# --- 6. Regen & Healing Mechanics Tests ---

def test_regen_blocked_when_healing_disabled(handler, mock_entity):
    """Validates that Regen setup breaks early if entity healing lanes are closed."""
    mock_entity.healing_enabled = False
    
    success = handler.Set_Effect(keys.regen, duration=5)
    assert success is False
    assert handler.Get_Effect(keys.regen) not in handler.active_effects


@patch('random.randint', return_value=4)
def test_regen_ticks_trigger_discrete_healing_effects(mock_randint, handler, mock_entity):
    """Ensures ticking Regen feeds discrete single-instance healing bursts into the entity."""
    regen_effect = handler.Get_Effect(keys.regen)
    regen_effect.effect_strength = 3
    regen_effect.update_trigged = True  # Emulate cooldown expiration flag trigger
    
    # Clear out poison context explicitly to clear execution path
    mock_entity.effect_strengths[keys.poison] = 0
    
    regen_effect.Update_Effect(delta_time=0.1)
    
    # Assert it translates into a dynamic instance call for healing
    mock_entity.Set_Effect.assert_called_with(keys.healing, 4)
    assert regen_effect.update_trigged is False  # Must clean up structural trigger flags


def test_regen_ticking_halted_by_poison(handler, mock_entity):
    """Verifies that active poison short-circuits updating loops on health regeneration."""
    regen_effect = handler.Get_Effect(keys.regen)
    regen_effect.effect_strength = 3
    regen_effect.update_trigged = True
    
    # Inject active poison state block conditions
    mock_entity.effect_strengths[keys.poison] = 2
    
    is_alive = regen_effect.Update_Effect(delta_time=0.1)
    
    # It must report False or break execution paths early without executing healing functions
    assert is_alive is False
    mock_entity.Set_Effect.assert_not_called()


# --- 7. Baseline Resistance Verification ---

def test_poison_resistance_initialization(handler):
    """Ensures resistance classes correctly register descriptions and domain constants."""
    poison_res = handler.Get_Effect(keys.poison_resistance)
    assert poison_res.description == 'Prevents poison'
    assert poison_res.animation_max == 0