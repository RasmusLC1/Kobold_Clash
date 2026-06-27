import pytest
from unittest.mock import MagicMock
import pygame
from collections import deque

from scripts.entities.moving_entities.moving_entity import Moving_Entity
from scripts.entities.moving_entities.moving_entity_functions.damage_text import Damage_Text
from scripts.entities.moving_entities.moving_entity_functions.damage_text_handler import Damage_Text_Handler
from scripts.engine.keys.keys import keys

@pytest.fixture(scope="session", autouse=True)
def headless_screen_context():
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture(autouse=True)
def clean_id_counters():
    from scripts.entities.entity.entities import PhysicsEntity
    PhysicsEntity._id_counter = 0
    PhysicsEntity._available_IDs = deque()

@pytest.fixture
def mock_game_context():
    game = MagicMock()
    game.render_scale = 1.0
    game.delta_time = 0.016
    game.tilemap.tile_size = 32
    game.tilemap.physics_rects_around.return_value = []
    
    game.enemy_handler = MagicMock()
    game.trap_handler = MagicMock()
    game.text_box_handler = MagicMock()
    
    mock_player = MagicMock()
    mock_player.rect.return_value = pygame.Rect(200, 200, 32, 32)
    game.player = mock_player
    return game

@pytest.fixture
def moving_entity(mock_game_context):
    entity = Moving_Entity(
        game=mock_game_context,
        type="enemy_kobold",
        category="monster",
        pos=[100.0, 100.0],
        size=(32, 32),
        health=100,
        strength=15,
        max_speed=2,
        agility=3,
        intelligence=10,
        stamina=10,
        sub_category="warrior"
    )
    
    # 1. Force fully mocked handlers directly on the instance to guarantee isolation
    entity.animation_handler = MagicMock()
    entity.effects = MagicMock()
    
    # 2. Setup mock layout context for tile checking logic if needed elsewhere
    entity.tile = MagicMock()
    entity.tile.Get_Distance_To_Player.return_value = 150
    entity.tile_handler = MagicMock()
    
    return entity



# --- 1. Vector Acceleration & Friction Physics Tests ---
def test_movement_acceleration_and_clamping(moving_entity):
    moving_entity.velocity = [0.0, 0.0]
    
    moving_entity.Update(tilemap=moving_entity.game.tilemap, delta_time=0.016, movement=(1, 0))
    
    assert moving_entity.velocity[0] > 0
    assert moving_entity.velocity[1] == 0
    
    # Force extreme velocity to test structural clamping limits
    moving_entity.velocity = [5000.0, 0.0]
    moving_entity.Update(tilemap=moving_entity.game.tilemap, delta_time=0.016, movement=(1, 0))
    
    # Expected: clamped max_speed (200.0) factored by 1 frame of friction (0.0001 ** 0.016)
    expected_speed = 200.0 * (moving_entity.movement.friction ** 0.016)
    
    # Use pytest.approx to handle floating-point precision variations smoothly
    assert moving_entity.velocity[0] == pytest.approx(expected_speed)



# 3. Combat Mitigation Tests
def test_damage_taken_respects_cooldowns(moving_entity):
    moving_entity.health = 100
    moving_entity.damage_cooldown = 0
    
    # Pass a valid direction vector (1, 0) instead of (0, 0) so your physics 
    # multiplier calculates changes and hits the internal Push pipelines cleanly.
    assert moving_entity.Damage_Taken(20, direction=(1, 0)) is True
    
    # Manually trigger cooldown frame matching real environment cycle logic
    moving_entity.Set_Damage_Cooldown()
    
    assert moving_entity.health == 80
    assert moving_entity.damage_cooldown > 0 
    
    # While cooldown is active, secondary hits are dropped
    assert moving_entity.Damage_Taken(20, direction=(1, 0)) is False
    assert moving_entity.health == 80



