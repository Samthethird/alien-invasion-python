import pygame

class Sound():
    """
    A class to manage all the sounds
    and music in the game.
    """
    
    def __init__(self):
        # Initialize the pygame sound module.
        pygame.mixer.init()

    def high_score_beat(self):
        # initiate wining audio.
        hg_beat_s = pygame.mixer.Sound("sound_effects/won.mp3")
        hg_beat_s.set_volume(0.2)
        hg_beat_s.play()

    def high_score_not_beat(self):
        # initiate losing audio.
        lost_s = pygame.mixer.Sound("sound_effects/lose.mp3")
        lost_s.set_volume(0.2)
        lost_s.play()

    def fire_bullet(self):
        # Initiate bullet firing audio.
        bullet_s = pygame.mixer.Sound("sound_effects/ship_shoot.wav")
        bullet_s.play()

    def high_score_broke(self):
        # Initiate high score broken audio.
        hs_file_name = "sound_effects/broke_high_score.wav"
        high_score_borke_s = pygame.mixer.Sound(hs_file_name)
        high_score_borke_s.set_volume(0.5)
        high_score_borke_s.play()
