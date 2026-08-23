import pytest
from unittest.mock import MagicMock, patch
import pygame
from collections import deque

# Adjust imports to point to your actual engine directory structure
from scripts.entities.entity.entities import PhysicsEntity
from scripts.entities.decoration.shared.shrine.shrine import Cycling_Shrine, Menu_Shrine
from scripts.entities.decoration.shared.shrine.shrine_reward_pools import GOOD_REWARDS
from scripts.entities.decoration.ancient_tomb.shrine.blood_shrine import Blood_Shrine
from scripts.entities.decoration.shared.shrine.shrine_types.sacrifice_shrine import Sacrifice_Shrine, RewardType
from scripts.entities.decoration.shared.shrine.shrine_types.hunter_shrine import Hunter_Shrine
from scripts.engine.keys.keys import keys

@pytest.fixture(scope="session", autouse=True)
def headless_pygame_context():
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture(autouse=True)
def reset_entity_id_counters():
    PhysicsEntity._id_counter = 0
    PhysicsEntity._available_IDs = deque()
    yield

@pytest.fixture
def mock_game():
    game = MagicMock()
    game.tilemap.tile_size = 32

    mock_tile = MagicMock()
    mock_tile.pos = (0, 0)
    mock_tile.light_level = 5
    mock_tile.scaled_pos = (0, 0)

    game.tilemap.Current_Tile.return_value = mock_tile
    game.tilemap.Get_Random_Tile_With_Path_To_Player.return_value = mock_tile

    game.light_handler.Add_Light.return_value = MagicMock(name="light_source_handle")
    game.light_handler.Initialise_Light_Level.return_value = 10

    game.player.health = 100
    game.rune_handler.active_runes = []

    return game


### 1. Cycling_Shrine base behavior

def test_cycling_shrine_holds_frame_during_cooldown(mock_game):
    shrine = Cycling_Shrine(mock_game, "test_shrine", (0, 0), cooldown_range=(0.5, 0.7))
    shrine.max_animation = 3
    shrine.animation_cooldown = 1.0

    shrine.Update_Animation(delta_time=0.4)

    assert shrine.animation == 0
    assert shrine.animation_cooldown == pytest.approx(0.6)


def test_cycling_shrine_wraps_animation_at_max(mock_game):
    shrine = Cycling_Shrine(mock_game, "test_shrine", (0, 0), cooldown_range=(0.5, 0.7))
    shrine.max_animation = 3
    shrine.animation = 3
    shrine.animation_cooldown = 0

    with patch("random.uniform", return_value=0.6):
        shrine.Update_Animation(delta_time=0.1)

    assert shrine.animation == 0


def test_cycling_shrine_particles_respect_chance_roll(mock_game):
    shrine = Cycling_Shrine(
        mock_game, "test_shrine", (0, 0), cooldown_range=(0.5, 0.7),
        particle_type=keys.soul_particle, particle_chance=2,
    )
    shrine.max_animation = 3
    shrine.animation_cooldown = 0

    with patch("random.uniform", return_value=0.6), patch("random.randint", return_value=0):
        shrine.Update_Animation(delta_time=0.1)

    mock_game.particle_handler.Activate_Particles.assert_called_once()
    args, _ = mock_game.particle_handler.Activate_Particles.call_args
    assert args[1] == keys.soul_particle


def test_cycling_shrine_skips_particles_without_type(mock_game):
    """Default particle_type=None means no particle call, regardless of the chance roll."""
    shrine = Cycling_Shrine(mock_game, "test_shrine", (0, 0), cooldown_range=(0.5, 0.7))
    shrine.max_animation = 3
    shrine.animation_cooldown = 0

    shrine.Update_Animation(delta_time=0.1)

    mock_game.particle_handler.Activate_Particles.assert_not_called()


### 2. Menu_Shrine base behavior

def test_menu_shrine_ignores_ticks_while_closed(mock_game):
    shrine = Menu_Shrine(mock_game, "test_menu_shrine", (0, 0), cycle_requires_open=True)
    shrine.max_animation = 3
    shrine.animation_cooldown = 0

    shrine.Update_Animation(delta_time=0.5)

    assert shrine.animation == 0


def test_menu_shrine_cycles_once_open(mock_game):
    shrine = Menu_Shrine(mock_game, "test_menu_shrine", (0, 0), cycle_requires_open=True)
    shrine.is_open = True
    shrine.min_animation = 1
    shrine.max_animation = 3
    shrine.animation_cooldown = 0

    with patch("random.randint", return_value=2) as mocked_randint:
        shrine.Update_Animation(delta_time=0.1)

    mocked_randint.assert_called_once_with(1, 3)
    assert shrine.animation == 2


