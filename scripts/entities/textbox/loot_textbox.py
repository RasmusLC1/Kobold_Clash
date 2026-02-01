from scripts.entities.textbox.textbox import Text_Box
from scripts.engine.keys.keys import keys

class Loot_Textbox(Text_Box):
    def __init__(self, entity):
        super().__init__(entity)

   
    def Edit_Entity_Name(self):
        entity_name = self.entity.sub_type
        entity_name = entity_name.replace('_resistance', ' res')
        return entity_name
    
    def Render_Headline(self, surf, entity_name, text_box_pos):
        item_rarity = self.entity.rarity
        fonts = {
            keys.common : keys.font_commmon,
            keys.uncommon : keys.font_uncommon,
            keys.rare : keys.font_rare,
            keys.epic : keys.font_epic,
            keys.legendary : keys.font_legendary,
        }

        rarity_font = fonts.get(item_rarity, None)

        if not rarity_font:
            print("FAILED TO FIND RARITY FONT", item_rarity, self.entity.type)
            return
        

        self.headline_font.Render_Word(surf, entity_name, text_box_pos, rarity_font)

