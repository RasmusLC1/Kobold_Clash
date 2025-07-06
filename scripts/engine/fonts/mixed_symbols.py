import re
from scripts.engine.keys.keys import keys

class Mixed_Symbols():
    def __init__(self, game, symbols, font):
        self.game = game
        self.font = font
        self.symbols = symbols

    def parse_mixed_elements(self, input_str):
        # Split by spaces, newlines, and symbols, but capture everything
        parts = re.split(r'(\s+|\n|[^\w\s])', input_str)
        elements = []
        current_text = ''

        for part in parts:
            if not part:
                continue
            
            if part == '\n':  # Handle newline separately
                if current_text:
                    elements.append({keys.type: 'text', 'content': current_text})
                    current_text = ''
                elements.append({keys.type: 'newline', 'content': part})
            elif part.isspace():  # Handle spaces by appending to current_text
                current_text += part
            elif self.symbols.Check_If_Symbol_Exist(part.lower()):  # Check for symbols
                if current_text:
                    elements.append({keys.type: 'text', 'content': current_text})
                    current_text = ''
                elements.append({keys.type: 'symbol', 'content': part})
            else:  # Otherwise, it's regular text
                current_text += part

        if current_text:
            elements.append({keys.type: 'text', 'content': current_text})

        return elements

    def Get_Font_Size(self, scale):
        font_size = keys.font
        if scale == 1:
            font_size = keys.font # Set font size 
        elif scale < 1:
            font_size = keys.font_small
        # elif scale > 1:
        #     font_size = "large"
        return font_size
        

    # 2 is default size
    def Render_Mixed_Text(self, surf, input_str, pos, scale=1, font_style = None):
        if not font_style:
            font_style = self.Get_Font_Size(scale)
        elements = self.parse_mixed_elements(input_str)
        current_x, current_y = pos
        for element in elements:
            if element[keys.type] == 'text':
                self.font.Render_Word(surf, element['content'], (current_x, current_y), font_style)
                # Update x position based on number of characters (14 pixels per character)
                current_x += 14 * len(element['content']) * scale
            elif element[keys.type] == 'symbol':
                # Render the symbol and update x position
                self.symbols.Render_Symbol(surf, element['content'], (current_x, current_y), scale)
                current_x += 16 * scale  # Assuming each symbol is 16 pixels wide, scaled
            elif element[keys.type] == 'newline':  # Handle newlines properly
                current_y += 16 * scale  # Adjust line height for the next line of text
                current_x = pos[0]  # Reset x position for the new line
