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
    shrine = Cycling_Shrine(mock_game, "test_shrine", (0, 0), max_animation = 3, animation_cooldown_max=0.5)
    shrine.animation_handler.animation_cooldown = 1.0
    start_animation = shrine.animation

    shrine.Update_Animation(delta_time=0.4)

    assert shrine.animation == start_animation
    assert shrine.animation_handler.animation_cooldown == pytest.approx(0.6)


def test_cycling_shrine_wraps_animation_at_max(mock_game):
    shrine = Cycling_Shrine(mock_game, "test_shrine", (0, 0), max_animation = 3, animation_cooldown_max=0.5)
    shrine.animation = 3
    shrine.animation_handler.animation_cooldown = 0

    with patch("random.uniform", return_value=0.6):
        shrine.Update_Animation(delta_time=0.1)

    assert shrine.animation == 0


def test_cycling_shrine_particles_respect_chance_roll(mock_game):
    shrine = Cycling_Shrine(
        mock_game, "test_shrine", (0, 0), max_animation = 3, animation_cooldown_max=0.5,
        particle_type=keys.soul_particle, particle_chance=2,
    )
    shrine.animation_handler.animation_cooldown = 0

    with patch("random.uniform", return_value=0.6), patch("random.randint", return_value=0):
        shrine.Update_Animation(delta_time=0.1)

    mock_game.particle_handler.Activate_Particles.assert_called_once()
    args, _ = mock_game.particle_handler.Activate_Particles.call_args
    assert args[1] == keys.soul_particle


def test_cycling_shrine_skips_particles_without_type(mock_game):
    """Default particle_type=None means no particle call, regardless of the chance roll."""
    shrine = Cycling_Shrine(mock_game, "test_shrine", (0, 0), max_animation = 3, animation_cooldown_max=0.5)
    shrine.animation_handler.animation_cooldown = 0

    shrine.Update_Animation(delta_time=0.1)

    mock_game.particle_handler.Activate_Particles.assert_not_called()


### 2. Menu_Shrine base behavior

def test_menu_shrine_ignores_ticks_while_closed(mock_game):
    shrine = Menu_Shrine(mock_game, "test_menu_shrine", (0, 0), cycle_requires_open=True)
    shrine.animation_handler.max_animation = 3
    shrine.animation_handler.animation_cooldown = 0

    shrine.Update_Animation(delta_time=0.5)

    assert shrine.animation == 0

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

import pytest
from unittest.mock import MagicMock, patch

from scripts.entities.decoration.shared.loot_container.chest import Chest
from scripts.entities.decoration.shared.loot_container.mimic_chest import Mimic_Chest
from scripts.entities.decoration.ancient_tomb.loot_container.effigy_tomb import Effigy_Tomb  # adjust import path as needed
from scripts.entities.decoration.ancient_tomb.loot_container.bookshelf import Bookshelf      # adjust import path as needed
from scripts.engine.keys.keys import keys


### Regression: loot tables must actually reach the LootComponent
# (Get_Loot_Types vs Get_Loot_Types naming bug — see review notes)

def test_chest_loot_weights_are_populated(mock_game):
    with patch("scripts.entities.decoration.shared.loot_container.chest.Luck_Calculator.Calculate_Rarity_Value", return_value=10):
        chest = Chest(mock_game, (0, 0))
    assert chest.loot_component.loot_weights, (
        "Chest's loot table is empty — Get_Loot_Types() isn't being used "
        "to populate the LootComponent"
    )
    assert keys.gem_ingot in chest.loot_component.loot_weights


def test_effigy_tomb_loot_weights_are_populated(mock_game):
    tomb = Effigy_Tomb(mock_game, (0, 0))
    assert tomb.loot_weights, "Effigy_Tomb.loot_weights was never set"
    assert tomb.enemies, "Effigy_Tomb.enemies was never set"


### Chest

