import math
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''A class to manage the bullets fired from the ship.'''
    
    def __init__(self, ai_settings, screen, ship):
        '''Create a bullet on the ships current location.'''
        super().__init__()
        self.screen = screen

        # Create a bullet and correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullets position as decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.index = int

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''Moving the bullet up the screen.'''
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def update_mantis_mode(self):
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