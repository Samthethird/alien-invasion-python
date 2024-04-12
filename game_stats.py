from pathlib import Path
import pygame
import json

class GameStats():
    '''Track statistics for Alien Invasion.'''
    def __init__(self):
        '''Initialize Statistics'''
        self.reset_stats()
        self.reset_music()

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        self.hint_activated = False
        self.hint_run = False

        # Reading high_score from save data
        self.open_high_scores()
        
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
        self.high_2_beat = False
        self.power_up_level = False
        self.one_timeM = False
        self.power_up_level_passed = False
        
        # game counter
        self.game_counter = 0
        
        # hard and insane modes acitivity.
        self.hard_mode = False
        self.insane_mode = False

        self.power_ups()
        self.permanent_power_ups()
        
    def power_ups(self):
        '''method dedicated to initializing power_up stats.'''
        # Group for current active powers
        self.active_powers = pygame.sprite.Group()
        self.permanent_powers = pygame.sprite.Group()

        # MACHINE GUN:
        self.reset_machine_gun_timer = False
        self.machine_gun_active = False
        self.shooting = False
        self.start_time = 0
        
        # GOD BULLET:
        self.reset_god_bullet_timer = False
        self.god_bullet_active = False

    def permanent_power_ups(self):
        # MANTIS GOD:
        self.mantis_god_active = False
        self.start_timeM = 0

    def reset_music(self):
        '''method for keeping track of music activity'''
        # Whether music is currently playing or not.
        self.music_playing = False

    def open_high_scores(self):
        '''Read high_scores into memory'''
        text = Path("saves/save_data.json").read_text() 
        high_scores = json.loads(text)
        
        # assign scores.
        self.high_score = high_scores['high']
        self.high_2 = high_scores['high_2']
        self.temp_2 = high_scores['high_2']
        self.high_3 = high_scores['high_3']
