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
        self.ai_settings.bullets_allowed = 1000
        self.stats.machine_gun_active = True
        self.get_start_time()

    def end_power(self):
        '''end power'''
        self.stats.machine_gun_active = False
        self.ai_settings.bullets_allowed = 3
        
    def __eq__(self, other):
        '''return color for equality'''
        if isinstance(other, MachineGunPowerUp):
            return self.color == other.color
        return False
    
    def __hash__(self):
        return hash(self.color)