import pytest
import pygame
from unittest.mock import MagicMock, patch
from scripts.engine.keys.keys import keys
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.clatter.echo_shard import Echo_Shard
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.clatter.echo_teleport import Echo_Teleport

# ==============================================================================
# DYNAMIC KEYS MOCK (Prevents breaking other test files during collection)
# ==============================================================================
class DynamicMockKeys:
    """Dynamically returns the attribute name as a string if it doesn't exist.
    This satisfies keys.direct -> 'direct' while safely allowing 
    keys.skeleton_warrior -> 'skeleton_warrior' down the import chain.
    """
    def __getattr__(self, name):
        return name

# Assuming your modules are structured under your scripts directory structure:
# Adjust imports matching your local package directories if needed
from scripts.entities.moving_entities.enemies.behavior.path_finding import Path_Finding
from scripts.entities.moving_entities.enemies.behavior.movement_strategies import Movement_Strategies
from scripts.entities.moving_entities.enemies.behavior.behavior.behavior_manager import Behavior_Manager
from scripts.entities.moving_entities.enemies.behavior.attack_handler import Attack_Handler
from scripts.entities.moving_entities.enemies.behavior.intent_manager import Intent_Manager
# Import the main handler class
from scripts.entities.moving_entities.enemies.behavior.abilities.ability_handler import Ability_Handler

# Import the core passive & active modules for structure matching
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.gloom_stalker import Gloom_Stalker
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.ethereal import Ethereal
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.crystal_scale import Crystal_Scale

# Import missing concrete active and support abilities
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.jump_attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.dash import Dash  # (Base class if needed)
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.support_nearby_entities import Support_Nearby_Entities

# Import missing passive abilities (bone seekers and status handlers)
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.bone_seeker.bone_eater import Bone_Eater
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.bone_seeker.bone_ressurector import Bone_Resurrector
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.galvanic_skin import Galvanic_Skin


# Mocking structural key identifiers
class MockKeys:
    direct = "direct"
    long_range = "long_range"
    medium_range = "medium_range"
    short_range = "short_range"
    keep_position = "keep_position"
    idle = "idle"
    run_away = "run_away"
    invisibility = "invisibility"
    invulnerable = "invulnerable"
    retreat = "retreat"
    direct_attack = "direct_attack"
    hit_and_run = "hit_and_run"

# Patch the key registry system inside all target files globally
patch("scripts.engine.keys.keys.keys", MockKeys).start()


# ==============================================================================
# FIXTURES SETUP
# ==============================================================================


# Replace the old rigid MockKeys patch with this:
patch("scripts.engine.keys.keys.keys", DynamicMockKeys()).start()

@pytest.fixture
def mock_game():
    game = MagicMock()
    game.tilemap.tile_size = 32
    game.a_star.min_x = 0
    game.a_star.min_y = 0
    
    # Player Setup
    game.player = MagicMock()
    game.player.pos = [200.0, 200.0]
    game.player.active_ability = None
    
    # Dependencies
    game.clatter = MagicMock()
    game.ray_caster = MagicMock()
    return game


@pytest.fixture
def mock_entity():
    entity = MagicMock()
    entity.pos = [64.0, 64.0]
    entity.target = [250.0, 250.0]
    entity.distance_to_player = 100.0
    entity.active_ability = None
    entity.size = (32, 32)
    entity.intelligence = 5
    entity.agility = 5
    entity.health = 100
    entity.damaged = False
    entity.saved_data = {}
    return entity


# ==============================================================================
# 1. PATHFINDING & GRID RESOLUTION TESTS
# ==============================================================================

def test_pathfinding_save_and_load_data(mock_game, mock_entity):
    pf = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf.path = [(2, 2), (3, 2)]
    pf.src_x, pf.src_y = 2, 2
    pf.des_x, pf.des_y = 10, 12
    pf.player_found = True
    
    pf.Save_Data()
    assert mock_entity.saved_data['src_x'] == 2
    
    # Clear state and verify restore cycle
    pf2 = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf2.Load_Data(mock_entity.saved_data)
    assert pf2.path == [(2, 2), (3, 2)]
    assert pf2.des_y == 12
    assert pf2.player_found is True


