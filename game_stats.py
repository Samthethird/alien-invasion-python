import pygame

class GameStats():
    '''Track statistics for Alien Invasion.'''
    def __init__(self, ai_settings):
        '''Initialize Statistics'''
        self.ai_settings = ai_settings
        self.reset_stats()
        self.reset_music()

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        # Reading high_score from save data
        self.high_score = 0
        with open(ai_settings.data_location) as high_score:
            contents = high_score.read()
        self.high_score = int(contents.rstrip())
            
    def reset_stats(self):
        '''A method for stats that reset each game.'''
        # Lives remaining.
        self.ships_left = self.ai_settings.ship_limit

        # Current score.
        self.score = 0
        
        # Current games level.
        self.level = 1

        # Whether high_score sound effect has been played.
        self.run_high_score_s = False

        # Whether game over sound has been played.
        self.game_over_s= False

        # Whether the high_score has already been broken.
        self.high_score_beat = False

        # How many time the game has run in the currnet session.
        self.game_counter = 0

        # Group for current active powers
        self.active_powers = pygame.sprite.Group()

        # mode for machine gun power_up.
        self.machine_gun_mode = False

    def reset_music(self):
        '''method for keeping track of music activity'''
        # Whether music is currently playing or not.
        self.music_playing = False