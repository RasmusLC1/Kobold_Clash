# tests/test_traps.py
import os
from collections import deque
from unittest.mock import MagicMock, Mock, patch

import pytest
import pygame

from scripts.engine.keys.keys import keys
from scripts.entities.entity.entities import PhysicsEntity
from scripts.entities.traps.traps.shared.spike import Spike
from scripts.entities.traps.traps.shared.spike_poisoned import Spike_Poisoned
from scripts.entities.traps.traps.shared.spike_pit import Spike_Pit
from scripts.entities.traps.traps.shared.spider_web import Spider_Web
from scripts.entities.traps.traps.shared.rubble import Rubble
from scripts.entities.traps.traps.shared.poison_plume import Poison_Plume
from scripts.entities.traps.traps.shared.fire_trap import Fire_Trap
from scripts.entities.traps.traps.ancient_tomb.tomb_pressure_plate import Tomb_Pressure_Plate
from scripts.entities.traps.traps.ancient_tomb.soul_trap import Soul_Trap
from scripts.entities.traps.traps.ancient_tomb.bell_pressure_plate import Bell_Pressure_plate
from scripts.entities.traps.traps.ancient_tomb.arrow_trap import Arrow_Trap
from scripts.entities.traps.traps.crystal_caverns.unstable_crystal import Unstable_Crystal


@pytest.fixture(scope="session", autouse=True)
def headless_pygame_context():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
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
    game.assets = MagicMock()
    game.sound_handler = MagicMock()
    game.decoration_handler = MagicMock()
    game.item_handler = MagicMock()
    game.trap_handler = MagicMock()
    game.clatter = MagicMock()
    
    # Mock player entity with explicit attributes
    player = MagicMock()
    player.type = keys.player
    player.category = keys.creature
    player.pos = [100.0, 100.0]
    player.dashing = False
    player.rect.return_value = pygame.Rect(100, 100, 32, 32)
    game.player = player

    # Tilemap mocking
    game.tilemap = MagicMock()
    game.tilemap.tile_size = 32
    mock_tile = MagicMock()
    mock_tile.pos = (0, 0)
    mock_tile.scaled_pos = (0, 0)
    mock_tile.contains_decoration = False
    mock_tile.physics = False
    mock_tile.room = False
    
    game.tilemap.Current_Tile.return_value = mock_tile
    game.tilemap.Get_Tile_From_Pos.return_value = mock_tile
    game.tilemap.tilemap = {(x, y): mock_tile for x in range(-10, 10) for y in range(-10, 10)}

    return game


@pytest.fixture
def mock_entity():
    def _create_entity(entity_id=1, entity_type=keys.player, category=keys.creature):
        entity = MagicMock()
        entity.ID = entity_id
        entity.type = entity_type
        entity.category = category
        entity.touching_ground = True
        entity.pos = [100.0, 100.0]
        entity.dashing = False
        entity.rect.return_value = pygame.Rect(100, 100, 32, 32)
        return entity
    return _create_entity


class TestSpikeTraps:
    def test_standard_spike_applies_damage_and_slow(self, mock_game, mock_entity):
        spike = Spike(mock_game, (0, 0))
        target = mock_entity(entity_id=10)
        
        spike.Apply_Entity_Effect(target)
        target.Damage_Taken.assert_called_once_with(2, (keys.slow, 1))

    def test_poison_spike_applies_poison_effect(self, mock_game, mock_entity):
        poison_spike = Spike_Poisoned(mock_game, (0, 0))
        target = mock_entity(entity_id=10)
        
        poison_spike.Apply_Entity_Effect(target)
        assert target.Damage_Taken.called
        args, _ = target.Damage_Taken.call_args
        assert args[0] == 2
        assert args[1][0] == keys.poison
        assert 3 <= args[1][1] <= 5

    def test_spike_pit_initial_snare_and_subsequent_slow(self, mock_game, mock_entity):
        pit = Spike_Pit(mock_game, (0, 0))
        target = mock_entity(entity_id=10)

        pit.Apply_Entity_Effect(target)
        target.Damage_Taken.assert_called_with(10, (keys.snare, 2))

        pit.Apply_Entity_Effect(target)
        target.Damage_Taken.assert_called_with(5, (keys.slow, 1))


class TestSpiderWeb:
    def test_ignores_items_and_creator(self, mock_game, mock_entity):
        creator = mock_entity(entity_id=1)
        item = mock_entity(entity_id=2, category=keys.item)
        web = Spider_Web(mock_game, (0, 0), entity=creator)

        web.entity_hit(item)
        assert not web.delete

        web.entity_hit(creator)
        assert not web.delete

    def test_applies_snare_and_flags_deletion_on_hit(self, mock_game, mock_entity):
        player = mock_entity(entity_id=2, entity_type=keys.player, category=keys.creature)
        web = Spider_Web(mock_game, (0, 0))

        web.entity_hit(player)
        assert (player.Set_Effect.called or player.Apply_Effect.called)
        assert web.delete is True

    def test_player_dashing_bypasses_web(self, mock_game, mock_entity):
        player = mock_entity(entity_id=2, entity_type=keys.player, category=keys.creature)
        player.dashing = True
        web = Spider_Web(mock_game, (0, 0))

        web.entity_hit(player)
        player.Set_Effect.assert_not_called()
        player.Apply_Effect.assert_not_called()
        assert web.delete is False