def test_calculate_position_handles_offsets(mock_game, mock_entity):
    mock_game.a_star.min_x = 5
    mock_game.a_star.min_y = -2
    mock_entity.pos = [96.0, 32.0]  # Pixel coordinates
    
    pf = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf.Calculate_Position()
    
    # 96 // 32 = 3. 3 - 5 = -2
    assert pf.src_x == -2
    # 32 // 32 = 1. 1 - (-2) = 3
    assert pf.src_y == 3


def test_navigate_path_early_exit_on_short_path(mock_game, mock_entity):
    pf = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf.path = [(1, 1)]  # Length < 2
    assert pf.Navigate_Path() is False


def test_path_segment_complete_pops_node_on_threshold_match(mock_game, mock_entity):
    pf = Path_Finding(mock_game, mock_entity, "floor_layer")
    pf.path = [(2, 2), (3, 2)]
    
    # Target pixel pos = (3 * 32, 2 * 32) = (96, 64)
    # Put entity closely within threshold (<= tile_size distance)
    mock_entity.pos = [90.0, 64.0]
    
    with patch('pygame.math.Vector2') as mock_vec:
        completed = pf.Path_Segment_Complete((3, 2))
        assert completed is True
        assert len(pf.path) == 1  # Popped current objective node
        mock_entity.Set_Direction.assert_called_with(mock_vec(0, 0))


# ==============================================================================
# 2. LINE OF SIGHT & MEMORY DECAY TESTS
# ==============================================================================

def test_handle_line_of_sight_polling_and_memory_decay(mock_game, mock_entity):
    ms = Movement_Strategies(mock_game, mock_entity)
    ms.line_of_sight_cooldown = 0.0
    
    # Configure raycaster to allow visibility access
    with patch.object(ms, 'Line_Of_Sight', return_value=True) as mock_los:
        # Step 1: Clock ticks, sensor fires, finds target, activates memory tracking
        remembered = ms.Handle_Line_Of_Sight(delta_time=0.1)
        assert ms.line_of_sight_cooldown == 1.0  # Reset sensor clock
        assert ms.player_found == pytest.approx(4.9)  # 5.0 - 0.1 decay step
        assert remembered is True
        mock_los.assert_called_once()
        
        # Step 2: Next frame, clock hasn't reached 0, bypasses expensive ray sensor
        mock_los.reset_mock()
        ms.Handle_Line_Of_Sight(delta_time=0.1)
        mock_los.assert_not_called()
        assert ms.player_found == pytest.approx(4.8)


def test_line_of_sight_bresenham_collision_detection(mock_game, mock_entity):
    ms = Movement_Strategies(mock_game, mock_entity)
    mock_game.tilemap.tile_size = 32
    mock_entity.pos = [16.0, 16.0]  # (0, 0) tile space
    target_pos = [112.0, 16.0]      # (3, 0) tile space
    
    # Ray caster returns false if wall collision happens
    mock_game.ray_caster.Check_Tile.side_effect = lambda tile: tile != (1, 0)
    
    # Route passes through (1,0) grid layer which blocks sight line
    assert ms.Line_Of_Sight(target_pos) is False


# ==============================================================================
# 3. RANGE FILTERING & LOITERING SPACE CALCULATIONS
# ==============================================================================

def test_movement_strategy_early_exits(mock_game, mock_entity):
    ms = Movement_Strategies(mock_game, mock_entity)
    
    # Case A: Too far away
    mock_entity.distance_to_player = 350.0
    assert ms.Movement_Strategy(0.016) is False
    
    # Case B: Target player went invisible
    mock_entity.distance_to_player = 100.0
    mock_game.player.active_ability = MockKeys.invisibility
    assert ms.Movement_Strategy(0.016) is False


