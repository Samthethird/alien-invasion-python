from power_up_base import PowerUp
import pygame

class GodBulletPowerUp(PowerUp):
    '''child class from PowerUp for GodBulletPowerUp.'''

    def __init__(self, ai_settings, screen, stats, alien):
        '''initialize parent settings'''
        super().__init__(ai_settings, screen, stats, alien)
        self.color = ai_settings.god_bullet_color
        self.image_location = "images/god_bullet.png"

        self.update_location(alien)
        
    def give_power(self):
        '''change the game settings, to apply power.'''
        self.stats.god_bullet_active = True
        self.ai_settings.bullet_width = 30
        self.ai_settings.bullet_height = 150
        self.ai_settings.bullet_color = self.color
        self.ai_settings.bullet_destruction = False
        self.get_start_time()

    def end_power(self):
        '''end power'''
        self.stats.god_bullet_active = False
        self.ai_settings.reset_god_bullet_settings()