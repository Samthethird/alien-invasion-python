import pygame

class Hit():
    def __init__(self) -> None:
        '''init'''        

    def hard_alien_hit(self, alien,):
        alien.image = pygame.image.load("images/alien2_normal.png")
    
    def insane_alien_hit(self, alien):
        