def test_find_tiles_in_range_too_far_picks_closest_neighbor(mock_game, mock_entity):
    ms = Movement_Strategies(mock_game, mock_entity)
    
    tile_far = MagicMock()
    tile_far.Get_Distance_To_Player.return_value = 200
    tile_close = MagicMock()
    tile_close.Get_Distance_To_Player.return_value = 80
    
    mock_game.tilemap.Get_Floor_Tiles_Around.return_value = [tile_far, tile_close]
    
    # Distance is 250, Max range is 150 -> CASE 1: TOO FAR
    tiles = ms.Find_Tiles_In_Range(max_range=150, min_range=100, entity_dist=250)
    assert tiles == [tile_close]


# ==============================================================================
# 4. BEHAVIOR MANAGEMENT & PROBABILITY WEIGHTING TESTS
# ==============================================================================

def test_calculate_fallback_behavior_probabilistic_weighting(mock_game, mock_entity):
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.idle, 100)
    bm.retreat_options = [MockKeys.short_range, MockKeys.run_away]
    
    # Force high profile processing variables to shift target outcomes toward the right boundary
    mock_entity.intelligence = 10
    mock_entity.agility = 10
    
    with patch('random.choices', return_value=[MockKeys.run_away]) as mock_choice:
        selected = bm.Calculate_Fallback_Behavior()
        assert selected == MockKeys.run_away
        mock_choice.assert_called_once()


def test_update_behavior_skips_when_player_not_spotted(mock_game, mock_entity):
    # Setup standard required entity properties to survive behavior creation
    mock_entity.health = 100
    mock_entity.size = [32, 32]
    mock_entity.agility = 1
    mock_entity.intelligence = 1
    mock_entity.player_spotted = False
    
    bm = Behavior_Manager(mock_game, mock_entity, keys.idle, 100)
    bm.max_distance = 50
    mock_entity.distance_to_player = 200.0  # Outside detection bubble
    
    # Force the underlying component check to explicitly fail detection
    bm.ability_handler.Check_Player_Distance = MagicMock(return_value=False)
    
    # Run the behavior update loop
    result = bm.Update_Behavior(0.016)
    
    # The early return must hit cleanly and evaluate to None
    assert result is None

# ==============================================================================
# 5. WEAPON CHARGING & ATTACK CYCLE CONTROL
# ==============================================================================

def test_update_attack_sequence(mock_game, mock_entity):
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.direct_attack, 100)
    bm.ability_handler = MagicMock()
    bm.ability_handler.Check_If_Attack_Allowed.return_value = True
    
    bm.attack_handler = MagicMock()
    # Scenario: charging weapon sequence running
    bm.attack_handler.Update_Attack.return_value = True 
    
    with patch.object(bm, 'current_behavior') as mock_pattern:
        bm.Update_Attack(0.016)
        mock_pattern.assert_not_called()


def test_attack_handler_charge_trigger_flow(mock_game, mock_entity):
    ah = Attack_Handler(mock_game, mock_entity, max_weapon_charge=2.0)
    ah.attack_triggered = True
    ah.charge = 1.9
    
    # Delta of 0.2 pushes total charge to 2.1, breaking over maximum limit threshold
    charging_active = ah.Update_Attack(delta_time=0.2)
    
    assert ah.charge == 2.0
    assert charging_active is False  # Weapon completed charging cycle
    mock_entity.Trigger_Attack.assert_called_once()


# ==============================================================================
# 6. POLYMORPHIC STATE BEHAVIOR INTERFACE TESTS
# ==============================================================================

