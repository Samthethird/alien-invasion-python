import pygame
from pygame.sprite import Sprite

class PowerUp(Sprite):
    """A parent class for all powerups"""

    def __init__(self, ai_settings, screen, stats, alien):
        """initialize attributes."""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen    
        self.alien = alien 
        self.start_time = int()
        self.stats = stats
        
        # power activity state
        self.power_active = False

    def update_location(self):
        # Load power-up image and position it.
        self.image = pygame.image.load(self.image_location)
        self.rect = self.image.get_rect()
        self.rect.top = self.alien.rect.bottom
        self.rect.centerx = self.alien.rect.centerx
        
        # accurate location.
        self.y = float(self.rect.y)

    def update_power_up(self):
        """make the power_up have a smooth descent"""
        self.y += self.ai_settings.cube_speed
        self.rect.y = self.y

    def blitme(self):
        '''draw the powerUP'''
        self.screen.blit(self.image, self.rect)
        
    def get_start_time(self):
        '''get the time when the power was give.'''
        self.start_time = pygame.time.get_ticks()
