import pygame

class BackGround():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.image = pygame.image.load("images/bg.jpg")
        self.image_rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.image_rect)