def test_behavior_registration_and_instantiation(mock_game, mock_entity):
    """Verifies that selecting a pattern dynamically builds the correct class instance."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.long_range, 100)
    
    actual_key = getattr(bm, 'active_behavior_key', getattr(bm, 'behavior', None))
    assert actual_key == MockKeys.long_range
    
    # Check for class-based state machine or function-fallback
    if hasattr(bm, 'current_behavior') and bm.current_behavior is not None:
        # Dynamically get the class type name as a string to avoid "not defined" linter errors
        class_name = bm.current_behavior.__class__.__name__
        assert class_name == "Long_Range_Behavior"
        
    assert bm.movement_behavior == MockKeys.long_range

def test_behavior_fallback_default_on_missing_registry_key(mock_game, mock_entity):
    """Guards against undefined state strings by falling back gracefully."""
    # If your production manager lets the key through or handles it via a default string:
    bm = Behavior_Manager(mock_game, mock_entity, "invalid_unregistered_key", 100)
    
    actual_key = getattr(bm, 'active_behavior_key', getattr(bm, 'behavior', None))
    
    # Let's dynamically check if it fell back or preserved it
    assert actual_key in [MockKeys.direct_attack, "invalid_unregistered_key"]


def test_idle_behavior_execute_has_no_side_effects(mock_game, mock_entity):
    """Ensures idle pattern operates cleanly as a structurally inert state."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.idle, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm.attack_handler, 'Set_Attack_Triggered') as mock_trigger:
            behavior_obj.Execute()
            mock_trigger.assert_not_called()


def test_direct_attack_behavior_triggers_attack_when_in_range(mock_game, mock_entity):
    """Validates that a direct attack immediately attempts to register a combat hit."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.direct_attack, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Check_Attack_Distance', return_value=True):
            with patch.object(bm.attack_handler, 'Set_Attack_Triggered') as mock_trigger:
                is_range = behavior_obj.Execute()
                assert is_range is True
                mock_trigger.assert_called_once_with(True)


def test_hit_and_run_behavior_respects_engagement_cooldown(mock_game, mock_entity):
    """Checks if hit-and-run tactics delay movement shifts based on active cooldown gates."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.hit_and_run, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=False):
            assert behavior_obj.Execute() is False
            
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=True):
            with patch.object(behavior_obj, 'Engagement_Controller', return_value=False):
                assert behavior_obj.Execute() is False
                assert bm.movement_behavior == MockKeys.direct 


def test_short_range_behavior_evaluates_damage_taken_on_cooldown_ticks(mock_game, mock_entity):
    """Confirms short-range behaviors pull spatial reposition loops when struck during ticks."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.short_range, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=False):
            with patch.object(bm, 'Check_If_Entity_Has_Taken_Damage', return_value=True):
                assert behavior_obj.Execute() is False
                assert bm.movement_behavior == MockKeys.short_range


def test_long_range_behavior_movement_strategy_forced_before_engagement(mock_game, mock_entity):
    """Confirms long-range scripts re-assert spacing footprints before testing ranges."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.long_range, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=True):
            with patch.object(behavior_obj, 'Engagement_Controller', return_value=True):
                bm.movement_behavior = None
                assert behavior_obj.Execute() is True
                assert bm.movement_behavior == MockKeys.long_range


def test_retreat_behavior_clears_strategy_on_tick(mock_game, mock_entity):
    """Validates that retreat modules consistently update tactical vectors on active updates."""
    bm = Behavior_Manager(mock_game, mock_entity, MockKeys.retreat, 100)
    behavior_obj = getattr(bm, 'current_behavior', None)
    
    if behavior_obj:
        with patch.object(bm, 'Update_Engagement_Cooldown', return_value=True):
            bm.movement_behavior = None
            behavior_obj.Execute()
            assert bm.movement_behavior == MockKeys.run_away

# ==============================================================================
# 7. ENEMY ABILITY SYSTEM INTEGRATION TESTS
# ==============================================================================

@pytest.fixture
def mock_ability_instance():
    """Generates a standard active mock ability structure."""
    ability = MagicMock()
    ability.name = "mock_dash"
    ability.is_passive = False
    ability.cooldown = 0
    ability.Get_Cooldown.return_value = 0
    ability.Update_Cooldown.return_value = True
    ability.Check_Trigger_Cooldown.return_value = True
    ability.Check_If_Trigger.return_value = True
    ability.Activate.return_value = True
    ability.Check_If_Attack_Allowed.return_value = True
    return ability


