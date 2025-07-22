from scripts.entities.moving_entities.moving_entity_functions.damage_text import Damage_Text
class Damage_Text_Handler():
    def __init__(self, game):
        self.game = game
        self.damage_text_pool = []
        self.active_damage_texts = []
        self.index = 0

    def Update(self, delta_time):

        for damage_text in self.active_damage_texts:
            if not damage_text.Update(delta_time):
                self.active_damage_texts.remove(damage_text)

            
    def Spawn_Damage_Text(self, pos, effect, text):
        damage_text = self.Find_Damage_Text()

        if not damage_text:
            damage_text = self.Create_Extra_Damage_Text()

        queue_length = len(self.active_damage_texts)
        damage_text.Activate(pos, effect, text, queue_length)
        self.active_damage_texts.append(damage_text)


    # Append extra damage_text to the pool in case it runs out
    def Create_Extra_Damage_Text(self):

        damage_text = Damage_Text()
        self.damage_text_pool.append(damage_text)
        return damage_text


    # Search for particles with an index
    def Find_Damage_Text(self):
        # If there are no particles in the pool return None to spawn particle
        if not self.damage_text_pool:
            return None
        
        # Check if the initial index is available, in which case loop the index back to 0
        if self.damage_text_pool[0].cooldown <= 0:
            self.index = 0
        
        # Overflow prevent
        if self.index >= len(self.damage_text_pool) - 1:
            return None

        # Set the fire particle to be the next available index
        damage_text = self.damage_text_pool[self.index]
        self.index += 1

        # If there are no free fire particle return None to spawn a new one
        if damage_text.cooldown <= 0:
            return None
        
        return damage_text

    def Render(self, surf, offset):
        for damage_text in self.active_damage_texts:
            if not damage_text.text:
                self.active_damage_texts.remove(damage_text)
                continue
            scroll_up_effect = damage_text.offset - damage_text.cooldown * 10
            self.game.default_font.Render_Word(surf, damage_text.text, (damage_text.pos[0] - offset[0], damage_text.pos[1] - scroll_up_effect - offset[1]), damage_text.font_style)
            