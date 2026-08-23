import pytest
from unittest.mock import MagicMock, patch
import pygame
from collections import deque

from scripts.entities.entity.entities import PhysicsEntity
from scripts.entities.decoration.decoration_handler import Decoration_Handler
from scripts.entities.decoration.decoration_spawner import Decoration_Spawner
from scripts.entities.decoration.shared.shrine.shrine_registry import SHRINE_REGISTRY
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
    game.player.pos = pygame.Vector2(0, 0)
    return game

def make_decoration(type_=keys.decoration, ID=0, pos=(0, 0), size=(32, 32)):
    """A lightweight stand-in for a real decoration entity."""
    deco = MagicMock()
    deco.type = type_
    deco.ID = ID
    deco.pos = pygame.Vector2(pos)
    deco.rect.return_value = pygame.Rect(pos, size)
    return deco


# =========================================================
# Decoration_Handler
# =========================================================

### 1. Lookup & Query

def test_get_random_decoration_of_type_filters_correctly(mock_game):
    handler = Decoration_Handler(mock_game)
    torch = make_decoration(type_=keys.torch, ID=1)
    door = make_decoration(type_="door", ID=2)
    handler.decorations = [torch, door]

    with patch("random.choice", side_effect=lambda lst: lst[0]):
        result = handler.Get_Random_Decoration_Of_Type([keys.torch])

    assert result == torch


def test_get_random_decoration_of_type_returns_none_when_empty(mock_game):
    handler = Decoration_Handler(mock_game)
    handler.decorations = [make_decoration(type_="door")]

    assert handler.Get_Random_Decoration_Of_Type([keys.torch]) is None


def test_get_decoration_by_id(mock_game):
    handler = Decoration_Handler(mock_game)
    target = make_decoration(ID=42)
    handler.decorations = [make_decoration(ID=1), target, make_decoration(ID=2)]

    assert handler.Get_Decoration_By_ID(42) is target
    assert handler.Get_Decoration_By_ID(999) is None


### 2. Add / Remove

def test_add_decoration_skips_duplicates(mock_game):
    handler = Decoration_Handler(mock_game)
    deco = make_decoration()
    handler.Add_Decoration(deco)
    handler.Add_Decoration(deco)

    assert handler.decorations.count(deco) == 1


def test_remove_decoration_cleans_up_fully(mock_game):
    handler = Decoration_Handler(mock_game)
    deco = make_decoration(ID=5)
    deco.tile = MagicMock()
    handler.decorations = [deco]

    handler.Remove_Decoration(deco)

    assert deco not in handler.decorations
    mock_game.item_handler.Remove_Item.assert_called_once_with(deco)
    mock_game.tilemap.Remove_Entity_From_Tile.assert_called_once_with(deco.tile, deco.ID)
    deco.Delete.assert_called_once()


def test_remove_decoration_noop_if_not_present(mock_game):
    handler = Decoration_Handler(mock_game)
    deco = make_decoration()
    handler.decorations = []

    handler.Remove_Decoration(deco)  # should not raise

    mock_game.item_handler.Remove_Item.assert_not_called()


### 3. Open_Decoration — distance sorting & bones filtering

def test_open_decoration_picks_nearest_non_bones(mock_game):
    handler = Decoration_Handler(mock_game)
    mock_game.player.pos = pygame.Vector2(0, 0)

    far = make_decoration(type_="chest", ID=1, pos=(100, 0))
    near = make_decoration(type_="chest", ID=2, pos=(10, 0))
    bones = make_decoration(type_=keys.bones, ID=3, pos=(1, 0))  # nearest, but must be skipped

    handler.Open_Decoration([far, near, bones])

    near.Open.assert_called_once()
    far.Open.assert_not_called()
    bones.Open.assert_not_called()


def test_open_decoration_all_bones_opens_nothing(mock_game):
    handler = Decoration_Handler(mock_game)
    bones = make_decoration(type_=keys.bones, ID=1, pos=(1, 0))

    result = handler.Open_Decoration([bones])

    bones.Open.assert_not_called()
    assert result is False


### 4. Item / Decoration collisions (shrine sacrifice flow)

def test_check_item_collision_triggers_spawn_reward(mock_game):
    handler = Decoration_Handler(mock_game)
    shrine = make_decoration(type_=keys.soul_well)
    shrine.rect.return_value = pygame.Rect(0, 0, 32, 32)
    handler.item_sacrifice = [shrine]

    item = MagicMock()
    item.rect.return_value = pygame.Rect(10, 10, 8, 8)  # overlaps shrine
    shrine.Spawn_Reward.return_value = True

    result = handler.Check_Item_Collision(item)

    shrine.Spawn_Reward.assert_called_once_with(item)
    assert result is True


def test_check_item_collision_no_overlap_returns_false(mock_game):
    handler = Decoration_Handler(mock_game)
    shrine = make_decoration(type_=keys.soul_well)
    shrine.rect.return_value = pygame.Rect(0, 0, 32, 32)
    handler.item_sacrifice = [shrine]

    item = MagicMock()
    item.rect.return_value = pygame.Rect(500, 500, 8, 8)  # far away

    result = handler.Check_Item_Collision(item)

    shrine.Spawn_Reward.assert_not_called()
    assert result is False


### 5. Decoration_Spawner (instance method on Decoration_Handler) & Load_Data

