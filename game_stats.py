import pygame

class GameStats():
    '''Track statistics for Alien Invasion.'''
    def __init__(self):
        '''Initialize Statistics'''
        self.reset_stats()
        self.reset_music()

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        # Reading high_score from save data
        self.high_score = 0
        with open("saves/save_data.txt") as high_score:
            contents = high_score.read()
        self.high_score = int(contents.rstrip())
            
    def reset_stats(self):
        '''A method for stats that reset each game.'''
        # scores
        self.ships_left = 3
        self.score = 0
        self.level = 1

        # one time runs
        self.run_high_score_s = False
        self.game_over_s= False
        self.high_score_beat = False

        # game counter
        self.game_counter = 0
        
        # hard and insane modes acitivity.
        self.hard_mode = False
        self.insane_mode = False

        self.power_ups()

    def power_ups(self):
        '''method dedicated to initializing power_up stats.'''
        # Group for current active powers
        self.active_powers = pygame.sprite.Group()

        # MACHINE GUN.
        self.reset_machine_gun_timer = False
        self.machine_gun_active = False
        self.machine_gun_mode = False
        self.shooting = False
        
        # GOD BULLET:
        self.reset_god_bullet_timer = False
        self.god_bullet_active = False

    def reset_music(self):
        '''method for keeping track of music activity'''
        # Whether music is currently playing or not.
        self.music_playing = False