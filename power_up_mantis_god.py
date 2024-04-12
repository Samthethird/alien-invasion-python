import pygame
from power_up_base import PowerUp

class MantisGodPowerUp(PowerUp):
    '''a permenant power_up.'''
    def __init__(self, ai_settings, screen, stats):
        super().__init__(ai_settings, screen, stats)
        self.image_location = "images/mantis_god.png"
        self.permanent = True
        self.update_location()

    def update_location(self):
        self.image = pygame.image.load(self.image_location)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        self.y = float(self.rect.y)

    def give_power(self):
        # make it so fire_bullet() function can shoot three bullets to three different directions.
        self.ai_settings.bullets_allowed *= 3
        self.stats.mantis_god_active = True