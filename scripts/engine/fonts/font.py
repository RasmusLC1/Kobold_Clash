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
        # Initalise to default font if none found
        if not font_style:
            font_style = keys.font
        original_x, original_y = pos
        current_y = original_y
        font = self.Find_Font(font_style)
        if not font:
            caller_frame = inspect.stack()[1]
            caller_name = caller_frame.function
            print("RENDER WORD FAILED ", font_style, caller_name)
            return
        size = self.Find_Font_Size(font_style)

        # Split by newline and then process each line
        lines = text.split('\n')

        for line in lines:
            words = line.split()  # Split the line into words
            chunks = [words[i:i+2] for i in range(0, len(words), 2)]  # Group words into chunks
            current_x = original_x  # Reset x for each line

            for chunk in chunks:
                line_text = ' '.join(chunk)
                char_positions = self.find_char_positions(line_text)
                self.Render_Chunk(surf, current_x, current_y, char_positions, size[0], font)
                current_x += len(line_text) * size[0]  # Adjust spacing if needed

            current_y += size[1]  # Move to the next line

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