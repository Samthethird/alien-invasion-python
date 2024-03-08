class GameStats():
    '''Track statistics for Alien Invasion.'''
    def __init__(self, ai_settings):
        '''Initialize Statistics'''
        self.ai_settings = ai_settings
        self.reset_stats()
    
        # Start Alien Invasion in an inactive state.
        self.game_active = False
        
        # Reading high_score from save data
        self.high_score = 0
        with open(ai_settings.data_location) as high_score:
            contents = high_score.read()
        self.high_score = int(contents.rstrip())
            
    def reset_stats(self):
        '''A method for stats that reset each game.'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1