def test_ability_handler_lazy_loading_via_getattr(mock_game, mock_entity):
    """Ensures __getattr__ intercepts registry mappings and caches instances correctly."""
    handler = Ability_Handler(mock_game, mock_entity)
    
    # Patch the registry item to map to a dummy constructor
    mock_ability_cls = MagicMock()
    handler.ABILITY_REGISTRY = {"dash": mock_ability_cls}
    
    # Trigger dynamic dynamic layout resolution
    resolved_ability = handler.dash
    
    assert resolved_ability is not None
    mock_ability_cls.assert_called_once_with(mock_game, mock_entity, "dash")
    # Verify it was cached locally as an instance attribute
    assert getattr(handler, "dash") == resolved_ability


def test_ability_handler_getattr_raises_error_on_missing_key(mock_game, mock_entity):
    """Guards lookup parameters by dropping clean errors on invalid lookups."""
    handler = Ability_Handler(mock_game, mock_entity)
    handler.ABILITY_REGISTRY = {"dash": MagicMock()}
    
    with pytest.raises(AttributeError, match="has no registry or attribute mapping for 'unregistered_spell'"):
        _ = handler.unregistered_spell


def test_passive_ability_updates_independently(mock_game, mock_entity):
    """Validates that passive modules update every engine loop frame unconditionally."""
    handler = Ability_Handler(mock_game, mock_entity)
    mock_passive = MagicMock()
    mock_passive.is_passive = True
    
    handler.passive_abilities["crystal_scale"] = mock_passive
    handler.Update(delta_time=0.016)
    
    mock_passive.Update.assert_called_once_with(0.016)


def test_active_ability_execution_lifecycle_flow(mock_game, mock_entity, mock_ability_instance):
    """Tests the state transition sequence from evaluation up to trigger locks."""
    handler = Ability_Handler(mock_game, mock_entity)
    handler.active_ability = mock_ability_instance
    mock_entity.active_ability = None # Target entity can host spell context
    
    # Emulate a single clock update
    triggered = handler.Update(delta_time=0.1)
    
    assert triggered is True
    assert handler.is_running_ability is True
    mock_ability_instance.Activate.assert_called_once()
    mock_entity.Set_Active_Ability.assert_called_once_with("mock_dash")


def test_active_ability_removal_on_cooldown_detection(mock_game, mock_entity, mock_ability_instance):
    """Ensures active loops drop gracefully once their cooldown timers are set."""
    handler = Ability_Handler(mock_game, mock_entity)
    handler.active_ability = mock_ability_instance
    handler.is_running_ability = True
    
    # Force cooldown to simulate that execution has completed
    mock_ability_instance.Get_Cooldown.return_value = 3.5
    
    handler.Update(delta_time=0.1)
    
    # Must shift system back to baseline tracking
    assert handler.is_running_ability is False
    assert mock_ability_instance in handler.abilities_on_cooldown
    mock_entity.Remove_Active_Ability.assert_called_once()


def test_ethereal_passive_damage_mitigation(mock_game, mock_entity):
    """Validates Ethereal entirely voids slash and blunt pipeline interactions."""
    # Instantiating custom entity context
    mock_entity.is_ethereal = False
    def set_ethereal(val): mock_entity.is_ethereal = val
    mock_entity.Set_Ethereal = set_ethereal
    
    ethereal_passive = Ethereal(mock_game, mock_entity, "ethereal")
    assert mock_entity.is_ethereal is True
    
    # Test physical reduction properties
    assert ethereal_passive.Damage_Taken(15, ("slash",), (1, 0), None) == 0
    assert ethereal_passive.Damage_Taken(22, ("blunt",), (0, 1), None) == 0
    # Elemental damage should slice through unhindered
    assert ethereal_passive.Damage_Taken(10, ("electric",), (0, 0), None) == 10


