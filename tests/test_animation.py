import pytest
import random
from unittest.mock import MagicMock

from scripts.entities.entity.animation_handlers.base_animation_handler import Base_Animation_Handler
from scripts.entities.entity.animation_handlers.fire_animation_handler import Fire_Animation_Handler
from scripts.entities.moving_entities.animation.animation_handler import Animation_Handler
from scripts.engine.keys.keys import keys


@pytest.fixture
def mock_entity():
    entity = MagicMock()
    entity.type = "kobold"
    entity.render = True
    entity.game.assets = {"kobold_running": ["frame0", "frame1", "frame2", "frame3"]}
    entity.distance_to_target = 0
    entity.charge = 0
    entity.frame_movement = False
    entity.attack_direction = (1, 0)
    return entity



@pytest.fixture
def base_handler(mock_entity):
    return Base_Animation_Handler(mock_entity, animation_max=3, animation_cooldown_max=1.5)


class FakeSurface:
    def convert_alpha(self):
        return self


@pytest.fixture
def mock_entity():
    entity = MagicMock()
    entity.type = "kobold"
    entity.render = True
    frames = [FakeSurface() for _ in range(4)]
    entity.game.assets = {"kobold_running": frames}
    entity.distance_to_target = 0
    entity.charge = 0
    entity.frame_movement = False
    entity.attack_direction = (1, 0)
    entity._frames = frames  # stash for assertions
    return entity

# --- 1. Construction & Random Initial Frame ---

def test_init_sets_cooldown_and_max_from_args(mock_entity):
    handler = Base_Animation_Handler(mock_entity, animation_max=3, animation_cooldown_max=1.5)

    assert handler.animation_max == 3
    assert handler.animation_cooldown_max == 1.5
    assert handler.animation_cooldown == 0.0


def test_random_initial_animation_within_bounds(mock_entity):
    random.seed(0)
    handler = Base_Animation_Handler(mock_entity, animation_max=3, animation_cooldown_max=1.5)

    assert 0 <= handler.animation <= 3


def test_random_initial_animation_zero_when_max_is_zero(mock_entity):
    handler = Base_Animation_Handler(mock_entity, animation_max=0, animation_cooldown_max=1.5)

    assert handler.animation == 0


# --- 2. Sprite / Frame Assignment ---

def test_set_sprite_success_sets_entity_image(base_handler, mock_entity):
    base_handler.animation = 0
    result = base_handler.Set_Sprite("kobold_running")

    assert result is True
    assert mock_entity.entity_image is mock_entity._frames[0]
    assert mock_entity.render_needs_update is True


def test_set_sprite_missing_key_fails_gracefully(base_handler, mock_entity):
    result = base_handler.Set_Sprite("does_not_exist")

    assert result is False
    assert base_handler.sprite is None


def test_set_frame_clamps_to_animation_max(base_handler, mock_entity):
    base_handler.Set_Frame(999)
    assert base_handler.animation == base_handler.animation_max

    base_handler.Set_Frame(-5)
    assert base_handler.animation == 0


def test_increase_frame_wraps_to_min_animation(base_handler):
    base_handler.min_animation = 0
    base_handler.animation = base_handler.animation_max

    base_handler.Increase_Frame()

    assert base_handler.animation == 0


# --- 3. Update_Animation cooldown gating (the actual bug you hit) ---

def test_update_animation_does_nothing_when_entity_not_rendering(base_handler, mock_entity):
    mock_entity.render = False
    base_handler.animation_cooldown = 0

    result = base_handler.Update_Animation(movement=(0, 0), delta_time=0.5)

    assert result is False


def test_update_animation_returns_false_and_stuck_when_cooldown_max_is_zero(mock_entity):
    """
    Regression test: if animation_cooldown_max is never set (e.g. a subclass
    forgets to forward it through its constructor chain), Update_Animation
    must refuse to advance frames rather than advancing every single call.
    """
    handler = Base_Animation_Handler(mock_entity, animation_max=3, animation_cooldown_max=0)
    starting_frame = handler.animation

    for _ in range(10):
        result = handler.Update_Animation(movement=(0, 0), delta_time=0.016)
        assert result is False

    assert handler.animation == starting_frame


