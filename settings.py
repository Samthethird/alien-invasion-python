class Settings():
    '''A class for storing the settings of Alien Invasion.'''

    def __init__(self, stats):
        '''Initializes the games static settings.'''
        # Display settings.
        self.screen_width = 1200 #1200
        self.screen_height = 790 #790
        self.bg_color = (230, 230, 230)
        self.stats = stats
        
        # Ship setttings.
        self.ship_limit = 3 #3

        # power up settings.
        self.cube_width = 40
        self.cube_height = 40
        self.cube_speed = 0.5
        self.god_bullet_color = (110, 0, 20)
        self.machine_gun_color = (40, 40, 100)

        self.machine_gun_timer = 9_000 # 9s
        self.god_bullet_timer = 6_000 # 6s

        # Alien settings.
        self.fleet_drop_speed = 10 #10

        # Game speed up factor.
        self.speedup_scale = 1.125 #1.1

        # Score Multiplier
        self.score_scale = 1.15
        
        self.prev_level = 16
        self.initialize_dynamic_settings()
        self.reset_god_bullet_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game.'''
        self.ship_speed_factor = 4 #1.5
        self.bullet_speed_factor = 5 #3
        self.alien_speed_factor = 2 #1
        self.cube_speed = 0.5

        # 1 means right and -1 vice versa.
        self.fleet_direction = 1 #1

        # Scoring settings.
        self.alien_points = 50

        self.alien_destruction = False
        self.bullets_allowed = 3 #3


    def reset_god_bullet_settings(self):
        '''initiate settings that can be increased by powerUps.'''
        # Bullet settings.
        self.bullet_width = 3 #3
        self.bullet_height = 15 #15
        self.bullet_color = (250, 130, 130)
        self.bullet_destruction = True

    def increase_speed(self):
        # Increase the speed settings and alien point value.
        if self.stats.level < 6 or self.stats.level == 9 or self.stats.level == 10:
            self.speed_up()
        elif self.stats.level >= 16 and self.stats.level - self.prev_level == 3:
            self.speed_up()
            self.prev_level = self.stats.level

    def speed_up(self):
            # multiply speed
            self.ship_speed_factor *= self.speedup_scale
            self.bullet_speed_factor *= self.speedup_scale
            self.alien_speed_factor *= self.speedup_scale
            self.cube_speed *= self.speedup_scale

    def increase_alien_worth(self):
        # increase points value of alines each level    
        self.alien_points = int(self.alien_points * self.score_scale)