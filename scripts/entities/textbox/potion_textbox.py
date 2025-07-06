from scripts.entities.textbox.textbox import Text_Box
from scripts.engine.keys.keys import keys



class Potion_Textbox(Text_Box):

    def Edit_Entity_Name(self):
        entity_name = super().Edit_Entity_Name()
        entity_name = entity_name.replace('_potion', '')
        return entity_name

