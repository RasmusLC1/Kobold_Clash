from scripts.engine.keys.keys import keys
import inspect

class Font():
    def __init__(self, game):
        self.game = game
        self.font = self.game.assets[keys.font]
        self.player_damage_font = self.game.assets[keys.player_damage_font]
        self.font_small = self.game.assets[keys.font_small]

        # Use dictionary for O(1) lookup time, using enumerate to number them
        self.font_lookup_table = {
            **{char: index for index, char in enumerate(
                [*map(chr, range(97, 123)),  # a-z
                *map(str, range(10)),       # 0-9
                '-', '+', ':', '!', '_', '/', ' ', '\n']
            )}
        }


    def find_char_positions(self, input_string):
        input_string = input_string.lower()  

        # Use list comprehension for optimisation and check that the char is in the dictionary
        char_positions = [
            self.font_lookup_table[char] if char in self.font_lookup_table else None
            for char in input_string
        ]
        
        return char_positions


    # Finds the specific font style and loads it in
    def Find_Font(self, font_style):
        try:
            return self.game.assets[font_style]
        except Exception as e:
            print(f'WRONG FONT STYLE {e}', font_style)

    def Find_Font_Size(self, font_style):
        font_size = (15, 16)
        if "small" in font_style.lower():
            font_size = (7, 8)
        elif "large" in font_style.lower():
            font_size = (30, 32)
        elif "headline" in font_style.lower():
            font_size = (11, 12)

        return font_size


    def Render_Word(self, surf, text, pos, font_style=None):
        if not font_style:
            font_style = keys.font
        
        font = self.Find_Font(font_style)
        if not font: return
        
        size = self.Find_Font_Size(font_style)
        char_w, char_h = size
        
        origin_x, current_y = pos
        lines = text.split('\n')

        for line in lines:
            current_x = origin_x
            # Process every single character, including spaces
            char_positions = self.find_char_positions(line)
            
            for pos_index in char_positions:
                if pos_index is not None:
                    surf.blit(font[pos_index], (current_x, current_y))
                # ALWAYS increment x, even if char is None (like a space)
                current_x += char_w
            
            current_y += char_h

    # Handles words
    def Render_Chunk(self, surf, current_x, current_y, char_positions, x_increment, font):
        for font_position in char_positions:
            if font_position is None:
                continue  # Skip characters not found in font_lookup
            try:
                surf.blit(font[font_position], (current_x, current_y))
                current_x += x_increment  # Increment x position for next character
            except Exception as e:
                print(f"WRONG SYMBOL FONT: {e}", font)