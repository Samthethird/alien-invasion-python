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

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        self.index = int

    def update(self):
        '''Moving the bullet up the screen.'''
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def update_mantis_mode(self):
        self.y -= self.speed_factor
        
        if self.index == 1:
            # if first bullet, go left
            self.x -= self.speed_factor
            
        elif self.index == 3:
            # if third bullet, go right
            self.x += self.speed_factor

        self.rect.y = self.y

    def draw_bullet(self):
        '''Draw the bullet on the screen.'''
        pygame.draw.rect(self.screen,
                         self.color,
                         self.rect,)