def test_menu_shrine_cycles_regardless_of_open_state(mock_game):
    """cycle_requires_open=False (Rune_Shrine's original behavior) animates even while closed."""
    shrine = Menu_Shrine(mock_game, "test_menu_shrine", (0, 0), cycle_requires_open=False)
    shrine.max_animation = 3
    shrine.animation_cooldown = 0

    with patch("random.randint", return_value=2):
        shrine.Update_Animation(delta_time=0.1)

    assert shrine.animation == 2


def test_menu_shrine_save_load_round_trip(mock_game):
    """Reads shrine.saved_data directly — Save_Data() itself currently returns None
    (Decoration/Shrine don't propagate PhysicsEntity's return value; flagged separately)."""
    shrine = Menu_Shrine(mock_game, "test_menu_shrine", (0, 0))
    shrine.is_open = True

    shrine.Save_Data()
    data = shrine.saved_data

    blank = Menu_Shrine(mock_game, "test_menu_shrine", (0, 0))
    blank.Load_Data(data)

    assert blank.is_open is True


### 3. Blood_Shrine (return-value regression from earlier review)

def test_blood_shrine_open_reports_success(mock_game):
    shrine = Blood_Shrine(mock_game, (0, 0))
    mock_game.player.health = 100

    result = shrine.Open()

    assert result is True
    assert shrine.empty is True
    mock_game.player.Set_Health.assert_called_once_with(50)
    mock_game.player.Set_Effect.assert_called_once_with(keys.vampiric, 1, True)


def test_blood_shrine_open_fails_when_already_empty(mock_game):
    shrine = Blood_Shrine(mock_game, (0, 0))
    shrine.empty = True

    result = shrine.Open()

    assert result is False
    mock_game.player.Set_Health.assert_not_called()


### 4. Sacrifice_Shrine reward tiers

def test_sacrifice_shrine_guarantees_good_reward_at_high_value(mock_game):
    shrine = Sacrifice_Shrine(mock_game, (0, 0))
    item = MagicMock(amount=1, value=150)

    assert shrine.Calculate_Reward(item) == RewardType.GOOD


def test_sacrifice_shrine_no_bad_reward_at_fifty_threshold(mock_game):
    """At value == 50, BAD should never be reachable — result is either MID or GOOD depending on the roll."""
    shrine = Sacrifice_Shrine(mock_game, (0, 0))
    item = MagicMock(amount=1, value=50)

    with patch("random.random", return_value=0.1):  # low roll -> MID
        assert shrine.Calculate_Reward(item) == RewardType.MID

    with patch("random.random", return_value=0.9):  # high roll -> GOOD
        assert shrine.Calculate_Reward(item) == RewardType.GOOD


def test_sacrifice_shrine_spawn_reward_uses_shared_pool(mock_game):
    shrine = Sacrifice_Shrine(mock_game, (0, 0))
    item = MagicMock(amount=1, value=150)  # guarantees GOOD
    picked = list(GOOD_REWARDS.items())[0]

    with patch("random.choice", return_value=picked):
        result = shrine.Spawn_Reward(item)

    assert result is True
    mock_game.item_handler.Remove_Item.assert_called_once_with(item, True)
    mock_game.player.Set_Effect.assert_called_once_with(*picked, True)
    mock_game.clatter.Generate_Clatter.assert_called_once_with(shrine.pos, 200)


### 5. Hunter_Shrine treasure flow

def test_hunter_shrine_open_spawns_treasure_and_locks(mock_game):
    shrine = Hunter_Shrine(mock_game, (0, 0))

    result = shrine.Open()

    assert result is True
    assert shrine.empty is True
    assert len(shrine.treasures) == 3
    mock_game.sound_handler.Play_Sound.assert_called_with(keys.hunter_shrine_activation, 0.4)


def test_hunter_shrine_rejects_wrong_item_type(mock_game):
    shrine = Hunter_Shrine(mock_game, (0, 0))
    shrine.animation = 1
    wrong_item = MagicMock(type="not_treasure")

    assert shrine.Spawn_Reward(wrong_item) is False


def test_hunter_shrine_spawn_reward_clears_treasures(mock_game):
    shrine = Hunter_Shrine(mock_game, (0, 0))
    shrine.animation = 1
    shrine.treasures = [MagicMock(), MagicMock()]
    treasure_item = MagicMock(type=keys.hunter_treasure)
    picked = list(GOOD_REWARDS.items())[0]

    with patch("random.choice", return_value=picked):
        result = shrine.Spawn_Reward(treasure_item)

    assert result is True
    assert shrine.treasures == []
    mock_game.clatter.Generate_Clatter.assert_called_once_with(shrine.pos, 1000)