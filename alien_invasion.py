from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from particles import ParticleSystem
from background import BackGround
from scoreboard import Scoreboard
from game_stats import GameStats
from pygame.sprite import Group
from settings import Settings
from menu_art import MenuArt
import game_functions as gf
from button import Button
from sounds import Sound
from ship import Ship
from hit import Hit
import pygame

# bug fixes
 
class AlienInvasion():
    '''Class for the game alien invasion.'''

    def __init__(self):
        '''Initialize pygame, Settings and self.screen object.'''
        pygame.init()
        self.stats = GameStats()
        self.ai_settings = Settings(self.stats)
        
        # self.Screen object.
        self.screen = pygame.display.set_mode(
            (self.ai_settings.screen_width, self.ai_settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Instances.
        self.particle_system = ParticleSystem()
        self.play_button = Button(self.ai_settings, self.screen, "Play")
        self.sb = Scoreboard(self.ai_settings, self.screen, self.stats)
        self.menu_art = MenuArt(self.ai_settings, self.screen, self.stats, 
                                self.sb)
        self.bg = BackGround(self.screen)
        self.sound = Sound()
        self.hit = Hit()
        self.clock = pygame.time.Clock()

        # Groups.
        self.ship = Ship(self.ai_settings, self.screen)
        self.power_ups = Group()
        self.bullets = Group()
        self.aliens = Group()
        self.health_drops = Group()

    def run_game(self):
        '''run all game functions'''
        # Main game loop.
        while True:
            print(self.power_ups)
            # GAME NOT ACTIVE.
            gf.check_events(self.ai_settings, self.screen, 
                            self.stats, self.sb, self.play_button, 
                            self.ship, self.aliens, 
                            self.bullets, self.sound, self.power_ups,
                            )
            gf.check_particles(self.ai_settings, self.particle_system, 
                               self.bullets, self.stats, self.power_ups,
                               self.health_drops)
            gf.check_machine_gun_mode(self.ai_settings, self.screen, 
                                      self.stats, self.ship, self.bullets, 
                                      self.sound
                                      )

            # GAME ACTIVE.
            if self.stats.game_active:
                # lock on 180 F_P_S
                self.clock.tick(180)
                print(self.stats.active_powers)
                self.ship.update()
                gf.update_bullet(self.ai_settings, self.screen, self.stats, 
                                self.sb, self.ship, self.aliens, self.bullets,
                                self.sound, self.power_ups, self.hit, 
                                self.health_drops,
                                )
                gf.update_aliens(self.ai_settings, self.stats, self.sb , self.screen, 
                                self.ship, self.aliens, self.bullets, self.sound, 
                                self.power_ups
                                )
                gf.update_power_ups(self.sound , self.sb, self.screen.get_rect(),
                                    self.stats, self.ship, self.power_ups,
                                    self.health_drops
                                    )
                gf.end_power(self.ai_settings, self.stats, self.stats.active_powers, 
                            )
            gf.update_screen(self.screen, self.stats, self.sb, 
                            self.ship, self.aliens, self.bullets, self.play_button, 
                            self.sound, self.menu_art, self.power_ups, self.bg,
                            self.particle_system, self.health_drops
                            )
            
            gf.update_music(self.stats, self.sound)

            
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()