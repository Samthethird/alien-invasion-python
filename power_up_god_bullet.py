from power_up_base import PowerUp
from pygame.sprite import Sprite

class GodBulletPowerUp(PowerUp):
    '''child class from PowerUp for GodBulletPowerUp.'''

    def __init__(self, ai_settings, screen, alien):
        super().__init__(ai_settings, screen, alien)
