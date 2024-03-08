import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    '''A class that handles most written information of the game.'''

    def __init__(self, ai_settings, screen, stats):
        '''Initialize score keeping attributes.'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        # Preapare initial score images.
        self.prep_images()

    def prep_score(self):
        '''Trun the score into a rendered image.'''
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)
        # Display the score on the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        '''Turn the hight score into a rendered image.'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, 
                                                 self.ai_settings.bg_color)

        # position high score.
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.screen_rect.centerx
        self.high_score_image_rect.top = self.screen_rect.top

    def show_score(self):
        '''Draw scores and ships to the screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)

    def prep_level(self):
        '''Turn level into a rendered image.'''
        self.level_image = self.font.render(str(self.stats.level), True, 
                                            self.text_color, self.ai_settings.bg_color)
        
        # Position level.
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.bottom + 10

    def prep_achivement(self):
        '''render and position "achivement"'''
        # determine whether player won or not.
        achivement_str = ""
        if self.stats.high_score_beat:
            achivement_str = "YOU BEAT YOUR HIGH-SCORE!!!"
        elif not self.stats.high_score_beat and self.stats.game_counter > 0:
            achivement_str = "YOU LOST!"
        
        # render image.
        if  achivement_str == "YOU LOST!":
            self.achivement_image = self.font.render(achivement_str, True,
                                            (160, 4, 8), self.ai_settings.bg_color)
        else:
            self.achivement_image = self.font.render(achivement_str, True,
                                                    (17, 93, 51), self.ai_settings.bg_color)
        
        # position the text
        self.achivement_image_rect = self.achivement_image.get_rect()
        self.achivement_image_rect.top = self.high_score_image_rect.bottom + 10
        self.achivement_image_rect.centerx = self.high_score_image_rect.centerx

        
    def draw_achivement(self):
        self.screen.blit(self.achivement_image, self.achivement_image_rect)

    def prep_ships(self):
        '''Show the amount of lives left.'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_achivement()

        