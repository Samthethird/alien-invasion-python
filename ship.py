import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Modeling the ship and all its attributes.'''

    def __init__(self, ai_settings, screen):
        '''Initialize the ship and its start position.'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
    
        # Loading the the ships image and getting rect.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Positioning the ship at the bottem center.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Stroring a decimal value for the ships center.
        self.center = float(self.rect.centerx)

        # Movement flags.
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        '''update the ships position based on the movement flag.'''
        # Update the center value.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update the ships location with self.center.
        self.rect.centerx = self.center

    def blitme(self):
        '''Dawing the ship at its current location.'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center the ship on the screen.'''
        self.center = self.screen_rect.centerx