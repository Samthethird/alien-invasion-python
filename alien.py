import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''A class to represent a single alien in a fleet.'''

    def __init__(self, ai_settings, screen, stats):
        '''Initialize the alien and its starting position.'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats
        
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # Start each alien in the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the aliens exact position.
        self.x = float(self.rect.x)

        self.increase_difficulty()

    def blitme(self):
        '''Draw the alien in its current location.'''
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        '''Return True if alien is at the edge of the screen.'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        '''Move the alien to the right or the left.'''
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def increase_difficulty(self):
        '''change the difficulty of the alines.'''
        if self.stats.hard_mode:
            self.image = pygame.image.load("images/alien2_normal.png")
            self.hp = 2

        #activate insane mode.
        elif self.stats.insane_mode:
            self.image = pygame.image.load("images/alien3_normal.png")
            self.hp = 3
