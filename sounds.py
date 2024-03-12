import pygame

class Sound():
    """
    A class to manage all the sounds
    and music in the game.
    """
    
    def __init__(self, stats):
        # Initialize the pygame sound module.
        pygame.mixer.init()
        self.stats = stats

    def high_score_beat(self):
        # initiate wining audio.
        hg_beat_s = pygame.mixer.Sound("sound_effects/won.mp3")
        hg_beat_s.set_volume(0.4)
        hg_beat_s.play()

    def high_score_not_beat(self):
        # initiate losing audio.
        lost_s = pygame.mixer.Sound("sound_effects/lose.mp3")
        lost_s.set_volume(0.4)
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

    def ship_hit(self):
        # Initiate loosing life audio.
        alien_hit_s = pygame.mixer.Sound("sound_effects/ship_hit.wav")
        alien_hit_s.set_volume(0.4)
        alien_hit_s.play()

    def next_level(self):
        # Initiate Next level audio.
        new_level_s = pygame.mixer.Sound("sound_effects/next_level.wav")
        new_level_s.set_volume(0.6)
        new_level_s.play()

    def play_music(self):
        # Determine which music to play.
        if not self.stats.music_playing:
            if self.stats.game_active:
                pygame.mixer.music.load("sound_effects/music/bg_music.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                self.stats.music_playing = True
            else:
                pygame.mixer.music.load("sound_effects/music/menu_music.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                self.stats.music_playing = True

