import re
from scripts.engine.keys.keys import keys

class Mixed_Symbols():
    def __init__(self, game, symbols, font):
        self.game = game
        self.font = font
        self.symbols = symbols

        # Filter to ensure we only try to sort actual strings
        all_symbol_names = [
            str(name) for name in self.symbols.symbols_lookup.keys() 
            if name is not None
        ]
        
        # Sort by length descending
        all_symbol_names.sort(key=len, reverse=True)
        self.symbol_re = "|".join(map(re.escape, all_symbol_names))


    def parse_mixed_elements(self, input_str):
        # This regex splits by newlines OR any of your specific symbol words
        pattern = f"(\\n|{self.symbol_re})"
        parts = re.split(pattern, input_str, flags=re.IGNORECASE)
        
        elements = []
        for part in parts:
            if not part:
                continue
            
            if part == '\n':
                elements.append({keys.type: 'newline'})
            elif self.symbols.Check_If_Symbol_Exist(part.lower()):
                elements.append({keys.type: 'symbol', 'content': part.lower()})
            else:
                # This is regular text (including spaces)
                elements.append({keys.type: 'text', 'content': part})
        return elements
    
    def Get_Font_Size(self, scale):
        # Default to standard font
        font_key = keys.font 
        
        # Logic based on your specific key names
        if scale < 1:
            font_key = keys.font_small
        elif scale > 1:
            # If you have a keys.font_large, use it here
            font_key = keys.font 
            
        return font_key

    def Render_Mixed_Text(self, surf, input_str, pos, scale=1, font_style=None):
        if not font_style:
            font_style = self.Get_Font_Size(scale)
            
        elements = self.parse_mixed_elements(input_str)
        current_x, current_y = pos
        
        # Get dimensions from Font class
        char_w, char_h = self.font.Find_Font_Size(font_style)
        symbol_size = int(16 * scale)

        for element in elements:
            if element[keys.type] == 'text':
                content = element['content']
                self.font.Render_Word(surf, content, (current_x, current_y), font_style)
                current_x += len(content) * char_w
                
            elif element[keys.type] == 'symbol':
                self.symbols.Render_Symbol(surf, element['content'], (current_x, current_y), scale)
                current_x += symbol_size
                
            elif element[keys.type] == 'newline':
                current_y += char_h
                current_x = pos[0]