import pygame

class Hit():
    '''class for hit states.'''
    
    def hard_alien_hit(self, alien):
        images = [pygame.image.load("images/alien2_hit.png"),]
        alien.image = images[0]

    def insane_alien_hit(self, alien):
        images = [pygame.image.load("images/alien3_hit.png"),
                  pygame.image.load("images/alien3_hit2.png"),]
        if alien.hp == 2:
            alien.image = images[0]
        if alien.hp == 1:
            alien.image = images[1]