from scripts.entities.textbox.textbox import Text_Box
import re
from scripts.engine.keys.keys import keys

class Enemy_Textbox(Text_Box):

    def Edit_Entity_Name(self):
        entity_name = self.entity.type
        entity_name = entity_name.replace('skeleton_', '')
         # Remove _ followed by an integer
        entity_name = re.sub(r'_\d+', '', entity_name)
        return entity_name
    
    def Set_Text_Box_pos(self, offset):
        text_box_pos = (0,0)
        text_box_pos = (self.entity.pos[0] - offset[0], self.entity.pos[1] - offset[1] - self.y_size)
        return text_box_pos
    

    # Seperate function for size flexibility
    def Set_Y_Size(self):
        self.y_size = 60