def test_update_animation_waits_for_full_cooldown_before_advancing(base_handler):
    base_handler.animation = 0
    base_handler.animation_cooldown = base_handler.animation_cooldown_max  # just advanced, cooldown freshly reset

    result = base_handler.Update_Animation(movement=(0, 0), delta_time=0.016)

    assert result is False
    assert base_handler.animation == 0
    assert base_handler.animation_cooldown == pytest.approx(1.5 - 0.016)


def test_update_animation_advances_once_cooldown_fully_elapsed(base_handler):
    base_handler.animation = 0
    base_handler.animation_cooldown = -0.01  # already elapsed by the time this call happens

    result = base_handler.Update_Animation(movement=(0, 0), delta_time=0.5)

    assert result is True
    assert base_handler.animation == 1
    assert base_handler.animation_cooldown == pytest.approx(1.5)


def test_update_animation_does_not_advance_faster_than_cooldown_over_many_ticks():
    """
    Simulates ~1 second of 60fps ticks against a 1.5s cooldown handler and
    confirms the frame never advances (since 1s < 1.5s cooldown).
    """
    entity = MagicMock()
    entity.render = True
    handler = Base_Animation_Handler(entity, animation_max=3, animation_cooldown_max=1.5)
    handler.animation = 0
    handler.animation_cooldown = 1.5  # start at full cooldown, like right after a real frame advance

    delta_time = 1 / 60
    for _ in range(60):  # ~1 real second
        handler.Update_Animation(movement=(0, 0), delta_time=delta_time)

    assert handler.animation == 0


# --- 4. Save / Load ---

def test_save_and_load_round_trip(base_handler):
    base_handler.animation = 2
    base_handler.animation_cooldown = 0.75

    data = base_handler.Save_Data()

    base_handler.animation = 0
    base_handler.animation_cooldown = 0

    base_handler.Load_Data(data)

    assert base_handler.animation == 2
    assert base_handler.animation_cooldown == 0.75


# --- 5. Fire_Animation_Handler: randomized frame selection ---

def test_fire_handler_increase_frame_stays_within_bounds(mock_entity):
    handler = Fire_Animation_Handler(mock_entity, animation_max=3, animation_cooldown_max=1.5)

    for _ in range(50):
        handler.Increase_Frame()
        assert 0 <= handler.animation <= 3


def test_fire_handler_increase_frame_never_zero(mock_entity):
    """Fire_Animation_Handler.Increase_Frame uses randint(1, animation_max),
    so it should never land back on frame 0 the way the base wrap-around does."""
    handler = Fire_Animation_Handler(mock_entity, animation_max=3, animation_cooldown_max=1.5)

    seen = set()
    for _ in range(50):
        handler.Increase_Frame()
        seen.add(handler.animation)

    assert 0 not in seen


# --- 6. Animation_Handler: per-type dict, action selection, locking ---

@pytest.fixture
def mock_moving_entity():
    entity = MagicMock()
    entity.type = "kobold"
    entity.render = True
    entity.distance_to_target = 0
    entity.charge = 0
    entity.frame_movement = False
    entity.game.assets = {
        "kobold_idle": ["idle0", "idle1"],
        "kobold_running": ["run0", "run1"],
        "kobold_attack": ["atk0", "atk1"],
    }
    return entity


@pytest.fixture
def animation_handler(mock_moving_entity):
    return Animation_Handler(mock_moving_entity, animation_max=0, animation_cooldown_max=0)


def test_set_animation_num_max_syncs_global_animation_max(animation_handler):
    animation_handler.Set_Animation_Num_Max(keys.run, 5)

    assert animation_handler.animations[keys.run][keys.num_max] == 5
    assert animation_handler.animation_max >= 5


def test_set_action_picks_attack_when_charging(animation_handler, mock_moving_entity):
    mock_moving_entity.charge = 1
    animation_handler.action = ""  # force a change

    animation_handler.Set_Action()

    assert animation_handler.action == keys.attack


def test_set_action_picks_running_when_moving(animation_handler, mock_moving_entity):
    mock_moving_entity.charge = 0
    mock_moving_entity.frame_movement = True

    animation_handler.Set_Action()

    assert animation_handler.action == "running"


def test_set_action_picks_idle_by_default(animation_handler, mock_moving_entity):
    mock_moving_entity.charge = 0
    mock_moving_entity.frame_movement = False

    animation_handler.Set_Action()

    assert animation_handler.action == keys.idle


def test_set_action_does_nothing_when_target_out_of_range(animation_handler, mock_moving_entity):
    mock_moving_entity.distance_to_target = 9999
    animation_handler.action = "previous_action"

    animation_handler.Set_Action()

    assert animation_handler.action == "previous_action"


