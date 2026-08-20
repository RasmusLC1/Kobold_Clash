# Global listener class that notifies enemies on clatter generation
class Clatter_Subscription:
    def __init__(self):
        self.acoustic_listeners = set() # Prevents duplicates, no future checks needed

    def Subscribe_To_Acoustics(self, entity):
        self.acoustic_listeners.add(entity)

    def Unsubscribe_From_Acoustics(self, entity):
        self.acoustic_listeners.discard(entity) # .discard() handles missing keys without throwing errors

    def Broadcast_Clatter(self, clatter_pos):
        for entity in self.acoustic_listeners:
            entity.On_Clatter_Heard(clatter_pos)

    def Clear_Acoustic_Listeners(self):
        self.acoustic_listeners.clear()