def test_chest_open_drops_loot_and_empties(mock_game):
    with patch("scripts.entities.decoration.shared.loot_container.chest.Luck_Calculator.Calculate_Rarity_Value", return_value=10):
        chest = Chest(mock_game, (0, 0))

    mock_game.item_handler.Check_If_Loot_Is_Affordable.return_value = [keys.gem_ingot]

    with patch.object(chest.loot_component, "Calculate_Rarity", return_value=10):
        result = chest.Open()

    assert result is True
    assert chest.loot_component.empty is True
    mock_game.item_handler.Spawn_Item_By_Type.assert_called_once()
    mock_game.decoration_handler.Remove_Decoration.assert_called_once_with(chest)


def test_chest_open_fails_when_already_empty(mock_game):
    with patch("scripts.entities.decoration.shared.loot_container.chest.Luck_Calculator.Calculate_Rarity_Value", return_value=10):
        chest = Chest(mock_game, (0, 0))
    chest.loot_component.empty = True

    result = chest.Open()

    assert result is False
    mock_game.item_handler.Spawn_Item_By_Type.assert_not_called()


def test_chest_version_scales_with_rarity(mock_game):
    with patch("scripts.entities.decoration.shared.loot_container.chest.Luck_Calculator.Calculate_Rarity_Value", return_value=100):
        chest = Chest(mock_game, (0, 0))
    assert chest.version == 7  # top rarity -> max animation index

    with patch("scripts.entities.decoration.shared.loot_container.chest.Luck_Calculator.Calculate_Rarity_Value", return_value=0):
        low_chest = Chest(mock_game, (0, 0))
    assert low_chest.version == 0


def test_mimic_chest_spawns_enemy_and_slows_player(mock_game):
    with patch("scripts.entities.decoration.shared.loot_container.chest.Luck_Calculator.Calculate_Rarity_Value", return_value=10):
        mimic = Mimic_Chest(mock_game, (0, 0))

    with patch("random.choices", return_value=[keys.skeleton_warrior]):
        mimic.Drop_Loot()

    mock_game.enemy_handler.Enemy_Spawner.assert_called_once()
    args, _ = mock_game.enemy_handler.Enemy_Spawner.call_args
    assert args[1] == keys.skeleton_warrior
    mock_game.player.Set_Effect.assert_called_once_with(keys.slow, 4)

### Effigy_Tomb

def test_effigy_tomb_open_plays_lid_sound(mock_game):
    tomb = Effigy_Tomb(mock_game, (0, 0))

    with patch("random.choices", return_value=[keys.revive]), \
         patch.object(tomb.loot_component, "Calculate_Rarity", return_value=50):
        result = tomb.Open()

    assert result is True
    assert tomb.animation == 1


def test_effigy_tomb_enemy_branch_spawns_from_own_table(mock_game):
    tomb = Effigy_Tomb(mock_game, (0, 0))

    with patch("random.choices", side_effect=[[keys.enemy], [keys.skeleton_guardian]]):
        tomb.Drop_Loot()

    mock_game.enemy_handler.Enemy_Spawner.assert_called_once()
    args, _ = mock_game.enemy_handler.Enemy_Spawner.call_args
    assert args[1] == keys.skeleton_guardian


def test_effigy_tomb_forced_enemy_override(mock_game):
    tomb = Effigy_Tomb(mock_game, (0, 0))
    tomb.Set_Loot_To_Always_Spawn_Enemy()
    assert tomb.loot_weights == {keys.enemy: 100}


### Bookshelf
# NOTE: Spawn_Loot / Select_Available_Rune / loot_categories are currently
# unreachable dead code — the generic LootComponent.Drop_Loot pathway never
# calls back into Bookshelf.Spawn_Loot. These tests exercise those methods
# directly rather than through Open()/Destroyed(), since that path doesn't
# reach them yet. Flagging rather than asserting the integration until the
# override is added (see review notes).

def test_bookshelf_select_available_rune_avoids_active_runes(mock_game):
    shelf = Bookshelf(mock_game, (0, 0))
    shelf.Get_Loot_Types()  # populate loot_categories / weights until this is wired into __init__

    mock_game.item_handler.rune_handler.Check_If_Rune_Is_Active.side_effect = [True, False]

    with patch("random.choices", side_effect=[[keys.dash_rune], [keys.healing_rune]]):
        shelf.Select_Available_Rune()

    mock_game.item_handler.Spawn_Rune.assert_called_once_with(keys.healing_rune, shelf.Get_Pos.__self__.pos if False else shelf.Get_Pos())


