from power_up_base import PowerUp
import pygame

class MachineGunPowerUp(PowerUp):
    '''A class for machine gun power_UP'''

    def __init__(self, ai_settings, screen, stats, alien):
        """initialize parent settings and replace color"""
        super().__init__(ai_settings, screen, stats, alien)
        self.color = ai_settings.machine_gun_color

    def give_power(self):
        '''give the powers of machine gun to the player.'''
        self.stats.machine_gun_mode = True
        self.shooting = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shooting = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.shooting = False   

    def end_power(self):
        '''end power'''