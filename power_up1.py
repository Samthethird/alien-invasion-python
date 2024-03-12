import pygame

class PowerUp1():
    """A class to manage first powerup"""

    def __init__(self, ai_settings, screen):
        """initialize attributes."""
        self.ai_settings = ai_settings
        self.screen = screen

        # Creat power-up rect and position it.
        self.rect = pygame.Rect(0, 0 ,self.ai_settings.cube_width,
                                self.ai_settings.cube_height)

        # accurate location.
        self.y = float(self.rect.y)

    def update_power_up(self):
        """make the power_up have a smooth descent"""
        self.y += self.ai_settings.cube_speed
        self.rect.y = self.y

    def draw_power_up(self):
        '''draw the powerUP'''
        pygame.draw.rect(self.screen, self.ai_settings.cube_color1,
                        self.rect)