import pygame

pygame.mixer.init()
# Initiate menu music.
while True:
    pygame.mixer.music.load("sound_effects/music/menu_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