def test_decoration_spawner_method_spawns_and_loads(mock_game):
    handler = Decoration_Handler(mock_game)
    spawned = make_decoration(type_="chest")
    spawn_fn = MagicMock(return_value=spawned)
    handler.spawn_methods = {"chest": spawn_fn}

    data = {keys.type: "chest", keys.pos: (0, 0)}
    result = handler.Decoration_Spawner("chest", (0, 0), data=data)

    spawn_fn.assert_called_once_with(mock_game, (0, 0))
    spawned.Load_Data.assert_called_once_with(data)
    assert result is spawned
    assert spawned in handler.decorations


def test_decoration_spawner_method_warns_on_unknown_type(mock_game, capsys):
    handler = Decoration_Handler(mock_game)
    handler.spawn_methods = {}

    result = handler.Decoration_Spawner("nonexistent_type", (0, 0))

    assert result is None
    assert handler.decorations == []


# =========================================================
# Decoration_Spawner
# =========================================================

@pytest.fixture
def spawner(mock_game):
    return Decoration_Spawner(mock_game)


### 6. Get_Dungeon_Type — invalid input

def test_get_dungeon_type_raises_for_unknown_dungeon(spawner, mock_game):
    mock_game.dungeon_type = "not_a_real_dungeon_type"

    with pytest.raises(ValueError):
        spawner.Get_Dungeon_Type()


### 7. Generic_Spawn

def test_generic_spawn_instantiates_registered_types(spawner, mock_game):
    spawned = make_decoration(type_="barrel")
    spawn_cls = MagicMock(return_value=spawned)
    spawner.spawn_methods = {"barrel": spawn_cls}
    spawner.decoration_initialiser = MagicMock()
    spawner.decoration_initialiser.decorations = {"barrel": [(0, 0), (32, 32)]}

    spawner.Generic_Spawn(["barrel"])

    assert spawn_cls.call_count == 2
    assert spawned in spawner.decorations
    assert len(spawner.decorations) == 2


def test_generic_spawn_skips_unregistered_type(spawner):
    spawner.spawn_methods = {}
    spawner.decoration_initialiser = MagicMock()
    spawner.decoration_initialiser.decorations = {"unregistered": [(0, 0)]}

    spawner.Generic_Spawn(["unregistered"])

    assert spawner.decorations == []


### 8. Spawn_Lightsource — weighted choice, torch special-case

def test_spawn_lightsource_creates_registered_class(spawner, mock_game):
    spawned_light = make_decoration(type_="torch_deco")
    light_cls = MagicMock(return_value=spawned_light)
    spawner.decoration_initialiser = MagicMock()
    spawner.decoration_initialiser.decorations = {keys.light_source: [(0, 0)]}
    spawner.light_source_classes = {"crystal": light_cls}
    spawner.light_source_probability = {"crystal": 1.0}

    with patch("random.choices", return_value=["crystal"]):
        spawner.Spawn_Lightsource()

    light_cls.assert_called_once_with(mock_game, (0, 0))
    assert spawned_light in spawner.decorations


def test_spawn_lightsource_torch_spawns_weapon_not_decoration(spawner, mock_game):
    spawner.decoration_initialiser = MagicMock()
    spawner.decoration_initialiser.decorations = {keys.light_source: [(5, 5)]}
    spawner.light_source_classes = {}
    spawner.light_source_probability = {keys.torch: 1.0}

    with patch("random.choices", return_value=[keys.torch]):
        spawner.Spawn_Lightsource()

    mock_game.item_handler.weapon_handler.Weapon_Spawner.assert_called_once_with(keys.torch, 5, 5)
    assert spawner.decorations == []  # torch is a weapon pickup, not a decoration


def test_spawn_lightsource_warns_on_unregistered_type(spawner, capsys):
    spawner.decoration_initialiser = MagicMock()
    spawner.decoration_initialiser.decorations = {keys.light_source: [(0, 0)]}
    spawner.light_source_classes = {}
    spawner.light_source_probability = {"ghost_light": 1.0}

    with patch("random.choices", return_value=["ghost_light"]):
        spawner.Spawn_Lightsource()

    assert spawner.decorations == []


### 9. Link_Teleportation_Circles

def test_link_teleportation_circles_pairs_and_links(spawner):
    circle_a = make_decoration(type_=keys.teleportation_circle, ID=1)
    circle_b = make_decoration(type_=keys.teleportation_circle, ID=2)
    circle_a.linked_portal = None
    circle_b.linked_portal = None
    spawner.decorations = [circle_a, circle_b]

    with patch("random.shuffle", lambda lst: lst):  # deterministic order
        spawner.Link_Teleportation_Circles()

    circle_a.Set_Linked_Portal.assert_called_once_with(circle_b)
    circle_b.Set_Linked_Portal.assert_called_once_with(circle_a)


### 10. Set_Item_Sacrifice_Decorations — shrine registry integration

def test_set_item_sacrifice_decorations_uses_shrine_registry(spawner, monkeypatch):
    monkeypatch.setattr(
        "scripts.entities.decoration.decoration_spawner.SHRINE_REGISTRY",
        [keys.soul_well],
    )
    shrine = make_decoration(type_=keys.soul_well)
    chest = make_decoration(type_="chest")
    spawner.decorations = [shrine, chest]

    spawner.Set_Item_Sacrifice_Decorations()

    assert spawner.item_sacrifice == [shrine]


def test_soul_well_registers_itself_in_shrine_registry():
    """Import-time side effect: Register_Shrine(keys.soul_well) must have populated SHRINE_REGISTRY."""
    import scripts.entities.decoration.shared.shrine.shrine_types.soul_well  # noqa: F401 — triggers registration
    assert keys.soul_well in SHRINE_REGISTRY