class TestAudioAndTriggerTraps:
    def test_rubble_triggers_clatter_and_sound(self, mock_game, mock_entity):
        rubble = Rubble(mock_game, (10, 10))
        # Clear sound calls triggered during Rubble.__init__
        mock_game.sound_handler.Play_Sound.reset_mock()
        
        player = mock_entity(entity_type=keys.player)
        rubble.Apply_Entity_Effect(player)
        
        mock_game.sound_handler.Play_Sound.assert_called_once_with(keys.rubble, 0.4)
        mock_game.clatter.Generate_Clatter.assert_called_once_with((10, 10), 500)

    def test_bell_pressure_plate_generates_sound(self, mock_game, mock_entity):
        bell = Bell_Pressure_plate(mock_game, (0, 0))
        bell.Generate_Sound = MagicMock()
        player = mock_entity(entity_type=keys.player)

        bell.Apply_Entity_Effect(player)
        bell.Generate_Sound.assert_called_once_with(keys.bell, 0.3, 1000)


class TestTombPressurePlate:
    def test_tomb_spawning_and_activation(self, mock_game, mock_entity):
        mock_tomb = MagicMock()
        mock_game.decoration_handler.Decoration_Spawner.return_value = mock_tomb

        plate = Tomb_Pressure_Plate(mock_game, (320, 320))
        plate.linked_tombs = []
        
        player = mock_entity(entity_type=keys.player)
        plate.Apply_Entity_Effect(player)

        assert plate.activated is True

    def test_already_activated_plate_ignores_retrigger(self, mock_game, mock_entity):
        plate = Tomb_Pressure_Plate(mock_game, (0, 0))
        plate.activated = True
        player = mock_entity(entity_type=keys.player)

        plate.Apply_Entity_Effect(player)
        mock_game.sound_handler.Play_Sound.assert_not_called()


class TestSoulTrap:
    def test_drains_soul_and_spawns_shard(self, mock_game, mock_entity):
        trap = Soul_Trap(mock_game, (0, 0))
        trap.tile = MagicMock(pos=(5, 5))
        
        target_tile = MagicMock()
        random_tile = MagicMock(scaled_pos=(160, 192))
        
        mock_game.tilemap.Current_Tile.return_value = target_tile
        mock_game.tilemap.Get_Random_Tile_With_Path_Tile.return_value = random_tile
        player = mock_entity(entity_type=keys.player)

        success = trap.Apply_Entity_Effect(player)

        assert success is True
        mock_game.item_handler.Spawn_Item_By_Type.assert_called_once_with(
            keys.valuable, (160, 192), type=keys.soul_shard
        )


# class TestArrowTrap:
#     def test_arrow_pool_initialization(self, mock_game):
#         mock_arrow = MagicMock()
#         mock_game.item_handler.Spawn_Arrow_For_Trap.return_value = mock_arrow

#         trap = Arrow_Trap(mock_game, (0, 0))

#         assert len(trap.arrows) == 3
#         assert trap.next_available_arrow == 0

#     def test_shoot_arrow_cycles_through_pool(self, mock_game):
#         arrows = [MagicMock(), MagicMock(), MagicMock()]
#         mock_game.item_handler.Spawn_Arrow_For_Trap.side_effect = arrows

#         trap = Arrow_Trap(mock_game, (100, 100))
        
#         trap.Shoot_Arrow()
#         arrows[0].Shooting_Setup.assert_called_once()
#         assert trap.next_available_arrow == 1

#         trap.Shoot_Arrow()
#         trap.Shoot_Arrow()
#         assert trap.next_available_arrow == 0


class TestFireTrap:
    def test_fire_trap_applies_burn_during_active_animation_frames(self, mock_game, mock_entity):
        trap = Fire_Trap(mock_game, (0, 0))
        trap.Cooldown = 0
        trap.active = True
        
        target = mock_entity(entity_type=keys.player)
        target.Get_Effect_Strength.return_value = False
        
        trap.Update(target)
        assert target.Set_Effect.called or target.Apply_Effect.called or target.Damage_Taken.called

    def test_fire_trap_ignores_target_during_inactive_animation_frames(self, mock_game, mock_entity):
        trap = Fire_Trap(mock_game, (0, 0))
        trap.Cooldown = 100
        trap.active = False
        
        target = mock_entity(entity_type=keys.player)
        trap.Update(target)
        
        target.Set_Effect.assert_not_called()

    def test_fire_trap_bypasses_invulnerable_entities(self, mock_game, mock_entity):
        trap = Fire_Trap(mock_game, (0, 0))
        trap.Cooldown = 0
        trap.active = True
        
        target = mock_entity(entity_type=keys.player)
        target.Get_Effect_Strength.return_value = True
        
        trap.Update(target)
        target.Set_Effect.assert_not_called()