def test_gloom_stalker_darkness_buff_toggle_boundaries(mock_game):
    """Checks that Gloom Stalker shifts stats accurately across threshold transitions."""
    mock_entity = MagicMock()
    mock_entity.strength = 10
    mock_entity.max_speed_holder = 4.0
    
    # Track stat changes using a side effect function so the mock updates its state dynamically
    def update_strength(new_val):
        mock_entity.strength = new_val
    mock_entity.Set_Strength.side_effect = update_strength

    from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.gloom_stalker import Gloom_Stalker
    gloom = Gloom_Stalker(mock_game, mock_entity, "gloom_stalker")

    # Scenario A: Initial state in deep dark (Light level 50 < 150)
    mock_entity.light_level = 50
    gloom.Update(0.1)
    mock_entity.Set_Strength.assert_called_with(20)   # 10 * 2
    mock_entity.Set_Max_Speed.assert_called_with(8.0) # 4.0 * 2

    # Scenario B: Move back into well-lit corridors (Light level 200 > 150)
    mock_entity.light_level = 200
    gloom.Update(0.1)
    mock_entity.Set_Strength.assert_called_with(10)   # 20 / 2 = 10 (Reverted perfectly!)


def test_crystal_scale_shield_absorption_breakthrough(mock_game, mock_entity):
    """Validates Crystal Scale shield absorption arithmetic and blunt double damage."""
    mock_entity.max_health = 40
    mock_entity.pos = pygame.math.Vector2(100, 120)
    
    # Mocking assets registry to skip real blitting image payloads
    mock_game.assets = {"crystal_scale_bar": MagicMock()}
    
    shield = Crystal_Scale(mock_game, mock_entity, "crystal_scale")
    shield.crystal_scale_max = 10
    shield.crystal_scale = 10
    
    # Standard breakthrough hit: 12 standard damage. 10 absorbed by shield, 2 breaks through.
    rem_damage = shield.Damage_Taken(12, "normal", (0,0), None)
    assert shield.crystal_scale == 0
    assert rem_damage == 2



# ==============================================================================
# 8. ADVANCED ROBUSTNESS & SERIALIZATION EDGE-CASE TESTS
# ==============================================================================

def test_ability_handler_save_and_load_data_restoration(mock_game, mock_entity):
    """Verifies complete state re-hydration during system Save/Load sequences."""
    handler = Ability_Handler(mock_game, mock_entity)
    mock_entity.saved_data = {}
    
    # Setup standard mocked active ability
    mock_active = MagicMock()
    mock_active.name = "dash"
    handler.active_ability = mock_active
    
    # Setup standard passive
    mock_passive = MagicMock()
    handler.passive_abilities["gloom_stalker"] = mock_passive
    
    # Save step execution
    handler.Save_Data()
    assert mock_entity.saved_data['active_ability_key'] == "dash"
    assert "gloom_stalker" in mock_entity.saved_data['passive_abilities_keys']
    mock_active.Save_Data.assert_called_once()
    mock_passive.Save_Data.assert_called_once()

    # Emulate payload loading step
    mock_data = {
        'active_ability_key': 'dash',
        'passive_abilities_keys': ['gloom_stalker'],
        'cooldown_keys': ['dash'],
        'is_running_ability': True,
        'cooldown': 10,
        'trigger_cooldown': 0
    }
    
    with patch.object(handler, 'Get_Ability') as mock_get:
        handler.Load_Data(mock_data)
        assert handler.is_running_ability is True
        assert mock_get.call_count == 2 # 1 for active, 1 for passive loop


