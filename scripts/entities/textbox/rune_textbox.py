from scripts.entities.textbox.textbox import Text_Box
from scripts.engine.keys.keys import keys

class Rune_Textbox(Text_Box):

    def Edit_Entity_Name(self):
        entity_name = super().Edit_Entity_Name()
        entity_name = entity_name.replace('_rune', '')
        return entity_name

    def Set_Text_Box_pos(self, offset):
        text_box_pos = (self.entity.game.screen_width // self.entity.game.render_scale - self.x_size - 20, self.entity.pos[1] -  self.y_size - 20)
        return text_box_pos
