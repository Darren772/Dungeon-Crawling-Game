import pygame

class Audio:
    """This class handle all audio for the game, including sound effects and background music"""
    def __init__(self):
        """initialize all audio that used in the game"""
        # Initialize mixer 
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.mana_regen_sound = pygame.mixer.Sound("audio/mana_regen.wav")
        self.mana_regen_sound.set_volume(0.25)
        
        self.heal_sound = pygame.mixer.Sound("audio/heal.wav")
        self.heal_sound.set_volume(0.25)

        self.fireball_sound = pygame.mixer.Sound("audio/fireball.wav")
        self.fireball_sound.set_volume(0.25)
        
        self.walking_sound = pygame.mixer.Sound("audio/walking.wav")
        self.walking_sound.set_volume(0.75)
        
        self.soundtrack = pygame.mixer.Sound("audio/soundtrack.wav")
        self.soundtrack.set_volume(0.2)
        
        self.win_sound = pygame.mixer.Sound("audio/win.wav")
        self.win_sound.set_volume(0.32)
        
        self.game_over_sound = pygame.mixer.Sound("audio/lose.wav")
        self.game_over_sound.set_volume(0.32)
        
        self.battle_music = pygame.mixer.Sound("audio/battle.ogg")
        self.battle_music.set_volume(0.3)
        
        self.encounter_sound = pygame.mixer.Sound("audio/encounter.mp3")
        self.encounter_sound.set_volume(0.4)

        self.blessing_sound = pygame.mixer.Sound("audio/node/blessing.ogg")
        self.blessing_sound.set_volume(0.5)

        self.acidic_sound = pygame.mixer.Sound("audio/node/acid.ogg")
        self.acidic_sound.set_volume(0.75)

        self.bgm_channel = pygame.mixer.Channel(0) 

    def play_soundtrack(self):
        """Play main background music"""
        if not self.bgm_channel.get_busy():
            self.bgm_channel.play(self.soundtrack, loops=-1)

    def pause_bgm(self):
        """pause the background music"""
        self.bgm_channel.pause()

    def unpause_bgm(self):
        """unpause the background music"""
        self.bgm_channel.unpause()