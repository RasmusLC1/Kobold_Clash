# tests/test_logic_update.py
from scripts.game.logic_update import Logic_Update

def test_freeze_frame_behavior(mock_game):
    # Setup our component with the mocked game object
    logic_update = Logic_Update(mock_game)
    
    # Check default state
    assert logic_update.freeze_frame == 0
    assert logic_update.Update_Freeze_Frame() is True
    
    # Set a freeze frame and check that it blocks updates
    logic_update.Set_Freeze_Frame(2)
    assert logic_update.freeze_frame == 2
    
    # First tick: Should return False (blocking game loop logic) and decrement
    assert logic_update.Update_Freeze_Frame() is False
    assert logic_update.freeze_frame == 1
    
    # Second tick: decrement again
    assert logic_update.Update_Freeze_Frame() is False
    assert logic_update.freeze_frame == 0
    
    # Third tick: unblocked
    assert logic_update.Update_Freeze_Frame() is True