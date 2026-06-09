import pygame
from scripts.engine.keys.keys import keys

class Font:
    def __init__(self, game):
        self.game = game
        
        # Define a clean string mapping characters to sprite indices sequentially
        # This matches the order of your character sprite strip
        chars_order = "abcdefghijklmnopqrstuvwxyz0123456789-+:!_/... "
        self.font_lookup_table = {char: idx for idx, char in enumerate(chars_order)}

    def _Find_Char_Positions(self, input_string):
        """Maps letters to sprite indices. Unknown characters resolve safely to None."""
        lookup = self.font_lookup_table
        return [lookup[char] for char in input_string.lower() if char in lookup]

    # Safely fetches the requested font sprite array from assets
    def _Find_Font(self, font_style):
        font_style = font_style or keys.font
        font_assets = self.game.assets.get(font_style)
        if not font_assets:
            print(f"Warning: Font style asset '{font_style}' not found.")
        return font_assets

    # Returns the dimensions (width, height) of a single character slot
    def Find_Font_Size(self, font_style):
        style_lower = font_style.lower() if font_style else ""
        if "small" in style_lower:
            return (7, 8)
        if "large" in style_lower:
            return (30, 32)
        if "headline" in style_lower:
            return (11, 12)
            
        return (15, 16) # Fallback standard size

    # Draws a clean row of text characters at a fixed target coordinate
    def Render_Word(self, surf, text, pos, font_style=None):
        font = self._Find_Font(font_style)
        if not font:
            print("FONT NOT FOUND", font_style)
            return
            
        char_w, _ = self.Find_Font_Size(font_style)
        current_x, current_y = pos

        # Process characters directly without splitting internal strings
        char_indices = self._Find_Char_Positions(text)
        
        for idx in char_indices:
            # Drop character to screen if mapped safely
            surf.blit(font[idx], (current_x, current_y))
            # Always advance cursor position horizontally, maintaining monospace grid alignment
            current_x += char_w