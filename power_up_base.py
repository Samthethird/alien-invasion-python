import pygame
from pygame.sprite import Sprite

class PowerUp(Sprite):
    """A parent class for all powerups"""

    def __init__(self, ai_settings, screen, alien):
        """initialize attributes."""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.color = self.ai_settings.cube_color1
        self.alien = alien
        
        # Creat power-up rect and position it.
        self.rect = pygame.Rect(0, 0 ,self.ai_settings.cube_width,
                                self.ai_settings.cube_height)
        self.rect.top = self.alien.rect.bottom
        self.rect.centerx = self.alien.rect.centerx
        
        # accurate location.
        self.y = float(self.rect.y)

    def update_power_up(self):
        """make the power_up have a smooth descent"""
        self.y += self.ai_settings.cube_speed
        self.rect.y = self.y

    def draw_power_up(self):
        '''draw the powerUP'''
        pygame.draw.rect(self.screen, 
                        self.color,
                        self.rect)