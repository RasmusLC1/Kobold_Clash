import pytest
from unittest.mock import MagicMock, patch

# Adjust import paths to match your project structure if necessary
from scripts.engine.awakening.clatter import Clatter, CLATTER_COOLDOWN, SILENCE_MULTIPLIER
from scripts.engine.keys.keys import keys

@pytest.fixture
def mock_game():
    """Provides a mocked game instance with nested player and enemy handlers."""
    game = MagicMock()
    
    # Mock Player setup
    game.player = MagicMock()
    game.player.active_ability = None
    
    # Mock Enemy Handler setup
    game.enemy_handler = MagicMock()
    game.enemy_handler.Find_Nearby_Enemies.return_value = []
    
    return game

@pytest.fixture
def clean_clatter(mock_game):
    """Provides a fresh instance of Clatter with heavily mocked Awakening dependency."""
    # Patch Awakening during initialization so it doesn't try to look up real files/assets
    with patch('scripts.engine.awakening.clatter.Awakening') as MockAwakening:
        clatter_instance = Clatter(mock_game)
        # Keep a reference to the mocked awakening instance for assertions
        clatter_instance.mock_awakening = MockAwakening.return_value
        return clatter_instance


def test_clatter_cooldown_decreases(clean_clatter):
    """Tests that Update properly ticks down the cooldown timer until it hits 0."""
    clean_clatter.Set_Clatter_Cooldown()  # Sets it to CLATTER_COOLDOWN (0.5)
    assert clean_clatter.clatter_cooldown_handler.value == CLATTER_COOLDOWN

    # Tick down by 0.2 seconds
    clean_clatter.Update(delta_time=0.2)
    assert pytest.approx(clean_clatter.clatter_cooldown_handler.value) == 0.3

    # Tick past zero to ensure it caps cleanly or handles guard returns
    clean_clatter.Update(delta_time=0.4)
    assert clean_clatter.clatter_cooldown_handler.value <= 0


def test_generate_clatter_success_triggers_events(clean_clatter, mock_game):
    """Tests that generating a clatter when off cooldown triggers systems and queues enemies."""
    clean_clatter.clatter_cooldown_handler.value = 0  # Ready to trigger

    mock_enemy_1 = MagicMock(locked_on_target=False)
    mock_enemy_2 = MagicMock(locked_on_target=False)
    mock_game.enemy_handler.Find_Nearby_Enemies.return_value = [mock_enemy_1, mock_enemy_2]

    center_pos = (10, 10)
    base_range = 300

    clean_clatter.Generate_Clatter(center=center_pos, clatter_range=base_range)

    # Cooldown should be reset
    assert clean_clatter.clatter_cooldown_handler.value == CLATTER_COOLDOWN

    clean_clatter.mock_awakening.Trigger_Awakening.assert_called_once()

    mock_game.enemy_handler.Find_Nearby_Enemies.assert_called_with(mock_game.player, base_range)

    assert mock_game.enemy_handler.Add_To_Pathfinding_Queue.call_count == 2
    mock_game.enemy_handler.Add_To_Pathfinding_Queue.assert_any_call(mock_enemy_1, center_pos)
    mock_game.enemy_handler.Add_To_Pathfinding_Queue.assert_any_call(mock_enemy_2, center_pos)


def test_generate_clatter_ignored_when_on_cooldown(clean_clatter, mock_game):
    """Tests that calling Generate_Clatter while a cooldown is active does nothing."""
    clean_clatter.clatter_cooldown_handler.value = 0.4  # Active cooldown

    clean_clatter.Generate_Clatter(center=(0, 0), clatter_range=100)

    # Cooldown shouldn't be altered back to full 0.5
    assert clean_clatter.clatter_cooldown_handler.value == 0.4
    clean_clatter.mock_awakening.Trigger_Awakening.assert_not_called()
    mock_game.enemy_handler.Find_Nearby_Enemies.assert_not_called()
def test_generate_clatter_filters_locked_on_enemies(clean_clatter, mock_game):
    """Ensures enemies that are already locked onto a target are omitted from the queue."""
    clean_clatter.clatter_cooldown = 0
    
    unlocked_enemy = MagicMock(locked_on_target=False)
    locked_enemy = MagicMock(locked_on_target=True)
    mock_game.enemy_handler.Find_Nearby_Enemies.return_value = [unlocked_enemy, locked_enemy]
    
    clean_clatter.Generate_Clatter(center=(0, 0), clatter_range=100)
    
    # Only the unlocked enemy makes it into the queue setup
    mock_game.enemy_handler.Add_To_Pathfinding_Queue.assert_called_once_with(unlocked_enemy, (0, 0))


def test_silence_modifier_reduces_range(clean_clatter, mock_game):
    """Verifies that the silence ability dynamically shrinks the clatter radius."""
    mock_game.player.active_ability = keys.silence
    
    mock_effect = MagicMock()
    mock_effect.effect_strength = 2  # 2 * SILENCE_MULTIPLIER (100) = 200 reduction
    mock_game.player.Get_Effect.return_value = mock_effect
    
    # Initial range 500 - 200 = 300 expected
    modified_range = clean_clatter.Calculate_Silence_Modifier(clatter_range=500)
    assert modified_range == 300


def test_silence_modifier_clamped_to_minimum(clean_clatter, mock_game):
    """Ensures powerful silence modifiers cannot drop clatter range below 1."""
    mock_game.player.active_ability = keys.silence
    
    mock_effect = MagicMock()
    mock_effect.effect_strength = 10  # 10 * 100 = 1000 reduction
    mock_game.player.Get_Effect.return_value = mock_effect
    
    # 100 - 1000 would be negative, should clamp to 1
    modified_range = clean_clatter.Calculate_Silence_Modifier(clatter_range=100)
    assert modified_range == 1


# ==================== EXTENDED NEW TESTS ====================

def test_generate_clatter_broadcasts_to_acoustic_subscribers(clean_clatter, mock_game):
    """Verifies that successful clatter events are instantly broadcast to the observer channel."""
    clean_clatter.clatter_cooldown = 0
    target_pos = (450, 200)
    
    clean_clatter.Generate_Clatter(center=target_pos, clatter_range=200)
    
    # Confirm the message was published directly to the subscription matrix
    mock_game.enemy_handler.clatter_subscription.Broadcast_Clatter.assert_called_once_with(target_pos)


def test_check_clatter_cooldown_reflects_state_correctly(clean_clatter):
    """Validates the boolean output accuracy of Check_Clatter_Cooldown."""
    clean_clatter.clatter_cooldown = 0.0
    assert clean_clatter.Check_Clatter_Cooldown() is False
    
    clean_clatter.clatter_cooldown = 0.2
    assert clean_clatter.Check_Clatter_Cooldown() is True


def test_awakening_level_management(clean_clatter):
    """Validates getter, increments, and reset pipelines for dungeon awakening state properties."""
    # Setup initial mock properties
    clean_clatter.mock_awakening.awakening_level = 3
    
    # Test Getter proxy
    assert clean_clatter.Get_Awakening_Level() == 3
    
    # Test Incrementor mechanics
    clean_clatter.Increase_Awakening()
    clean_clatter.mock_awakening.Set_Awakening_Level.assert_called_with(4)
    
    # Test Reset structural commands
    clean_clatter.Reset_Awakening_Level()
    assert clean_clatter.mock_awakening.awakening_cooldown == 0
    clean_clatter.mock_awakening.Set_Awakening_Level.assert_called_with(0)