from scripts.engine.keys.keys import keys
from scripts.engine.fonts.noise.noise import Noise

class Noise_Handler():
    def __init__(self, game):
        
        self.game = game
        self.index = 0
        self.active_noise_symbols = []
        self.noise_pool = []


    def Update(self):
        for noise_symbol in self.active_noise_symbols:
            if not noise_symbol.Update():
                self.Remove_Noise_Symbol_From_Active(noise_symbol)

    def Activate(self, pos):
        noise_symbol = self.Find_Noise()

        if not noise_symbol:
            noise_symbol = self.Create_Extra_Noise()

        noise_symbol.Set_Active(pos)

    
    def Find_Noise(self):
        # If there are no noise symbol in the pool return None to spawn particle
        if not self.noise_pool:
            return None
        
        # Check if the initial index is available, in which case loop the index back to 0
        if not self.noise_pool[0].timer:
            self.index = 0
        
        # Overflow prevent
        if self.index >= len(self.noise_pool) - 1:
            return None

        # Set the noise symbol to be the next available index
        noise_symbol = self.noise_pool[self.index]
        self.index += 1

        # If there are no free noise symbols return None to spawn a new one
        if noise_symbol.timer:
            return None
        
        return noise_symbol
    
    def Remove_Noise_Symbol_From_Active(self, noise_symbol):
        self.active_noise_symbols.remove(noise_symbol)


    # Append extra fire particle to the pool in case it runs out
    def Create_Extra_Noise(self):
        noise = Noise(self.game)
        self.active_noise_symbols.append(noise)
        return noise


    def Render(self, surf, offset):
        for noise_symbol in self.active_noise_symbols:
            noise_symbol.Render(surf, offset)

    