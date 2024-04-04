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
        self.text_color = (200, 250, 200)
        self.text_color2 = (150, 250, 200)
        self.font = pygame.font.SysFont(None, 48)
        self.high_font = pygame.font.SysFont(None, 64)

        # Preapare initial score images.
        self.prep_images()

    def prep_images(self):
        """Preping all images"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_achivement()
        self.prep_ships()
        self.prep_high_scores()

    def show_score(self):
        '''Draw all scores and ships to the screen'''
        if self.stats.game_active:
            self.screen.blit(self.level_image, self.level_image_rect)
            self.ships.draw(self.screen)
            self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)

    def prep_score(self):
        '''Trun the score into a rendered image.'''
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        # Display the score on the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        '''Turn the hight score into a rendered image.'''
        high_score_str = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        
        # position high score.
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.screen_rect.centerx
        self.high_score_image_rect.top = self.screen_rect.top

    def prep_level(self):
        '''Turn level into a rendered image.'''
        self.level_image = self.font.render(str(self.stats.level), True, 
                                            self.text_color)
        
        # Position level.
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.bottom + 10

    def prep_achivement(self):
        '''render and position "achivement"'''
        # Determine text.
        self.prep_achivement_msg()

        # position the text.
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

    def prep_achivement_msg(self):
        # determine whether the player has won or not.
        achivement_str = ""
        if self.stats.game_counter == 0:
            self.achivement_image = self.font.render(achivement_str, True,
                            (17, 93, 51))

        elif self.stats.high_score_beat:
            achivement_str = "YOU BEAT YOUR HIGH-SCORE!!!"
            # if won render green.
            self.achivement_image = self.font.render(achivement_str, True,
                                        (17, 93, 51))

        elif not self.stats.high_score_beat and self.stats.game_counter > 0:
            achivement_str = "YOU LOST!"
            # if you lost render red.
            self.achivement_image = self.font.render(achivement_str, True,
                                    (160, 4, 8))
        
    def draw_high_scores(self):
        self.screen.blit(self.high_image, self.high_rect)
        self.screen.blit(self.high_2_image, self.high_2_image_rect)
        self.screen.blit(self.high_3_image, self.high_3_image_rect)
        self.screen.blit(self.text_image, self.text_image_rect)

    def prep_high_scores(self):
        self.prep_high()
        self.prep_high_2()
        self.prep_high_3()
        self.prep_high_text()

    def prep_high_text(self):
        self.text_image = self.high_font.render("Top Scores!", True, self.text_color2)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.centerx = self.high_2_image_rect.centerx
        self.text_image_rect.centery = self.high_rect.centery - 70

    def prep_high(self):
        high_str = "1. {:,}".format(self.stats.high_score)
        self.high_image = self.high_font.render(high_str, True,
                                             self.text_color2)

        self.high_rect = self.high_score_image.get_rect()
        self.high_rect.center = (950, 300)
    
    def prep_high_2(self):
        high_2_str = "2. {:,}".format(self.stats.high_2)
        self.high_2_image = self.font.render(high_2_str, True,
                                             self.text_color2)
        self.high_2_image_rect = self.high_2_image.get_rect()
        self.high_2_image_rect.centerx = self.high_rect.centerx + 30
        self.high_2_image_rect.centery = self.high_rect.centery + 100
        
    def prep_high_3(self):
        high_3_str = "3. {:,}".format(self.stats.high_3)
        self.high_3_image = self.font.render(high_3_str, True,
                                             self.text_color2)
        self.high_3_image_rect = self.high_3_image.get_rect()
        self.high_3_image_rect.centerx = self.high_rect.centerx + 30
        self.high_3_image_rect.centery = self.high_2_image_rect.centery + 70


    def prep_hint(self):
        # arguments
        font = pygame.font.SysFont(None, 64)
        Blue = (60, 60, 120)
        message = "Hold space to rapid fire!"

        # prep
        self.image = font.render(message, True, Blue)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (600, 650)

    def draw_hint(self):
        self.screen.blit(self.image, self.image_rect)
