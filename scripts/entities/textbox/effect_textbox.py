from scripts.entities.textbox.textbox import Text_Box
from scripts.engine.keys.keys import keys

class Effect_Textbox(Text_Box):

    def Edit_Entity_Name(self):
        entity_name = self.entity.effect.effect_type
        entity_name = entity_name.replace('_resistance', ' res')
        return entity_name

    def Set_Text_Box_pos(self, offset):
        return (self.entity.pos[0] + 50, self.entity.pos[1] - 10)

    def Render(self, surf, text_box_pos, offset = (0,0)):
   
        entity_name = self.Edit_Entity_Name()

        
        text_box_pos = self.Text_Box_Setup(surf, entity_name, offset)
        self.entity.game.mixed_symbols.Render_Mixed_Text(surf, self.entity.effect.description, text_box_pos, 0.5)



