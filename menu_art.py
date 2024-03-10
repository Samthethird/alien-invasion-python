import pygame
from ship import Ship
from alien import Alien
from bullet import Bullet

class MenuArt():
    '''A class that make the main menu art'''

    def __init__(self, ai_settings, screen):
        self.ai_settings = ai_settings
        self.screen = screen
        
    def create_menu_art(self):
        '''Make the main menu art.'''
        self.create_menu_alien()
        self.create_menu_bullet()
        self.create_menu_ship()


    def create_menu_alien(self):
        '''Create an alien for the main menu art.'''
        solo_alien = Alien(self.ai_settings, self.screen)
        solo_alien.rect.x = 200
        solo_alien.rect.y = 250
        solo_alien.blitme()


    def create_menu_ship(self):
        '''Create a ship for the amin menu art.'''
        solo_ship = Ship(self.ai_settings, self.screen)
        solo_ship.rect.x = 200
        solo_ship.rect.y = 470
        solo_ship.blitme()


    def create_menu_bullet(self):
        '''Create a bullet for the main menu art.'''
        rect = pygame.Rect(0, 0, self.ai_settings.bullet_width,
                        self.ai_settings.bullet_height)
        rect.x = 230
        rect.y = 400
        pygame.draw.rect(self.screen, self.ai_settings.bullet_color, rect)
