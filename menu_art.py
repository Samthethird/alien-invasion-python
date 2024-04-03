import pygame
from ship import Ship
from alien import Alien

class MenuArt():
    '''A class that make the main menu art'''

    def __init__(self, ai_settings, screen, stats, sb):
        self.ai_settings = ai_settings
        self.screen = screen
        self.stats = stats
        self.sb = sb

    def create_menu_art(self):
        '''Make the main menu art.'''
        self.create_menu_alien()
        self.create_menu_bullet()
        self.create_menu_ship()
        self.create_high_surface()
        self.sb.draw_high_scores()
        
    def create_menu_alien(self):
        '''Create an alien for the main menu art.'''
        solo_alien = Alien(self.ai_settings, self.screen, self.stats)
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

    def create_high_surface(self):
        object = pygame.Surface((300, 300), pygame.SRCALPHA)
        object.fill((200, 250, 200, 15))
        object_rect = object.get_rect()
        object_rect.top = self.sb.text_image_rect.top
        object_rect.centerx = self.sb.text_image_rect.centerx

        self.screen.blit(object, (835, 200))