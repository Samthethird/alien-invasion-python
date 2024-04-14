import math
import pygame
from pygame.sprite import Sprite

# how to make diagonal bullets
class Bullet(Sprite):
    '''A class to manage the bullets fired from the ship.'''
    
    def __init__(self, ai_settings, screen, ship, stats):
        '''Create a bullet on the ships current location.'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.ship = ship
        self.stats = stats

        self.rect = pygame.Rect(0, 0, self.ai_settings.bullet_width,
                        self.ai_settings.bullet_height)
        self.rect.midtop = self.ship.rect.midtop

        # Store the bullets position as decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.index = int

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def set_location(self):
        # Create a bullet and correct position.
        (x, y) = self.ship.rect.midtop
        if self.stats.god_bullet_active:
            increment = 25
        else:
            increment = 15

        if self.stats.mantis_active:
            if self.index == 1:
                self.rect.midtop = (x-increment, y)
            if self.index == 2:
                self.rect.midtop = (x+increment, y)

    def update(self):
        '''Moving the bullet up the screen.'''
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def update_mantis_god_mode(self):
        if self.index == 1:
            # if first bullet, go left
            self.y -= self.speed_factor
            self.x -= self.speed_factor * 0.2
        
        elif self.index == 2:
            self.y -= self.speed_factor
            
        elif self.index == 3:
            # if third bullet, go right
            self.y -= self.speed_factor 
            self.x += self.speed_factor * 0.2

        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        '''Draw the bullet on the screen.'''
        pygame.draw.rect(self.screen,
                         self.color,
                         self.rect,)