# --- 4. Serialization Loop ---
def test_moving_entity_save_and_load(moving_entity):
    # Initialize the container dictionary expected by PhysicsEntity superclasses
    moving_entity.saved_data = {}
    moving_entity.saved_data['ID'] = moving_entity.ID
    
    moving_entity.health = 42
    moving_entity.max_health = 120
    moving_entity.strength = 88
    moving_entity.target = (400, 500)
    
    moving_entity.animation_handler.animation = "run_west"
    moving_entity.effects.Save_Data.return_value = {"poison_ticks": 3}
    
    # Execute the save routine
    moving_entity.Save_Data()
    data_dump = moving_entity.saved_data  # Grab the data dict directly
    
    # Scramble stats to ensure loading overwrites state properly
    moving_entity.health = 999
    moving_entity.target = (0, 0)
    
    # Run payload restore step
    moving_entity.Load_Data(data_dump)
    
    assert moving_entity.health == 42
    assert moving_entity.max_health == 120
    assert moving_entity.strength == 88
    assert moving_entity.target == (400, 500)
    assert moving_entity.animation_handler.animation == "run_west"
    moving_entity.effects.Load_Data.assert_called_with({"poison_ticks": 3})

# --- 5. Knockback & Physics Force Vectors ---

def test_push_applies_positive_velocity_vectors(moving_entity):
    """Verifies that an incoming directional vector applies an immediate physics push."""
    moving_entity.velocity = [0.0, 0.0]
    direction_vector = (1.0, -1.0)  # Diagonal knockback up and to the right
    push_strength = 2.0
    
    moving_entity.Push(direction_vector, tilemap=moving_entity.game.tilemap, push_strength=push_strength)
    
    # Expected modifier: direction * strength * 500
    assert moving_entity.velocity[0] == 1.0 * 2.0 * 500
    assert moving_entity.velocity[1] == -1.0 * 2.0 * 500
    moving_entity.effects.Push.assert_called_with(direction_vector)


def test_push_enforces_absolute_strength_value(moving_entity):
    """Ensures negative strength arguments do not invert the intended knockback vector direction."""
    moving_entity.velocity = [0.0, 0.0]
    direction_vector = (1.0, 0.0)
    negative_strength = -3.5
    
    moving_entity.Push(direction_vector, tilemap=moving_entity.game.tilemap, push_strength=negative_strength)
    
    # Logic explicitly uses abs(push_strength), vector should remain positive along the X-axis
    assert moving_entity.velocity[0] > 0
    assert moving_entity.velocity[0] == 3.5 * 500


# --- 6. Grid Proximity & Entity Repulsion Mechanics ---

def test_apply_repulsion_pushes_weaker_entities(moving_entity):
    """Confirms stronger entities push away weaker ones when overlapping."""
    moving_entity.strength = 50  # High baseline strength pusher
    moving_entity.pos = [100.0, 100.0]
    
    # Construct a weaker target entity
    weak_enemy = MagicMock()
    weak_enemy.strength = 10
    weak_enemy.pos = [110.0, 100.0]  # Located slightly to the right
    
    # Seed the pusher set manually to trigger collision loops
    moving_entity.movement.pushed_entities.add(weak_enemy)
    
    collided = moving_entity.movement.Apply_Repulsion(tilemap=moving_entity.game.tilemap)
    
    assert collided is True
    # Verify a positive repulsion force multiplier was passed down explicitly
    # Formula: 1 + (50 - 10) / 10 = 5.0
    weak_enemy.Push.assert_called_once()
    called_args = weak_enemy.Push.call_args[1]
    assert called_args['push_strength'] == pytest.approx(5.0)


def test_movement_acceleration_and_clamping(moving_entity):
    moving_entity.velocity = [0.0, 0.0]

    moving_entity.Update(tilemap=moving_entity.game.tilemap, delta_time=0.016, movement=(1, 0))

    assert moving_entity.velocity[0] > 0
    assert moving_entity.velocity[1] == 0

    # Force extreme velocity to test clamping
    moving_entity.velocity = [5000.0, 0.0]
    moving_entity.Update(tilemap=moving_entity.game.tilemap, delta_time=0.016, movement=(1, 0))

    # New model: clamp to max_speed first, then drag only applies on axes with no input.
    # movement=(1, 0) means X has active input, so drag is NOT applied on X.
    # Result should just be max_speed.
    expected_speed = moving_entity.movement.max_speed
    assert moving_entity.velocity[0] == pytest.approx(expected_speed, rel=1e-3)
