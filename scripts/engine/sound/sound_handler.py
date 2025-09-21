import pygame

class Sound_Handler():
    def __init__(self, game) -> None:
        self.game = game
        pygame.init()
        pygame.mixer.init()

    def Play_Sound(self, sound_name, volume = 1):
        # Disable all sounds if the player is silenced
        if self.game.player.effects.silence.effect:
            return
        if self.game.clatter.temp_disable_clatter:
            return
        
        try:
            self.game.sfx[sound_name].set_volume(volume)
            self.game.sfx[sound_name].play()
        except Exception as e:
            print(f"Wrong sound input {e}", sound_name, volume)


    # Player noise disabled
    def Play_Menu_Sound(self, sound_name, volume = 1):
        try:
            self.game.sfx[sound_name].set_volume(volume)
            self.game.sfx[sound_name].play()
        except Exception as e:
            print(f"Wrong sound input {e}", sound_name, volume)

    def Check_If_Sound_Exist(self, sound_name) -> bool:
        return sound_name in self.game.sfx
    
    def Set_HeartBeat_Sound(self, awakening_level):
        if awakening_level == 0:
            pygame.mixer.music.stop()  # stop playback
            return
        
        pygame.mixer.music.load('data/sounds/awakening/heartbeat/' + str(awakening_level) +'_heartbeat.mp3')

        if awakening_level == 5:
            pygame.mixer.music.set_volume(0.6)
        elif awakening_level == 3:
            pygame.mixer.music.set_volume(0.2)
        else:
            pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)