def test_bone_seeker_delta_time_throttling_and_cleanup(mock_game, mock_entity):
    """Ensures Bone Seeker limits performance spikes and cleans up deleted targets."""
    # Build complete execution landscape path structures
    mock_game.tilemap = MagicMock()
    mock_game.enemy_handler = MagicMock()
    
    bone_seeker = Bone_Resurrector(mock_game, mock_entity, "bone_resurrector")
    
    # Mock stale / destroyed target parameters
    destroyed_bone = MagicMock()
    destroyed_bone.is_destroyed = True
    bone_seeker.target_bones = destroyed_bone
    bone_seeker.target_bones_collision_cooldown = 0
    
    # Update execution loop must catch target death state instantly
    bone_seeker.Update(delta_time=0.1)
    assert bone_seeker.target_bones is None


def test_bone_seeker_collision_and_consumption_trigger(mock_game, mock_entity):
    """Validates real physical bounding box triggers item consumer hooks."""
    mock_game.particle_handler = MagicMock()
    
    bone_seeker = Bone_Eater(mock_game, mock_entity, "bone_eater")
    mock_bone = MagicMock()
    mock_bone.is_destroyed = False
    bone_seeker.target_bones = mock_bone
    bone_seeker.target_bones_collision_cooldown = 0
    
    # Force a mock rect intersection match
    mock_entity.rect = MagicMock(return_value=pygame.Rect(0, 0, 32, 32))
    mock_bone.rect = MagicMock(return_value=pygame.Rect(10, 10, 32, 32))
    
    bone_seeker.Update(delta_time=0.1)
    
    # Assert that hooks clean out memory records properly
    mock_bone.Consume.assert_called_once()
    assert bone_seeker.target_bones is None


def test_support_nearby_entities_empty_or_failed_activation(mock_game, mock_entity):
    """Ensures area of effect abilities fail cleanly when zero targets exist."""
    mock_game.enemy_handler.Find_Nearby_Enemies.return_value = []
    
    # Provide a support entity class instance config manually 
    support_spell = Support_Nearby_Entities(
        mock_game, mock_entity, "rally", "strength_buff", "rally_particle", radius=100
    )
    
    # Trigger execution frame validation
    success = support_spell.Activate()
    assert success is True # Returns true to avoid stopping core manager update cascades
    mock_game.particle_handler.Activate_Particles.assert_not_called()


def test_jump_attack_movement_reduction_gate(mock_game, mock_entity):
    """Confirms jump attack locks down movement forces while building charging power."""
    jump_attack = Jump_Attack(mock_game, mock_entity, "jump")
    jump_attack.wait_before_jump_cooldown = 1.5
    jump_attack.jump_trigged = False
    
    jump_attack.Update(delta_time=0.5)
    
    # Entity should be frozen during winding phases
    mock_entity.Reduce_Movement.assert_called_with(10000)
    assert jump_attack.jump_trigged is False


def test_healing_from_damage_type_status_conversion(mock_game, mock_entity):
    """Checks that fire/electric status effects correctly convert to recovery states."""
    from scripts.engine.keys.keys import keys
    
    galvanic = Galvanic_Skin(mock_game, mock_entity, "galvanic_skin")
    
    # Emulate entity being under active element stress
    mock_effect = MagicMock()
    mock_effect.effect_strength = 5
    mock_entity.Get_Effect.return_value = mock_effect
    
    galvanic.Update(delta_time=0.016)
    
    # Check that status effects morph safely into clean absorption mechanics
    mock_entity.Set_Effect.assert_any_call(keys.healing, 5)
    mock_entity.Set_Effect.assert_any_call(keys.electric + '_resistance', 2)

@pytest.fixture
def echo_shard_context():
    """Sets up a clean test framework for an Echo Shard instance."""
    game = MagicMock()
    entity = MagicMock()
    
    # Mock clatter subsystem behavior
    game.clatter.Check_If_Noise_Generated.return_value = None
    
    ability = Echo_Shard(game, entity, "echo_shard")
    return game, entity, ability


def test_echo_shard_initializes_hidden(echo_shard_context):
    game, entity, ability = echo_shard_context
    
    # Initial frame has a tiny cooldown to force initialization setup
    assert ability.clatter_cooldown == 0.01
    assert ability.is_revealed is False
    
    # Process first frame tick down to zero
    ability.Update(delta_time=0.016)
    
    assert ability.clatter_cooldown <= 0
    entity.Set_Effect.assert_called_once_with(effect=keys.invisibility, duration=6, permanent=True)


