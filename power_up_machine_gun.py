from power_up_base import PowerUp
import pygame

class MachineGunPowerUp(PowerUp):
    '''A class for machine gun power_UP'''

    def __init__(self, ai_settings, screen, stats, alien):
        """initialize parent settings and replace color"""
        super().__init__(ai_settings, screen, stats, alien)
        self.image_location = 'images/machine_gun.png'
        self.update_location(alien)
        
    def give_power(self):
        '''give the powers of machine gun to the player.'''
        self.ai_settings.bullets_allowed = 1000
        self.stats.machine_gun_active = True
        self.get_start_time()

    def end_power(self):
        '''end power'''
        self.stats.machine_gun_active = False
        if self.stats.mantis_active:
            self.ai_settings.bullets_allowed = 6

        elif self.stats.mantis_god_active:
            self.ai_settings.bullets_allowed = 9
            
        else:
            self.ai_settings.bullets_allowed = 3
        