def test_set_animation_respects_lock(animation_handler):
    animation_handler.animation_lock = True
    animation_handler.action = "idle"

    result = animation_handler.Set_Animation("running")

    assert result is False
    assert animation_handler.action == "idle"


def test_set_animation_changes_action_and_locks(animation_handler):
    animation_handler.animation_lock = False
    animation_handler.action = ""

    result = animation_handler.Set_Animation("running")

    assert result is True
    assert animation_handler.action == "running"
    assert animation_handler.animation_key == "kobold_running"
    assert animation_handler.animation_lock is True


def test_set_animation_no_op_when_action_unchanged(animation_handler):
    animation_handler.animation_lock = False
    animation_handler.Set_Animation("idle")
    animation_handler.animation = 5  # simulate progress made mid-animation

    result = animation_handler.Set_Animation("idle")

    assert result is False
    assert animation_handler.animation == 5  # not reset


def test_update_generic_animation_triggers_attack_on_matching_frame(animation_handler, mock_moving_entity):
    animation_handler.attack_frame = 1
    animation_handler.animations[keys.attack][keys.num_max] = 3
    animation_handler.animations[keys.attack][keys.cooldown] = 0
    animation_handler.animations[keys.attack][keys.num] = 0

    animation_handler.Update_Generic_Animation(keys.attack, delta_time=0.5)

    mock_moving_entity.Trigger_Attack.assert_called_once()


def test_update_generic_animation_unlocks_after_final_frame(animation_handler):
    animation_handler.animation_lock = True
    animation_handler.animations[keys.idle][keys.num_max] = 1
    animation_handler.animations[keys.idle][keys.cooldown] = 0
    animation_handler.animations[keys.idle][keys.num] = 1  # about to exceed num_max

    animation_handler.Update_Generic_Animation(keys.idle, delta_time=0.5)

    assert animation_handler.animation_lock is False
    assert animation_handler.animations[keys.idle][keys.num] == 0


def test_handle_animation_update_dispatches_to_matching_type(animation_handler):
    animation_handler.animation_key = "kobold_running"
    animation_handler.animations[keys.run][keys.cooldown] = 0
    animation_handler.animations[keys.run][keys.num_max] = 3

    animation_handler.Update_Generic_Animation = MagicMock()
    animation_handler.Handle_Animation_Update(delta_time=0.5)

    animation_handler.Update_Generic_Animation.assert_called_once_with(keys.run, 0.5)


def test_flip_entity_in_move_direction(animation_handler):
    animation_handler.Flip_Entity_In_Move_Direction((5, 0))
    assert animation_handler.flip[0] is True

    animation_handler.Flip_Entity_In_Move_Direction((-5, 0))
    assert animation_handler.flip[0] is False


def test_attack_direction_handler_flip(animation_handler, mock_moving_entity):
    mock_moving_entity.attack_direction = (-1, 0)
    animation_handler.Attack_Direction_Handler()
    assert animation_handler.flip[0] is False

    mock_moving_entity.attack_direction = (1, 0)
    animation_handler.Attack_Direction_Handler()
    assert animation_handler.flip[0] is True


def test_set_attack_animation_num_max_derives_frame_and_cooldown(animation_handler, mock_moving_entity):
    mock_moving_entity.max_weapon_charge = 1.0

    animation_handler.Set_Attack_Animation_Num_Max(4)

    assert animation_handler.animations[keys.attack][keys.num_max] == 4
    assert animation_handler.attack_frame == 3
    assert animation_handler.animations[keys.attack][keys.cooldown_max] == pytest.approx(0.25)

def test_update_animation_needs_extra_call_after_cooldown_reaches_zero(base_handler):
    """A delta_time that fully consumes the cooldown does not advance the
    frame in the same call — it takes one more call to actually fire.
    Cooldown_Handler clamps the decrement at 0 rather than going negative."""
    base_handler.animation = 0
    base_handler.animation_cooldown = 0.01

    first_result = base_handler.Update_Animation(movement=(0, 0), delta_time=0.5)
    assert first_result is False
    assert base_handler.animation == 0
    assert base_handler.animation_cooldown == 0  # clamped, not negative

    second_result = base_handler.Update_Animation(movement=(0, 0), delta_time=0.0)
    assert second_result is True
    assert base_handler.animation == 1