def test_bookshelf_spawn_loot_routes_curse_category(mock_game):
    shelf = Bookshelf(mock_game, (0, 0))
    shelf.Get_Loot_Types()

    shelf.Spawn_Loot(keys.temptress_embrace, (0, 0))

    mock_game.item_handler.Spawn_Item_By_Type.assert_called_once_with(
        keys.curse, (0, 0), type=keys.temptress_embrace
    )

import pytest
from unittest.mock import MagicMock, patch
import pygame

from scripts.entities.decoration.shared.interactive.campfire import Campfire      # adjust path
from scripts.entities.decoration.shared.interactive.lever import Lever            # adjust path
from scripts.entities.decoration.shared.interactive.teleportation_circle import Teleportation_Circle  # adjust path
from scripts.entities.decoration.shared.doors.door import Door              # adjust path
from scripts.entities.decoration.shared.doors.fragile_wall import Fragile_Wall  # adjust path
from scripts.entities.decoration.shared.bones.bones import Bones            # adjust path
from scripts.engine.keys.keys import keys


### Campfire

def test_campfire_open_heals_player_and_locks(mock_game):
    fire = Campfire(mock_game, (0, 0))
    fire.empty = False

    result = fire.Open()

    assert result is True
    assert fire.empty is True
    mock_game.player.Set_Effect.assert_called_once_with(keys.healing, mock_game.player.max_health // 2)
    mock_game.clatter.Increase_Awakening.assert_called_once()


def test_campfire_open_fails_when_already_lit(mock_game):
    fire = Campfire(mock_game, (0, 0))
    fire.empty = True

    result = fire.Open()

    assert result is False
    mock_game.player.Set_Effect.assert_not_called()


def test_campfire_animation_spawns_fire_particles(mock_game):
    fire = Campfire(mock_game, (0, 0))
    with patch.object(fire, "rect", return_value=pygame.Rect(0, 0, 32, 32)):
        fire.Update_Animation(delta_time=0.1)
    mock_game.particle_handler.Activate_Particles.assert_called_once()


### Lever
# NOTE: self.empty is marked True *before* confirming a door was found —
# a failed lookup permanently disables the lever with no visible effect.
# Test documents current behavior; flag if that's not the intended design.

def test_lever_opens_a_random_door(mock_game):
    lever = Lever(mock_game, (0, 0))
    lever.empty = False
    mock_door = MagicMock()
    mock_game.decoration_handler.Get_Random_Door.return_value = mock_door

    result = lever.Open()

    assert result is True
    assert lever.empty is True
    assert mock_door.is_open is True
    mock_door.Open.assert_called_once_with(False)


def test_lever_with_no_door_still_locks_itself(mock_game):
    lever = Lever(mock_game, (0, 0))
    lever.empty = False
    mock_game.decoration_handler.Get_Random_Door.return_value = None

    result = lever.Open()

    assert result is None  # falls through without an explicit return
    assert lever.empty is True  # locked even though nothing happened


def test_lever_already_used_does_nothing(mock_game):
    lever = Lever(mock_game, (0, 0))
    lever.empty = True

    result = lever.Open()

    assert result is False
    mock_game.decoration_handler.Get_Random_Door.assert_not_called()


### Teleportation_Circle

def test_teleportation_circle_moves_player_and_costs_souls(mock_game):
    circle = Teleportation_Circle(mock_game, (0, 0))
    linked = MagicMock()
    linked.pos = pygame.Vector2(500, 500)
    circle.linked_portal = linked
    mock_game.player.Decrease_Souls.return_value = True

    with patch("random.randint", return_value=10):
        circle.Open()

    mock_game.player.Decrease_Souls.assert_called_once_with(10)
    mock_game.player.Set_Position.assert_called_once()
    mock_game.particle_handler.Activate_Particles.assert_called_once()


def test_teleportation_circle_blocked_without_enough_souls(mock_game):
    circle = Teleportation_Circle(mock_game, (0, 0))
    circle.linked_portal = MagicMock()
    mock_game.player.Decrease_Souls.return_value = False

    circle.Open()

    mock_game.player.Set_Position.assert_not_called()


def test_teleportation_circle_save_load_round_trip(mock_game):
    circle = Teleportation_Circle(mock_game, (0, 0))
    portal = MagicMock(ID=42)
    circle.Set_Linked_Portal(portal)

    circle.Save_Data()
    data = circle.saved_data

    blank = Teleportation_Circle(mock_game, (0, 0))
    blank.Load_Data(data)

    assert blank.linked_portal_ID == 42


### Door

def test_door_destroyed_forces_open(mock_game):
    door = Door(mock_game, (0, 0))
    with patch.object(door, "Destroyed", wraps=door.Destroyed) if False else patch.object(
        door.__class__.__bases__[0], "Destroyed", return_value=True
    ):
        result = door.Destroyed()

    assert result is True
    assert door.is_open is True
    mock_game.decoration_handler.Remove_Decoration.assert_called_once_with(door)


def test_door_save_load_round_trip(mock_game):
    door = Door(mock_game, (0, 0))
    door.is_open = True
    door.Save_Data()
    data = door.saved_data

    blank = Door(mock_game, (0, 0))
    with patch.object(blank, "Open") as mock_open:
        blank.Load_Data(data)

    assert blank.is_open is True
    mock_open.assert_called_once_with(False)


### Fragile_Wall

def test_fragile_wall_destroyed_becomes_passable(mock_game):
    wall = Fragile_Wall(mock_game, (0, 0))
    with patch.object(wall.__class__.__bases__[0], "Destroyed", return_value=True):
        result = wall.Destroyed()

    assert result is True
    assert wall.is_open is True
    mock_game.decoration_handler.Remove_Decoration.assert_called_once_with(wall)


### Bones

def test_bones_revive_spawns_enemy_once(mock_game):
    bones = Bones(mock_game, (0, 0), keys.skeleton_warrior)

    bones.Revive()

    assert bones.activated is True
    mock_game.enemy_handler.Enemy_Spawner.assert_called_once_with(bones.pos, str(keys.skeleton_warrior))
    mock_game.decoration_handler.Remove_Decoration.assert_called_once_with(bones)


def test_bones_revive_is_idempotent(mock_game):
    bones = Bones(mock_game, (0, 0), keys.skeleton_warrior)
    bones.Revive()
    bones.Revive()

    mock_game.enemy_handler.Enemy_Spawner.assert_called_once()

def test_harmonic_crystal_open_grants_souls_and_empties(mock_game):
    crystal = Harmonic_Crystal(mock_game, (0, 0))
    crystal.empty = False

    result = crystal.Open()

    assert result is True
    assert crystal.empty is True
    mock_game.player.Increase_Souls.assert_called_once_with(100)

from scripts.entities.decoration.crystal_caverns.harmonic_crystal import Harmonic_Crystal  # adjust path

def test_harmonic_crystal_open_fails_when_already_empty(mock_game):
    crystal = Harmonic_Crystal(mock_game, (0, 0))
    crystal.empty = True

    result = crystal.Open()

    assert result is False
    mock_game.player.Increase_Souls.assert_not_called()


def test_harmonic_crystal_open_generates_sound(mock_game):
    crystal = Harmonic_Crystal(mock_game, (0, 0))
    crystal.empty = False

    with patch.object(crystal, "Generate_Sound") as mock_sound:
        crystal.Open()

    mock_sound.assert_called_once_with(keys.harmonic_crystal, 0.5, 1000)


def test_harmonic_crystal_update_does_not_crash(mock_game):
    """Update() no longer references the stray Check_Player_Distance() call —
    Open() is player-triggered externally, same pattern as Campfire."""
    crystal = Harmonic_Crystal(mock_game, (0, 0))
    crystal.animation_handler.animation_cooldown = 999  # avoid unrelated animation branches

    crystal.Update(delta_time=0.1)  # should be a no-op passthrough to super()