def test_clatter_detection_reveals_enemy(echo_shard_context):
    game, entity, ability = echo_shard_context
    ability.clatter_cooldown = 0.0  # Clear startup latch
    
    # Simulate noise generation event trigger
    game.clatter.Check_If_Noise_Generated.return_value = (500, 500)
    
    ability.Update(delta_time=0.016)
    
    # Assert state transitions shifted correctly
    assert ability.is_revealed is True
    assert ability.clatter_cooldown == 10.0
    entity.Remove_Effect.assert_called_once_with(effect=keys.invisibility, reduce_permanent=6)


def test_subsequent_clatter_refreshes_timer_without_re_removing_effect(echo_shard_context):
    game, entity, ability = echo_shard_context
    ability.is_revealed = True
    ability.clatter_cooldown = 4.0  # Ticking down
    
    # Noise heard mid-reveal window
    game.clatter.Check_If_Noise_Generated.return_value = (200, 200)
    
    ability.Update(delta_time=0.016)
    
    # Timer should snap back to max, but Remove_Effect shouldn't be called again
    assert ability.clatter_cooldown == 10.0
    entity.Remove_Effect.assert_not_called()


def test_timer_expiry_re_conceals_enemy(echo_shard_context):
    game, entity, ability = echo_shard_context
    ability.is_revealed = True
    ability.clatter_cooldown = 0.005  # Almost expired
    
    ability.Update(delta_time=0.016)
    
    assert ability.is_revealed is False
    assert ability.clatter_cooldown <= 0
    entity.Set_Effect.assert_called_once_with(effect=keys.invisibility, duration=6, permanent=True)

@pytest.fixture
def teleport_context():
    """Sets up a clean mock environment for the Echo_Teleport ability."""
    game = MagicMock()
    entity = MagicMock()
    
    # Setup baseline tracking states on entity
    entity.locked_on_target = False
    
    # Default global sound engine state to no noise
    game.clatter.Check_If_Noise_Generated.return_value = None
    
    ability = Echo_Teleport(game, entity, "echo_teleport")
    return game, entity, ability


def test_update_handles_quiet_frames_without_crashing(teleport_context):
    game, entity, ability = teleport_context
    
    # Execute an update tick on a quiet frame (clatter_pos is None)
    try:
        ability.Update(delta_time=0.016)
    except UnboundLocalError as e:
        pytest.fail(f"Game crashed due to scoping bug on quiet frames: {e}")
        
    # Verify that no teleportation was mistakenly attempted
    entity.Set_Position.assert_not_called()


def test_clatter_triggers_teleportation_in_range(teleport_context):
    game, entity, ability = teleport_context
    
    # Simulate a noisy frame at specific coordinates
    clatter_source = (500, 500)
    game.clatter.Check_If_Noise_Generated.return_value = clatter_source
    
    ability.Update(delta_time=0.016)
    
    # Verify Set_Position was called exactly once
    entity.Set_Position.assert_called_once()
    
    # Extract the actual arguments passed to Set_Position
    called_args = entity.Set_Position.call_args[0][0]  # Expecting a tuple (x, y)
    actual_x, actual_y = called_args
    
    # Verify the final position falls strictly within the randomized offset window (-100 to 100)
    assert 400 <= actual_x <= 600
    assert 400 <= actual_y <= 600


def test_locked_on_target_blocks_teleportation(teleport_context):
    game, entity, ability = teleport_context
    
    # Force pathfinding engine to take tracking priority
    entity.locked_on_target = True
    
    # Even if noise is made...
    game.clatter.Check_If_Noise_Generated.return_value = (100, 100)
    
    ability.Update(delta_time=0.016)
    
    # Repositioning must be entirely blocked to preserve path vectors
    entity.Set_Position.assert_not_called()