class TestUnstableCrystal:
    @pytest.fixture
    def crystal_instance(self, mock_game):
        crystal = Unstable_Crystal(mock_game, (100, 100))
        if not hasattr(crystal, 'trigger_radius'):
            crystal.trigger_radius = 32
        return crystal

    def test_trigger_rect_dimensions(self, mock_game, crystal_instance):
        rect = crystal_instance.rect()
        assert isinstance(rect, pygame.Rect)

    def test_detonates_and_spawns_explosion_on_player_proximity(self, mock_game, mock_entity, crystal_instance):
        crystal_instance.Generate_Sound = MagicMock()
        
        player = mock_entity(entity_type=keys.player)
        crystal_instance.Apply_Entity_Effect(player)
        
        assert crystal_instance.Generate_Sound.called or mock_game.sound_handler.Play_Sound.called
        assert mock_game.item_handler.Add_Item.called or mock_game.trap_handler.Remove_Trap.called

    def test_ignores_non_player_entities(self, mock_game, mock_entity, crystal_instance):
        crystal_instance.Generate_Sound = MagicMock()
        
        enemy = mock_entity(entity_type='goblin', category='enemy')
        crystal_instance.Apply_Entity_Effect(enemy)
        
        crystal_instance.Generate_Sound.assert_not_called()
        mock_game.item_handler.Add_Item.assert_not_called()
        mock_game.trap_handler.Remove_Trap.assert_not_called()


# ---------------------------------------------------------------------------
# Force registry decorators to run before any test resolves a registry key.
# ---------------------------------------------------------------------------
from scripts.entities.traps.trap_spawner import Trap_Spawner
from scripts.entities.traps.trap_handler import Trap_Handler
from scripts.entities.traps.traps.shared import shared_registry as trap_registry
from scripts.entities.traps.traps.ancient_tomb import ancient_tomb_registry as ancient_tomb_trap_registry
from scripts.entities.traps.traps.crystal_caverns import crystal_cavern_registry as crystal_cavern_trap_registry



class TestTrapRegistry:
    def test_shared_trap_registry_is_populated(self):
        """Fails if a shared trap module wasn't imported (decorator never ran)."""
        expected_keys = [
            keys.pit_trap, keys.spike_poison_trap, keys.spike_trap,
            keys.rubble, keys.arrow_trap,
        ]
        for key in expected_keys:
            assert key in trap_registry.TRAP_REGISTRY, (
                f"'{key}' missing from TRAP_REGISTRY — check load_all.py imports it."
            )

    def test_ancient_tomb_trap_registry_is_populated(self):
        expected_keys = [keys.tomb_pressure_plate, keys.bell_pressure_plate, keys.soul_trap]
        for key in expected_keys:
            assert key in ancient_tomb_trap_registry.TRAP_REGISTRY, (
                f"'{key}' missing from ancient tomb TRAP_REGISTRY."
            )

    def test_weighted_and_lookup_only_traps_are_distinguished(self):
        """Env traps (lava/water/ice) are lookup-only — never rolled by weight."""
        assert keys.lava_env in trap_registry.TRAP_REGISTRY
        assert keys.lava_env not in trap_registry.TRAP_TABLE


class TestTrapSpawnerDungeonMerge:
    def test_ancient_crypt_merges_shared_and_dungeon_specific(self, mock_game):
        mock_game.dungeon_type = keys.ancient_crypt
        spawner = Trap_Spawner(mock_game)

        # shared traps present
        assert keys.spike_trap in spawner.trap_classes
        # dungeon-specific traps present
        assert keys.soul_trap in spawner.trap_classes
        assert keys.soul_trap in spawner.TRAP_TABLE

    def test_unknown_dungeon_type_raises(self, mock_game):
        mock_game.dungeon_type = "not_a_real_dungeon"
        with pytest.raises(ValueError):
            Trap_Spawner(mock_game)


class TestTrapHandlerSpawning:
    def test_initialise_builds_plain_trap_spawner(self, mock_game):
        mock_game.dungeon_type = keys.ancient_crypt
        handler = Trap_Handler(mock_game)
        handler.Initialise()

        assert isinstance(handler.trap_spawner, Trap_Spawner)

    def test_load_data_adds_trap_to_handlers_own_list(self, mock_game):
        """Regression test: loaded traps must land in Trap_Handler.traps,
        not just Trap_Spawner.traps, or they never update/render."""
        mock_game.dungeon_type = keys.ancient_crypt
        handler = Trap_Handler(mock_game)

        saved_data = {
            "1": {keys.type: keys.spike_trap, keys.pos: (64, 64)}
        }
        handler.Load_Data(saved_data)

        assert len(handler.traps) == 1
        assert handler.traps[0].type == keys.spike_trap