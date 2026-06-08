import re
from scripts.engine.keys.keys import keys

class Mixed_Symbols:
    def __init__(self, game, symbols, font):
        self.game = game
        self.font = font
        self.symbols = symbols
        self._build_regex_pattern()

    def _build_regex_pattern(self):
        """Compiles the matching regex pattern using keys directly from the registry."""
        # Pull sanitized string keys directly from your SymbolRegistry dictionary
        all_symbol_names = [str(name) for name in self.symbols._symbols.keys() if name is not None]
        # Sort descending by length to prevent partial word matches (e.g., 'fire' matching before 'fire_resistance')
        all_symbol_names.sort(key=len, reverse=True)
        
        # Matches newlines, spaces, or registered symbol keys
        symbol_re = "|".join(map(re.escape, all_symbol_names))
        self.token_pattern = re.compile(f"(\\n|\\s+|{symbol_re})", re.IGNORECASE)

    def parse_mixed_elements(self, input_str):
        """Splits the string into individual words, whitespace chunks, and symbol tags."""
        parts = self.token_pattern.split(input_str)
        elements = []
        
        for part in parts:
            if not part:
                continue
                
            if part == '\n':
                elements.append({'type': 'newline'})
            elif part.isspace():
                elements.append({'type': 'whitespace', 'content': part})
            elif self.symbols.exists(part):
                elements.append({'type': 'symbol', 'content': part.lower()})
            else:
                elements.append({'type': 'text', 'content': part})
                
        return elements
    
    def get_font_style(self, scale):
        """Resolves the appropriate asset font key based on rendering scale."""
        return keys.font_small if scale < 1 else keys.font

    def Render_Mixed_Text(self, surf, input_str, pos, max_width=200, scale=1, font_style=None):
        """Facilitator method that coordinates parsing, layout calculations, and drawing."""
        if not font_style:
            font_style = self.get_font_style(scale)
            
        char_w, char_h = self.font.Find_Font_Size(font_style)
        symbol_size = int(16 * scale)

        # 1. Parsing Phase
        elements = self.parse_mixed_elements(input_str)
        
        # 2. Layout Phase (Pure math/position generation)
        layout_plan = self._Calculate_Layout(elements, pos, max_width, char_w, char_h, symbol_size)
        
        # 3. Execution Phase (Pure Pygame rendering)
        self._Draw_Layout(surf, layout_plan, font_style, scale)

    # --- PRIVATE LAYOUT HELPERS ---

    def _Calculate_Layout(self, elements, start_pos, max_width, char_w, char_h, symbol_size):
        """Processes elements and assigns concrete (x, y) coordinates to renderable tokens."""
        start_x, start_y = start_pos
        current_x, current_y = start_x, start_y
        line_spacing = max(char_h, symbol_size) + 2
        
        layout_plan = []

        for element in elements:
            el_type = element['type']
            
            if el_type == 'newline':
                current_y += line_spacing
                current_x = start_x
                continue

            element_width = self._Get_Element_Width(element, char_w, symbol_size)

            # Check boundary conditions for automatic word wrapping
            if current_x + element_width > start_x + max_width:
                if el_type == 'whitespace' and current_x == start_x:
                    continue  # Ignore leading line indentation spaces
                current_y += line_spacing
                current_x = start_x

            # Capture positioned tokens for the draw pass
            layout_plan.append({
                'type': el_type,
                'content': element.get('content', ''),
                'pos': (current_x, current_y),
                'width': element_width
            })
            
            current_x += element_width

        return layout_plan

    def _Get_Element_Width(self, element, char_w, symbol_size):
        """Calculates the precise width of an element based on its structural type."""
        el_type = element['type']
        if el_type in ('text', 'whitespace'):
            return len(element['content']) * char_w
        if el_type == 'symbol':
            return symbol_size
        return 0

    # --- PRIVATE DRAWING HELPERS ---

    def _Draw_Layout(self, surf, layout_plan, font_style, scale):
        """Iterates over a pre-calculated layout list and executes surface blits."""
        for token in layout_plan:
            self._Draw_Token(surf, token, font_style, scale)

    def _Draw_Token(self, surf, token, font_style, scale):
        """Draws a single layout token based on its specific rendering instructions."""
        el_type = token['type']
        pos = token['pos']
        content = token['content']

        if el_type == 'text':
            self.font.Render_Word(surf, content, pos, font_style)
        elif el_type == 'symbol':
            self.symbols.Render_Symbol_By_Key(surf, content, pos, scale)
        # Note: 'whitespace' and 'newline' don't blit anything, so they safely pass through